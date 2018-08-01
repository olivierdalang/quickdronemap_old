import math, os, datetime, tempfile, json

from PIL import Image as PILImage
from PIL import ExifTags as PILExifTags

import numpy as np

from scipy.optimize import least_squares
from scipy.optimize import minimize
import scipy as sp
import scipy.misc
import imreg_dft as ird
import imreg_dft.utils

from qgis.core import (QgsPointXY,QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsRasterTransparency,QgsProject, QgsMessageLog)
from qgis.gui import (QgsRubberBand)

from qgis.core import QgsWkbTypes

from PyQt5.QtCore import Qt

from .utils import absolute_angle_difference, gps_tag_to_decimal_degress, resized, transform_matrix


# Threshold over which images are not considered being in the same sequence (in radians)
ANGLE_THRESHOLD = 15.0 / 180.0 * math.pi # 15°
# Threshold over which images are not considered being in the same sequence (in seconds)
TIME_THRESHOLD = 20
# Similarity will be computed on downscaled images. The lower the factor, the fastest the process
DOWNSCALING_FACTOR = 0.025
# Parameter for imreg_dft (higher is better but slower)
IMREG_DFT_NUMITER = 5
# Parameter for imreg_dft (to determine extend parameter in pixel values, should correspond to typical image overlap)
# IMREG_DFT_EXTEND_RATIO = 0.333
IMREG_DFT_EXTEND = 50
# Similarities under this threshold won't be taken into account (probably invalid)
SUCCESS_THRESHOLD = 0.1


# Add some operands to QgsPointXY
def add_qgs_points(self, other):
    return QgsPointXY(self.x()+other.x(),self.y()+other.y())
QgsPointXY.__add__ = add_qgs_points
def sub_qgs_points(self, other):
    return QgsPointXY(self.x()-other.x(),self.y()-other.y())
QgsPointXY.__sub__ = sub_qgs_points
def mul_qgs_points(self, factor):
    return QgsPointXY(self.x()*factor,self.y()*factor)
QgsPointXY.__mul__ = mul_qgs_points
def rotated(self, angle):
    return QgsPointXY( math.cos(angle)*self.x() - math.sin(angle)*self.y(), math.sin(angle)*self.x() + math.cos(angle)*self.y() )
QgsPointXY.rotated = rotated
def dist(self):
    return math.sqrt(self.x()**2+self.y()**2)
QgsPointXY.dist = dist


class DroneMap():

    def __init__(self, iface, folder):
        self.iface = iface
        self.folder = folder
        self.images = []
        self.edges = []
        
        self.crs_src = QgsCoordinateReferenceSystem(4326)
        self.crs_dest = None
        self.xform = None

    def reproject(self, lon, lat):
        """
        This returns a reprojected point, and determines the map's CRS automatically if not set using UTM grid applicable to the first image's lat lon
        """
        if self.xform is None:
            # if the CRS hasn't been determined yet, we set it from the first image's lat/lon (take the UTM crs)
            utm_i = str(int(math.floor((self.images[0].lon + 180) / 6 ) % 60) + 1).zfill(2)
            epsg_code = int('326' + utm_i) if (self.images[0].lat >= 0) else int('327' + utm_i)
            self.crs_dest = QgsCoordinateReferenceSystem(epsg_code)
            self.xform = QgsCoordinateTransform(self.crs_src, self.crs_dest, QgsProject.instance())
        return self.xform.transform(QgsPointXY(lon, lat))

    def process(self):
        """
        Main process that go through all images and sets their transformation parameters
        """

        QgsMessageLog.logMessage("1/ Instantiating all images...", "QuickDroneMap")
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".JPG"):
                    image_path = os.path.join(root, file)
                    image = Image(self, image_path)
                    self.images.append(image)
        # self.images = self.images[0:25]
        # for i in [301,300,329]: # 3 images, transform fails on all of them
        # for i in [397,398,364]: # 3 images, transform fails on one of them
        # for i in [377,380,381]: # 3 images, transform works on all of them
        #     path = "C:\\Users\\Olivier\\Dropbox\\Affaires\\SPC\\Sources\\quickdronemap\\test\\data\\DJI_{0:04d}.JPG".format(i)
        #     self.images.append(Image(self, path))

        QgsMessageLog.logMessage("2/ Assigning ids", "QuickDroneMap")
        for i, image in enumerate(self.images):
            image.id = i


        QgsMessageLog.logMessage("2/ Loading image attributes and parsing exif tags...", "QuickDroneMap")
        for image in self.images:
            image.set_attributes()

        QgsMessageLog.logMessage("3/ Building image sequences...", "QuickDroneMap")
        sorted_images = sorted(self.images, key=lambda x: x.timestamp)
        for i in range(len(sorted_images)):

            prev_image = sorted_images[i-1] if i>0 else None
            image = sorted_images[i]
            next_image = sorted_images[i+1] if i<len(sorted_images)-1 else None

            if prev_image is None or next_image is None:
                continue

            angle_p_i = math.atan2(image.point.x()-prev_image.point.x(),-image.point.y()+prev_image.point.y())
            angle_i_n = math.atan2(next_image.point.x()-image.point.x(),-next_image.point.y()+image.point.y())

            # Checking if the three images are aligned (if not, we're probably at an angle)
            dA = absolute_angle_difference(angle_p_i, angle_i_n)
            if dA > ANGLE_THRESHOLD:
                continue

            # Checking if the three images are near enough timewise, if not, it could be separate flights
            dT1 = image.timestamp - prev_image.timestamp
            dT2 = next_image.timestamp - image.timestamp
            if dT1 > TIME_THRESHOLD or dT2 > TIME_THRESHOLD:
                continue

            prev_image.next_image = image
            image.prev_image = prev_image
            image.next_image = next_image
            next_image.prev_image = image

        QgsMessageLog.logMessage("4/ Deriving orientation from image sequence", "QuickDroneMap")
        for image in self.images:
            # if the direction wasn't set in the Exif tags, we derive it from the image sequences
            if image.angle is None:
                img_a = image.prev_image or image 
                img_b = image.next_image or image 
                # TODO : reenable this
                # image.angle = math.atan2(img_b.point.x()-img_a.point.x(),-img_b.point.y()+img_a.point.y())
                image.angle = 0.0

        QgsMessageLog.logMessage("5/ Building image neighbourhood graph...", "QuickDroneMap")
        from scipy.spatial import Delaunay
        points = [(i.point.x(),i.point.y()) for i in self.images]
        triangulation = Delaunay(points)

        done = [[False for _i2 in self.images] for _i1 in self.images]
        for tri in triangulation.simplices:
            i1,i2,i3 = tri
            if not done[i1][i2]:
                e = Edge(self.images[i1], self.images[i2])
                self.edges.append(e)
                self.images[i1].edges.append(e)
                self.images[i2].edges.append(e)
                done[i1][i2] = True
            if not done[i1][i3]:
                e = Edge(self.images[i1], self.images[i3])
                self.edges.append(e)
                self.images[i1].edges.append(e)
                self.images[i3].edges.append(e)
                done[i1][i3] = True
            if not done[i2][i3]:
                e = Edge(self.images[i2], self.images[i3])
                self.edges.append(e)
                self.images[i2].edges.append(e)
                self.images[i3].edges.append(e)
                done[i2][i3] = True

        QgsMessageLog.logMessage("6/ Computing similarities", "QuickDroneMap")
        for edge in self.edges:
            edge.compute_transform()

        initial_guess_np, _ = self.get_initial_values_and_bounds()
        QgsMessageLog.logMessage("Initial fitness is {}".format(self.calculate_fitness(initial_guess_np)), "QuickDroneMap")

        # print("TESTING QUALITY OF SIMILARITY (disable optimization to do this)")
        # done = []
        # edges_to_delete = []
        # for edge in self.edges:

        #     if edge.imageA in done or edge.imageB in done:
        #         edges_to_delete.append(edge)
        #         continue

        #     done.append(edge.imageA)
        #     done.append(edge.imageB)

        #     d_angle = edge.angle
        #     edge.imageB.angle = edge.imageA.angle + d_angle

        #     f_scale = edge.scale
        #     edge.imageB.scale = edge.imageA.scale * f_scale

        #     d_point = QgsPointXY(edge.tvec[0],edge.tvec[1])
        #     d_point = d_point.rotated(edge.imageA.angle)
        #     d_point *= edge.imageA.pixel_size/DOWNSCALING_FACTOR
        #     edge.imageB.point = edge.imageA.point + d_point
        # for edge in edges_to_delete:
        #     self.edges.remove(edge)


        # print("AFTER PROTOTYPE PLACEMENT")
        # initial_guess_np, _ = self.get_initial_values_and_bounds()
        # self.calculate_fitness(initial_guess_np)


        QgsMessageLog.logMessage("7/ Optimizing", "QuickDroneMap")
        initial_guess_np, bounds = self.get_initial_values_and_bounds()
    
        # res_1 = least_squares(calculate_fitness, initial_guess_np, bounds=([b[0] for b in bounds],[b[1] for b in bounds]))
        res_1 = minimize(self.calculate_fitness, initial_guess_np, bounds=bounds)

        for image in self.images:
            px = res_1.x[image.id*4+0]
            py = res_1.x[image.id*4+1]
            pa = res_1.x[image.id*4+2]
            ps = res_1.x[image.id*4+3]
            image.point = QgsPointXY(px, py)
            image.angle = pa
            image.psize = ps

        initial_guess_np, _ = self.get_initial_values_and_bounds()
        QgsMessageLog.logMessage("After optimization fitness is {}".format(self.calculate_fitness(initial_guess_np)), "QuickDroneMap")
        
        QgsMessageLog.logMessage("8/ Computing all transforms...", "QuickDroneMap")
        for image in self.images:
            image.update_transform()

        QgsMessageLog.logMessage("9/ Creating debug jsons files", "QuickDroneMap")
        edg_data = {"type": "FeatureCollection","features": [], "crs": {"type": "EPSG","properties": {"code": 32628}}} # TODO : use self.crs
        for edge in self.edges:
            coords = [[edge.imageA.point.x(), edge.imageA.point.y()],[edge.imageB.point.x(), edge.imageB.point.y()]]
            props = {k:v for (k,v) in vars(edge).items()}
            props['angle_a'] = edge.imageA.angle
            props['angle_b'] = edge.imageB.angle
            feature = {"type": "Feature","properties": props,"geometry": {"type": "LineString","coordinates": coords}}
            edg_data['features'].append(feature)

        
        edg_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.geojson', delete=False)
        json.dump(edg_data, edg_file, default=lambda o: str(o))
        edg_file.close()
        layer = self.iface.addVectorLayer(edg_file.name,"[DEBUG] Edges","ogr")
        layer.loadNamedStyle(os.path.join(os.path.dirname(os.path.realpath(__file__)),'debug_edges_style.qml'))
        
        graph_data = {"type": "FeatureCollection","features": [], "crs": {"type": "EPSG","properties": {"code": 4326}}} # TODO : use self.crs
        for edge in self.edges:
            coords = [[edge.imageA.lon, edge.imageA.lat],[edge.imageB.lon, edge.imageB.lat]]
            props = {k:v for (k,v) in vars(edge).items()}
            feature = {"type": "Feature","properties": props,"geometry": {"type": "LineString","coordinates": coords}}
            graph_data['features'].append(feature)

        graph_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.geojson', delete=False)
        json.dump(graph_data, graph_file, default=lambda o: str(o))
        graph_file.close()
        layer = self.iface.addVectorLayer(graph_file.name,"[DEBUG] Graph","ogr")
        layer.loadNamedStyle(os.path.join(os.path.dirname(os.path.realpath(__file__)),'debug_graph_style.qml'))


    def get_initial_values_and_bounds(self):
        initial_guess = []
        bounds = []
        for image in self.images:
            initial_guess.append(image.point.x())
            initial_guess.append(image.point.y())
            initial_guess.append(image.angle)
            initial_guess.append(image.scale)

            GPS_ACCURACY = 100

            bounds.append((image.point.x()-GPS_ACCURACY,image.point.x()+GPS_ACCURACY))
            bounds.append((image.point.y()-GPS_ACCURACY,image.point.y()+GPS_ACCURACY))
            bounds.append((-math.pi,math.pi))
            bounds.append((0.999,1.001))
        initial_guess_np = np.array(initial_guess, dtype=float)
        return initial_guess_np, bounds

    def calculate_fitness(self, x):
        total_fitness = 0
        ignored_count = 0
        for edge in self.edges:

            if edge.success is not None and edge.success < SUCCESS_THRESHOLD:
                ignored_count += 1
                continue

            px_a = x[edge.imageA.id*4+0]
            py_a = x[edge.imageA.id*4+1]
            pa_a = x[edge.imageA.id*4+2]
            ps_a = x[edge.imageA.id*4+3]
            px_b = x[edge.imageB.id*4+0]
            py_b = x[edge.imageB.id*4+1]
            pa_b = x[edge.imageB.id*4+2]
            ps_b = x[edge.imageB.id*4+3]
            score = edge.calculate_score(px_a, py_a, pa_a, ps_a,
                                         px_b, py_b, pa_b, ps_b)
            total_fitness += score
        # QgsMessageLog.logMessage("Total fitness is {} ({} edges ignored)".format(total_fitness,ignored_count), "QuickDroneMap")
        return total_fitness

    def load_worldfiles(self):
        for image in self.images:
            image.write_worldfile()
            image.load_worldfile(self.iface)

    def load_vrts(self):
        for image in self.images:
            image.write_vrt()
            image.load_vrt(self.iface)


class Image():

    def __init__(self, drone_map, path):
        self.drone_map = drone_map
        # Image properties
        self.id = None # must be initialized after instantiation, starting at 0 and with no missing values, as parameters array for optimization rely on those
        self.path = path
        self.width = None
        self.height = None
        # Exif tags
        self.focal = None
        self.timestamp = None
        self.lat = None
        self.lon = None
        self.direction = None
        self.altitude = None
        self.pixel_size = None

        # neighbouring attributes
        self.prev_image = None
        self.next_image = None
        self.edges = []

        # transform attributes
        self.point = None
        self.angle = None
        self.scale = None

        # corrections
        # self.d_point = QgsPointXY(0,0)
        # self.d_direction = 0
        # self.f_pixel_size = 1.0

        # transform (according to Worldfile definition (see wikipedia)
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None

    def name(self):
        return os.path.basename(self.path)

    def set_attributes(self):
        """
        This sets the instance attributes based on the image and the exif tags
        """

        pil_image = PILImage.open(self.path)

        # Get the exif data
        # Thanks https://gist.github.com/erans/983821
        exif_data = {}
        info = pil_image._getexif()
        if info:
            for tag, value in info.items():
                decoded = PILExifTags.TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = PILExifTags.GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value

        gps_latitude = exif_data.get("GPSInfo",{}).get("GPSLatitude")
        gps_latitude_ref = exif_data.get("GPSInfo",{}).get('GPSLatitudeRef')
        gps_longitude = exif_data.get("GPSInfo",{}).get('GPSLongitude')
        gps_longitude_ref = exif_data.get("GPSInfo",{}).get('GPSLongitudeRef')
        gps_altitude = exif_data.get("GPSInfo",{}).get('GPSAltitude')
        gps_altitude_ref = exif_data.get("GPSInfo",{}).get('GPSAltitudeRef')
        gps_direction = exif_data.get("GPSInfo",{}).get('GPSImgDirection')
        gps_direction_ref = exif_data.get("GPSInfo",{}).get('GPSImgDirectionRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = gps_tag_to_decimal_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = gps_tag_to_decimal_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

        # image attributes
        self.width, self.height = pil_image.size
        # exif attributes
        self.lat, self.lon = lat, lon
        self.focal = float(exif_data["FocalLengthIn35mmFilm"])
        self.timestamp = datetime.datetime.strptime(exif_data["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S").timestamp()
        self.altitude = gps_altitude[0] / gps_altitude[1]
        self.direction = float(gps_direction) if gps_direction is not None else None
        self.pixel_size = (self.altitude * 35.0 / self.focal) / float(self.width)
        # transform attributes
        self.point = self.drone_map.reproject(lon,lat)
        self.angle = float(gps_direction) if gps_direction is not None else None
        self.scale = 1.0

    def update_transform(self):
        """
        This updates the image's transform parameters (in worldfile standards) according to it's attributes
        """

        self.a = self.scale * self.pixel_size * math.cos(self.angle)
        self.d = self.scale * self.pixel_size * math.sin(self.angle)
        self.b = self.d
        self.e = -self.a
        self.c = self.point.x() - self.a*self.width/2.0 - self.b*self.height/2.0
        self.f = self.point.y() - self.d*self.width/2.0 - self.e*self.height/2.0

        self.bounding_box = [[self.c,self.f],[self.c+self.a*self.width,self.f+self.d*self.width],[self.c+self.a*self.width+self.b*self.height,self.f+self.d*self.width+self.e*self.height],[self.c+self.b*self.height,self.f+self.e*self.height],]

    def write_worldfile(self):
        # CREATE THE WORLDFILE
        open(self.path+"w", 'w').write("{a}\n{d}\n{b}\n{e}\n{c}\n{f}".format(a=self.a,d=self.d,b=self.b,e=self.e,c=self.c,f=self.f))
        
    def load_worldfile(self, iface, suffix=""):
        # Add to project
        layer = iface.addRasterLayer(self.path,"WORLD-{}{}".format(self, suffix))
        layer.setCrs(self.drone_map.crs_dest)
        
        # We make black pixels transparent to remove the rotated frame, not ideal if there are actually black pixels in the image
        rasterTransparency = layer.renderer().rasterTransparency()
        pixel = QgsRasterTransparency.TransparentThreeValuePixel()
        pixel.red, pixel.green, pixel.blue, pixel.percentTransparent = 0,0,0,100
        rasterTransparency.setTransparentThreeValuePixelList([pixel])

    def write_vrt(self):
        # CREATE THE VRT
        xsize, ysize=2000,2000
        xoff=int((self.width-xsize)/2.0)
        yoff=int((self.width-xsize)/2.0)
        vrt = """
        <VRTDataset rasterXSize="{width}" rasterYSize="{height}">
            <GeoTransform>{c},{a},{d},{f},{b},{e}</GeoTransform>
            <VRTRasterBand dataType="Byte" band="1"><ColorInterp>Red</ColorInterp><SimpleSource>
                    <SourceFilename relativeToVRT="0" shared="0">{path}</SourceFilename>
                    <SourceProperties RasterXSize="{width}" RasterYSize="{height}" DataType="Byte" BlockXSize="{width}" BlockYSize="1" />
                    <SourceBand>1</SourceBand>
                    <SrcRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
                    <DstRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
            </SimpleSource></VRTRasterBand>
            <VRTRasterBand dataType="Byte" band="2"><ColorInterp>Green</ColorInterp><SimpleSource>
                    <SourceFilename relativeToVRT="0" shared="0">{path}</SourceFilename>
                    <SourceProperties RasterXSize="{width}" RasterYSize="{height}" DataType="Byte" BlockXSize="{width}" BlockYSize="1" />
                    <SourceBand>2</SourceBand>
                    <SrcRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
                    <DstRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
            </SimpleSource></VRTRasterBand>
            <VRTRasterBand dataType="Byte" band="3"><ColorInterp>Blue</ColorInterp><SimpleSource>
                    <SourceFilename relativeToVRT="0" shared="0">{path}</SourceFilename>
                    <SourceProperties RasterXSize="{width}" RasterYSize="{height}" DataType="Byte" BlockXSize="{width}" BlockYSize="1" />
                    <SourceBand>3</SourceBand>
                    <SrcRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
                    <DstRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
            </SimpleSource></VRTRasterBand>
        </VRTDataset>"""
        vrt = vrt.format(path=self.path, width=self.width, height=self.height, xsize=xsize, ysize=ysize, xoff=xoff, yoff=yoff, a=self.a, b=self.b, c=self.c, d=self.d, e=self.e, f=self.f)
        open(self.path+".vrt", 'w').write(vrt)

    def load_vrt(self, iface, suffix=""):
        # Add to project
        layer = iface.addRasterLayer(self.path+".vrt","VRT-{}{}".format(self, suffix))
        layer.setCrs(self.drone_map.crs_dest)
        
        # We make black pixels transparent to remove the rotated frame, not ideal if there are actually black pixels in the image
        rasterTransparency = layer.renderer().rasterTransparency()
        pixel = QgsRasterTransparency.TransparentThreeValuePixel()
        pixel.red, pixel.green, pixel.blue, pixel.percentTransparent = 0,0,0,100
        rasterTransparency.setTransparentThreeValuePixelList([pixel])

    def __repr__(self):
        return "{} [{}]".format(self.name(), self.id)

class Edge():
    
    def __init__(self, imageA, imageB):
        self.imageA = imageA
        self.imageB = imageB

        self.tvec = None
        self.angle = None
        self.scale = None
        self.success = None

    def other(self, image):
        if image is self.imageA:
            return self.imageB
        elif image is self.imageB:
            return self.imageA

    def compute_transform(self):
        src_img_path = resized(self.imageA.path, factor=DOWNSCALING_FACTOR)
        mvg_img_path = resized(self.imageB.path, factor=DOWNSCALING_FACTOR)
        
        cache_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache.txt')

        if os.path.exists(cache_path):
            cache_file = open(cache_path, "r")
            lines = cache_file.readlines()
            cache_file.close()
            cache = {k:v for k,v in [l.rsplit('\t',1) for l in lines]}
        else:
            cache = {}

        key = "{}\t{}\t{}\t{}".format(src_img_path,mvg_img_path,IMREG_DFT_NUMITER,IMREG_DFT_EXTEND)

        try:
            val = json.loads(cache[key])
            self.tvec = val['tvec']
            self.angle = val['angle']
            self.scale = val['scale']
            self.success = val['success']
        except KeyError:

            src_data = sp.misc.imread(src_img_path, True)
            mvg_data = sp.misc.imread(mvg_img_path, True)

            src_data = imreg_dft.utils.extend_by(src_data, IMREG_DFT_EXTEND)
            mvg_data = imreg_dft.utils.extend_by(mvg_data, IMREG_DFT_EXTEND)

            result = ird.similarity(src_data, mvg_data, numiter=IMREG_DFT_NUMITER)

            self.tvec = result['tvec'][1], -result['tvec'][0] # (Y,X)
            self.angle = result['angle'] / 180.0 * math.pi
            self.scale = result['scale']
            self.success = result['success']

            val = json.dumps({'tvec':self.tvec,'angle':self.angle,'scale':self.scale,'success':self.success})
            
            cache_file = open(cache_path, "a+")
            cache_file.write("\n")
            cache_file.write("{}\t{}".format(key, val))
            cache_file.close()

    def calculate_score(self, a_x, a_y, a_angle, a_scale, b_x, b_y, b_angle, b_scale):
        """
        This calculates the score of this edge with custom parameter values (to be used by optimizer)
        """        
        # We get the transform matrix (matrix to transform from A to B, as calculated by imreg_dft)
        tvec = QgsPointXY(self.tvec[0],self.tvec[1])
        tvec *= self.imageA.pixel_size * a_scale / DOWNSCALING_FACTOR
        edge_matrix = transform_matrix(self.scale, self.angle, tvec.x(), tvec.y())
        # We get the point A transform matrix (matrix to transform from local to A coordinates)
        ptA_matrix = transform_matrix(a_scale, a_angle, a_x, a_y)
        # We compute the A*edge matrix (matrix to get to B coordinates)
        ptA_edge_matrix = ptA_matrix * edge_matrix
        # We get the point B transform matrix (matrix to transform from local to B coordinates)
        ptB_matrix = transform_matrix(b_scale, b_angle, b_x, b_y)

        # Now we compare how well ptA_edge_matrix and ptB_matrix are similar using two sample points (in homogeneous coordinates)       
        sample1 = [[10],[0],[1]]
        sample1_a = ptA_matrix * sample1
        sample1_b = ptB_matrix * sample1
        sample1_ab = ptA_edge_matrix * sample1

        sample2 = [[0],[10],[1]]
        sample2_a = ptA_matrix * sample2
        sample2_b = ptB_matrix * sample2
        sample2_ab = ptA_edge_matrix * sample2

        # The score is the distance between the two transformed points (summed)
        score1 = math.sqrt((sample1_b.item(0)-sample1_ab.item(0))**2 + (sample1_b.item(1)-sample1_ab.item(1))**2)
        score2 = math.sqrt((sample2_b.item(0)-sample2_ab.item(0))**2 + (sample2_b.item(1)-sample2_ab.item(1))**2)

        return score1 + score2

    def __repr__(self):
        return "Edge {}-{}".format(self.imageA.name(), self.imageB.name())
