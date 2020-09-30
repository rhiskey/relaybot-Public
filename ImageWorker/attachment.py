from PIL import Image
from PIL import ImageFilter

from InstagramAPI import InstagramAPI
from instagram_private_api import Client, ClientCompatPatch

import io
import requests

class ImageAttachment:
    # class variable shared by all instances
    MAX_I_IMG_PORT_HEIGHT = 1350           # MAX_INSTA_IMG_PortSide_HEIGHT = 1350;
    MAX_I_IMG_LAND_WIDTH = 1080            # MAX_INSTA_IMG_LandSide_SIZE=1080;
    MIN_I_IMG_LAND_HEIGHT=608              # MIN_INSTA_ING_LANDSIZE_HEIGHT=608;
    I_IMG_BG_COLOR_DEFAULT=(255, 255, 255) # BG_COLOR=(255,255,255); #white by default
    MIN_I_IMG_PORT_RATIO= 4 / 5            # MIN_INSTA_IMG_PORT_RATIO=4/5;
    MAX_I_IMG_LAND_RATIO=1.91              # MAX_INSTA_IMG_LAND_RATIO=1.91;
    # Preferences

    USE_BG_BLURE=True                      # useBGBlurInsteadOfWhiteBG
    TEST_WIDE_IMG_URL='https://www.lg.com/bg/img/news/LG_34UC97_MULTISCREEN.jpg'
    TEST_WIDE_IMG_NAME="bride1.jpg"
    
    def __init__(self,url=TEST_WIDE_IMG_URL):
        # instance variable unique to each instan
        self._imageUrl=0
        self.__image=0
        self.__imageDiscord=0
        self.__imageInstagram=0


        if url!=self.TEST_WIDE_IMG_URL:
            self.downloadImgNet(url)



    def loadImgHdd(self,path=TEST_WIDE_IMG_NAME):
        if (path!=self.TEST_WIDE_IMG_NAME):
            self.__image=Image.open(path)

        # resize here on load
        self.__resizeImage()

    def downloadImgNet(self,url):
        self._imageUrl = url
        try:
            resp = requests.get(url, stream=True).raw
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

        try:
            self.__image = Image.open(resp)
        except IOError:
            print("Unable to open image")

        try:
            self.__image.load()  # LazyDownLoad -> we need NOW
        except Exception as e:
            print("Unable to download image %s" % e)

        # resize here on load
        self.__resizeImage()


    def __resizeImage(self):
        self.__image.convert('RGB')
        self.__resizeImgDisc()
        self.__resizeImgInsta()


    def __resizeImgDisc(self):
        self.__imageDiscord=self.__image

    def __resizeImgInsta(self):
        if self.__image.height > self.__image.width:
            bgHeight = self.MAX_I_IMG_PORT_HEIGHT
            if (self.__image.height * self.MAX_I_IMG_LAND_WIDTH / self.MAX_I_IMG_PORT_HEIGHT > imgOrig.width):
                scaleRatio = self.MAX_I_IMG_PORT_HEIGHT / (self.__image.height)
            else:
                scaleRatio = self.MAX_I_IMG_LAND_WIDTH / self.__image.width
        else:
            bgHeight = self.MIN_I_IMG_LAND_HEIGHT
            scaleRatio = self.MAX_I_IMG_LAND_WIDTH / self.__image.width
        # scaling))
        (img_width, img_height) = (int(self.__image.width * scaleRatio), int(self.__image.height * scaleRatio))
        self.__imageInstagram = self.__image.resize((img_width, img_height), Image.BICUBIC)  # BICUBIC  BILINEAR
        # if scale ratio is to big for Insta
        ratio = (self.__imageInstagram.width / self.__imageInstagram.height)
        if (ratio < self.MIN_I_IMG_PORT_RATIO) or (ratio > self.MAX_I_IMG_LAND_RATIO):  # or (fotoSeries==True):
            imgBG = Image.new('RGB', (self.MAX_I_IMG_LAND_WIDTH, bgHeight), self.I_IMG_BG_COLOR_DEFAULT)
            # whana play Uncharted? some Blur here for BackGround)))
            if (self.USE_BG_BLURE == True):
                imgBG = self.__image.resize((self.MAX_I_IMG_LAND_WIDTH, self.MAX_I_IMG_PORT_HEIGHT), Image.BILINEAR)
                xCornerOnBlur = int((imgBG.width - self.MAX_I_IMG_LAND_WIDTH) / 2)
                yCornerOnBlur = int((imgBG.height - bgHeight) / 2)
                imgBG = imgBG.crop(
                    (xCornerOnBlur, yCornerOnBlur, imgBG.width - xCornerOnBlur, imgBG.height - yCornerOnBlur))
                imgBG = imgBG.filter(ImageFilter.GaussianBlur(10))
            # Put picture on BG
            (xCornerOnBG, yCornerOnBG) = (int((self.MAX_I_IMG_LAND_WIDTH - self.__imageInstagram.width) / 2), int((bgHeight - self.__imageInstagram.height) / 2))
            imgBG.paste(self.__imageInstagram, (xCornerOnBG, yCornerOnBG))
            self.__imageInstagram =imgBG

    def saveImage(self):
        self.__image.save("most.jpg", "JPEG")
        self.__imageInstagram.save("mostInsta.jpg", "JPEG")

    def getImage(self):
        return self.__image

    def getImageInstagram(self):
        return self.__imageInstagram

    def getImageDiscord(self):
        return self.__imageDiscord

    def toInstagramBytes(self):
        buf = io.BytesIO()
        self.__imageInstagram.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        return byte_im

    def toInstagramSize(self):
        return (self.__imageInstagram.width, self.__imageInstagram.height)

def main():
    a=ImageAttachment();#'https://wallpaperaccess.com/full/346725.jpg')
    a.loadImgHdd("Bridge.jpg")
    a.saveImage()
    a.getImageInstagram().save("mostBLUR.jpg", "JPEG")
    print (a.toInstagram()[1])
    api.post_photo(a.toInstagram())
   # p.save("mostBLUR.jpg", "JPEG")

if __name__ == '__main__':
     main()