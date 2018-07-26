import math, os, datetime

from PIL import Image as PILImage
from PIL import ExifTags as PILExifTags

from qgis.core import (QgsPointXY,QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsRasterTransparency,QgsProject)
from qgis.gui import (QgsRubberBand)

from qgis.core import QgsWkbTypes

from PyQt5.QtCore import Qt

from .utils import absolute_angle_difference, gps_tag_to_decimal_degress

# Threshold over which images are not considered being in the same sequence (in radians)
ANGLE_THRESHOLD = 15.0 / 180.0 * math.pi # 15°
# Threshold over which images are not considered being in the same sequence (in seconds)
TIME_THRESHOLD = 20
# Offset to images loaded
LOAD_LIMIT_OFFSET = 70
# Count of images loaded (None or 0 for no limit)
LOAD_LIMIT_COUNT = 15


class DroneMap():

    def __init__(self, iface, folder):
        self.iface = iface
        self.folder = folder
        self.images = []

    def process(self):
        """
        Main process that go through all images and sets their transformation parameters
        """

        print("1/ Instantiating all images...")
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".JPG"):
                    image_path = os.path.join(root, file)
                    image = Image(self, image_path)
                    self.images.append(image)

        self.images = self.images[LOAD_LIMIT_OFFSET:LOAD_LIMIT_OFFSET+LOAD_LIMIT_COUNT]


        print("2/ Loading image attributes and parsing exif tags...")
        for image in self.images:
            image.set_attributes()

        print("3/ Getting coordinate system...")
        utm_i = str(int(math.floor((self.images[0].lon + 180) / 6 ) % 60) + 1).zfill(2)
        epsg_code = int('326' + utm_i) if (self.images[0].lat >= 0) else int('327' + utm_i)
        self.crs_src = QgsCoordinateReferenceSystem(4326)
        self.crs_dest = QgsCoordinateReferenceSystem(epsg_code)
        self.xform = QgsCoordinateTransform(self.crs_src, self.crs_dest, QgsProject.instance())

        print("4/ Reprojecting...")
        for image in self.images:
            image.reproject()

        print("5/ Building image sequences...")
        self.images.sort(key=lambda x: x.timestamp)
        for i in range(len(self.images)):

            prev_image = self.images[i-1] if i>0 else None
            image = self.images[i]
            next_image = self.images[i+1] if i<len(self.images)-1 else None

            print("Building sequences... Doing image {}".format(image.name()))

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
            if image.direction is None:
                img_a = image.prev_image or image 
                img_b = image.next_image or image 

                image.direction = math.atan2(img_b.point.x()-img_a.point.x(),-img_b.point.y()+img_a.point.y())


        print("7/ Building image neighbourhood graph...")
        # TODO
        
        print("8/ Computing all transforms...")
        for image in self.images:
            image.update_transform()

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
        self.path = path

        # neighbouring attributes
        self.prev_image = None
        self.next_image = None
        self.neighbours_images = []

        # image/tags attributes
        self.width = None
        self.height = None
        self.lat = None 
        self.lon = None 
        self.altitude = None
        self.direction = None
        self.focal = None
        self.timestamp = None

        # point
        self.point = None

        # corrections
        self.d_lat = 0
        self.d_lon = 0
        self.d_altitude = 0
        self.d_direction = 0
        self.d_focal = 0

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

        # Setting the attributes
        self.width, self.height = pil_image.size
        self.lat = lat
        self.lon = lon
        self.point = QgsPointXY(self.lon,self.lat)
        self.altitude = gps_altitude[0] / gps_altitude[1]
        self.direction = float(gps_direction) if gps_direction is not None else None
        self.focal = float(exif_data["FocalLengthIn35mmFilm"])
        self.timestamp = datetime.datetime.strptime(exif_data["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S").timestamp()

    def reproject(self):
        """
        This updates the points according the the droneMap's transformation
        """
        self.point = self.drone_map.xform.transform(QgsPointXY(self.lon,self.lat))

    def update_transform(self):
        """
        This updates the image's transform parameters (in worldfile standards) according to it's attributes
        """
        size_meter = self.altitude * 35.0 / self.focal
        pixel_size = size_meter / float(self.width)

        self.a = pixel_size * math.cos(self.direction)
        self.d = pixel_size * math.sin(self.direction)
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
                    <SourceFilename relativeToVRT="0" shared="0">{path}</SourceFilename><SourceBand>1</SourceBand>
                    <SourceProperties RasterXSize="{width}" RasterYSize="{height}" DataType="Byte" BlockXSize="{width}" BlockYSize="1" />
                    <SourceBand>1</SourceBand>
                    <SrcRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
                    <DstRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
            </SimpleSource></VRTRasterBand>
            <VRTRasterBand dataType="Byte" band="2"><ColorInterp>Green</ColorInterp><SimpleSource>
                    <SourceFilename relativeToVRT="0" shared="0">{path}</SourceFilename><SourceBand>1</SourceBand>
                    <SourceProperties RasterXSize="{width}" RasterYSize="{height}" DataType="Byte" BlockXSize="{width}" BlockYSize="1" />
                    <SourceBand>2</SourceBand>
                    <SrcRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
                    <DstRect xOff="{xoff}" yOff="{yoff}" xSize="{xsize}" ySize="{ysize}" />
            </SimpleSource></VRTRasterBand>
            <VRTRasterBand dataType="Byte" band="3"><ColorInterp>Blue</ColorInterp><SimpleSource>
                    <SourceFilename relativeToVRT="0" shared="0">{path}</SourceFilename><SourceBand>1</SourceBand>
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

    def __str__(self):
        return "{} <{:.4f};{:.4f}> [{}]".format(self.name(), self.lon, self.lat, datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S'))
