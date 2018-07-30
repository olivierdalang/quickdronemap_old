import math, os, datetime, tempfile, json

from PIL import Image as PILImage
from PIL import ExifTags as PILExifTags

import numpy as np

from scipy.optimize import least_squares
import scipy as sp
import scipy.misc
import imreg_dft as ird

from qgis.core import (QgsPointXY,QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsRasterTransparency,QgsProject)
from qgis.gui import (QgsRubberBand)

from qgis.core import QgsWkbTypes

from PyQt5.QtCore import Qt

from .utils import absolute_angle_difference, gps_tag_to_decimal_degress, resized, transform_matrix


# Threshold over which images are not considered being in the same sequence (in radians)
ANGLE_THRESHOLD = 15.0 / 180.0 * math.pi # 15°
# Threshold over which images are not considered being in the same sequence (in seconds)
TIME_THRESHOLD = 20
# Similarity will be computed on downscaled images. The lower the factor, the fastest the process
DOWNSCALING_FACTOR = 0.05


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

        # print("1/ Instantiating all images...")
        # for root, dirs, files in os.walk(self.folder):
        #     for file in files:
        #         if file.endswith(".jpg") or file.endswith(".JPG"):
        #             image_path = os.path.join(root, file)
        #             image = Image(self, image_path, len(self.images))
        #             self.images.append(image)
        # for i in list(range(327,332))+list(range(361,366))+list(range(395,400)):
        for i in list(range(327,329))+list(range(365,366)):
            path = "C:\\Users\\Olivier\\Dropbox\\Affaires\\SPC\\Sources\\quickdronemap\\test\\data\\DJI_{0:04d}.JPG".format(i)
            self.images.append(Image(self, path, len(self.images)))


        print("2/ Loading image attributes and parsing exif tags...")
        for image in self.images:
            image.set_attributes()

        print("5/ Building image sequences...")
        self.images.sort(key=lambda x: x.timestamp)
        for i in range(len(self.images)):

            prev_image = self.images[i-1] if i>0 else None
            image = self.images[i]
            next_image = self.images[i+1] if i<len(self.images)-1 else None

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


        print("6/ Deriving orientation from image sequence")
        for image in self.images:
            # if the direction wasn't set in the Exif tags, we derive it from the image sequences
            if image.angle is None:
                img_a = image.prev_image or image 
                img_b = image.next_image or image 

                image.angle = math.atan2(img_b.point.x()-img_a.point.x(),-img_b.point.y()+img_a.point.y())


        print("7/ Building image neighbourhood graph...")
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

        print("8/ Computing similarities")
        for edge in self.edges:
            edge.compute_transform()


        # print("9/ Optimizing")
        # initial_guess = []
        # for image in self.images:
        #     initial_guess.append(float(image.point.x()))
        #     initial_guess.append(float(image.point.y()))
        #     initial_guess.append(image.angle)
        #     initial_guess.append(image.scale)
        # initial_guess_np = np.array(initial_guess, dtype=float)

        # for image in self.images:
        #     image.matrix = transform_matrix(image.scale, image.angle, image.tvec)
        # for edge in self.edges:
        #     edge.matrix = transform_matrix(image.scale, image.angle, image.tvec)

        # def calculate_fitness(x):

        #     total_fitness = 0
        #     for edge in self.edges:

        #         px_a = x[edge.imageA.id*4+0]
        #         py_a = x[edge.imageA.id*4+1]
        #         pa_a = x[edge.imageA.id*4+2]
        #         ps_a = x[edge.imageA.id*4+3]

        #         px_b = x[edge.imageB.id*4+0]
        #         py_b = x[edge.imageB.id*4+1]
        #         pa_b = x[edge.imageB.id*4+2]
        #         ps_b = x[edge.imageB.id*4+3]


        #     total_fitness = 0
        #     for i,image in enumerate(self.images):

        #         px = x[i*4+0]
        #         py = x[i*4+1]
        #         pa = x[i*4+2]
        #         ps = x[i*4+3]

        #         fitness = 0
        #         for edge in image.edges:
        #             reverse = image is edge.imageA
        #             other = edge.other(image)

        #             # print("DOING IMAGE {} TO {}".format(image, other))

        #             d_angle = edge.angle
        #             if reverse:
        #                 d_angle *= -1.0
        #             target_angle = other.angle + d_angle
        #             fitness += absolute_angle_difference(target_angle, pa)

        #             # f_scale = edge.scale
        #             # if reverse:
        #             #     f_scale = 1.0/f_scale
        #             # target_psize = other.psize * f_scale
        #             # fitness += abs(target_psize/ps)*10.0
                    
        #             d_point = QgsPointXY(edge.tvec[0],edge.tvec[1])
        #             if reverse:
        #                 d_point *= -1.0
        #             d_point = d_point.rotated(other.angle)
        #             d_point *= other.pixel_size*other.scale/DOWNSCALING_FACTOR
        #             target_point = other.point + d_point

        #             fitness += (target_point - QgsPointXY(px,py)).dist()
        #         total_fitness += fitness/len(image.edges)
        #     return total_fitness
    
        # res_1 = least_squares(calculate_fitness, initial_guess_np)
        
        # print("Initial guess")
        # print(initial_guess_np)
        # print("Results")
        # print(res_1.x)

        # for i,image in enumerate(self.images):
        #     px = res_1.x[i*4+0]
        #     py = res_1.x[i*4+1]
        #     pa = res_1.x[i*4+2]
        #     ps = res_1.x[i*4+3]
        #     self.images[i].point = QgsPointXY(px, py)
        #     self.images[i].angle = pa
        #     self.images[i].psize = ps


        print("8/ Adjusting positions PROTOTYPE")
        for image in self.images[0:1]:

            target_angles = []
            target_psizes = []
            target_points = []

            error = 0.0

            for edge in image.edges[0:1]:

                reverse = image is edge.imageA
                other = edge.other(image)

                d_angle = edge.angle
                if reverse:
                    d_angle *= -1.0
                image.target_angle = other.angle + d_angle

                f_scale = edge.scale
                if reverse:
                    f_scale = 1.0/f_scale
                image.target_scale = other.scale * f_scale

                d_point = QgsPointXY(edge.tvec[0],edge.tvec[1])
                if reverse:
                    d_point *= -1.0
                d_point = d_point.rotated(other.angle)
                d_point *= other.pixel_size/DOWNSCALING_FACTOR
                image.target_point = other.point + d_point

        for image in self.images[0:1]:
            image.angle = image.target_angle
            image.scale = image.target_scale
            image.point = image.target_point

        
        print("8/ Computing all transforms...")
        for image in self.images:
            image.update_transform()

        print("9/ Creating debug jsons files")
        img_data = {"type": "FeatureCollection","features": []}
        for image in self.images:
            coords = [image.lon, image.lat]
            props = {k:v for (k,v) in vars(image).items()}
            feature = {"type": "Feature","properties": props,"geometry": {"type": "Point","coordinates": coords}}
            img_data['features'].append(feature)
        
        img_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.geojson', delete=False)
        json.dump(img_data, img_file, default=lambda o: str(o))
        img_file.close()
        layer = self.iface.addVectorLayer(img_file.name,"[DEBUG] Geolocated images","ogr")
        layer.loadNamedStyle(os.path.join(os.path.dirname(os.path.realpath(__file__)),'debug_geolocated_style.qml'))
        layer.setCrs(self.crs_src)

        edg_data = {"type": "FeatureCollection","features": []}
        for edge in self.edges:
            coords = [[edge.imageA.lon, edge.imageA.lat],[edge.imageB.lon, edge.imageB.lat]]
            props = {k:v for (k,v) in vars(edge).items()}
            feature = {"type": "Feature","properties": props,"geometry": {"type": "LineString","coordinates": coords}}
            edg_data['features'].append(feature)
        
        edg_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.geojson', delete=False)
        json.dump(edg_data, edg_file, default=lambda o: str(o))
        edg_file.close()
        layer = self.iface.addVectorLayer(edg_file.name,"[DEBUG] Graph edges","ogr")
        layer.loadNamedStyle(os.path.join(os.path.dirname(os.path.realpath(__file__)),'debug_edges_style.qml'))
        layer.setCrs(self.crs_src)

    def load_worldfiles(self):
        for image in self.images:
            image.write_worldfile()
            image.load_worldfile(self.iface)

    def load_vrts(self):
        for image in self.images:
            image.write_vrt()
            image.load_vrt(self.iface)


class Image():

    def __init__(self, drone_map, path, id):
        self.drone_map = drone_map
        # Image properties
        self.id = id
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
        
    def load_worldfile(self, iface):
        # Add to project
        layer = iface.addRasterLayer(self.path,"WORLD-{}".format(self))
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

    def load_vrt(self, iface):
        # Add to project
        layer = iface.addRasterLayer(self.path+".vrt","VRT-{}".format(self))
        layer.setCrs(self.drone_map.crs_dest)
        
        # We make black pixels transparent to remove the rotated frame, not ideal if there are actually black pixels in the image
        rasterTransparency = layer.renderer().rasterTransparency()
        pixel = QgsRasterTransparency.TransparentThreeValuePixel()
        pixel.red, pixel.green, pixel.blue, pixel.percentTransparent = 0,0,0,100
        rasterTransparency.setTransparentThreeValuePixelList([pixel])

    def __repr__(self):
        return "{} [{}]".format(self.name(), datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S'))

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
        
        cache_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache.json')
        if not os.path.exists(cache_path):
            cache_file = open(cache_path, "w+")
            cache_file.write("{}")
            cache_file.close()

        cache_file = open(cache_path, "r")
        cache = json.load(cache_file)
        cache_file.close()

        try:
            self.tvec = cache[src_img_path][mvg_img_path]['tvec']
            self.angle = cache[src_img_path][mvg_img_path]['angle']
            self.scale = cache[src_img_path][mvg_img_path]['scale']
            self.success = cache[src_img_path][mvg_img_path]['success']
        except KeyError:

            src_data = sp.misc.imread(src_img_path, True)
            mvg_data = sp.misc.imread(mvg_img_path, True)
            result = ird.similarity(src_data, mvg_data)

            self.tvec = result['tvec'][1], -result['tvec'][0] # (Y,X)
            self.angle = result['angle'] / 180.0 * math.pi
            self.scale = result['scale']
            self.success = result['success']

            if src_img_path not in cache:
                cache[src_img_path] = {}
            if mvg_img_path not in cache[src_img_path]:
                cache[src_img_path][mvg_img_path] = {}
            
            cache[src_img_path][mvg_img_path]['tvec'] = self.tvec
            cache[src_img_path][mvg_img_path]['angle'] = self.angle
            cache[src_img_path][mvg_img_path]['scale'] = self.scale
            cache[src_img_path][mvg_img_path]['success'] = self.success
            cache[src_img_path][mvg_img_path]['matrix'] = self.matrix
            cache_file = open(cache_path, "w")
            json.dump(cache, cache_file)
            cache_file.close()

    def transform_matrix():
        s = self.scale
        cosA, sinA = math.cos(self.angle), math.sin(self.angle)
        dx, dy = self.tvec
        mtrx_scale = np.matrix([
            [s, 0, 0],
            [0, s, 0],
            [0, 0, 1],
        ])
        mtrx_rotate = np.matrix([
            [cosA, -sinA, 0],
            [sinA,  cosA, 0],
            [0,     0,    1],
        ])
        mtrx_offset = np.matrix([
            [1,0,dx],
            [0,1,dy],
            [0,0,1 ],
        ]) 
        return mtrx_rotate * mtrx_scale * mtrx_offset