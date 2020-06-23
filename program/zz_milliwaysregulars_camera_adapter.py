from picamera import PiCamera
from PIL import Image
from PIL import ImageStat
import os

class CameraAdapter():
    #uses the camera for brightness recorgnition and saves images optional

    def __init__(self):
        #initializing the camera
        self.__camera = PiCamera()
        self.__camera.resolution = 512,512
        self.__photo_number = 0


    def start(self):
        #starting camera preview
        self.__camera.start_preview()


    def end(self):
        #ending camera preview
        self.__camera.stop_preview()


    def brightness(self,save = False):
        #returns brightness and optional filepath

        #naming imagepath
        image_path = "image"  + str(self.__photo_number) + ".jpg"
        #captures image and saves image to file
        self.__camera.capture(image_path)
        #opens imagefile and converts image to greyscale
        image = Image.open(image_path).convert("L")
        #calculates average pixel level in the image
        image_stat = ImageStat.Stat(image)
        brightness = image_stat.mean[0]

        # keeps or removes imagefile
        if save:
            self.__photo_number += 1
        else:
            os.remove(image_path)
            image_path = ""

        return brightness, image_path
