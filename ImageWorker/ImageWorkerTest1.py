from PIL import Image
from PIL import ImageFilter



def resizeImgInsta(imgOrig,useBGBlurInsteadOfWhiteBG=False,fotoSeries=False):
    #from PIL import Image
    #from PIL import ImageFilter
    MAX_INSTA_IMG_PortSide_HEIGHT = 1350;
    MAX_INSTA_IMG_LandSide_SIZE=1080;
    MIN_INSTA_ING_LANDSIZE_HEIGHT=608;
    BG_COLOR=(255,255,255);
    MIN_INSTA_IMG_PORT_RATIO=4/5;
    MAX_INSTA_IMG_LAND_RATIO=1.91;
    #first we need to finde biggest side to calculate scale
    #assert isinstance(imgOrig.convert, object)
    imgOrig=imgOrig.convert('RGB')
    if imgOrig.height>imgOrig.width:
        bgHeight=MAX_INSTA_IMG_PortSide_HEIGHT
        if (imgOrig.height*MAX_INSTA_IMG_LandSide_SIZE/MAX_INSTA_IMG_PortSide_HEIGHT>imgOrig.width):
            scaleRatio = MAX_INSTA_IMG_PortSide_HEIGHT / (imgOrig.height)
        else:
            scaleRatio = MAX_INSTA_IMG_LandSide_SIZE / imgOrig.width
    else:
        bgHeight=MIN_INSTA_ING_LANDSIZE_HEIGHT
        scaleRatio = MAX_INSTA_IMG_LandSide_SIZE / imgOrig.width
    #scaling))
    (img_width, img_height) = (int(imgOrig.width * scaleRatio), int(imgOrig.height * scaleRatio))
    imgOut=imgOrig.resize((img_width,img_height),Image.BICUBIC)#BICUBIC  BILINEAR
    #if scale ratio is to big for Insta
    ratio=(imgOut.width/imgOut.height)
    if  (ratio<MIN_INSTA_IMG_PORT_RATIO) or (ratio>MAX_INSTA_IMG_LAND_RATIO):# or (fotoSeries==True):
        imgBG = Image.new('RGB', (MAX_INSTA_IMG_LandSide_SIZE, bgHeight), BG_COLOR)
        #whana play Uncharted? some Blur here for BG)))
        if (useBGBlurInsteadOfWhiteBG==True):
            imgBG=imgOrig.resize((MAX_INSTA_IMG_LandSide_SIZE,MAX_INSTA_IMG_PortSide_HEIGHT),Image.BILINEAR)
            xCornerOnBlur=int((imgBG.width - MAX_INSTA_IMG_LandSide_SIZE) / 2)
            yCornerOnBlur=int((imgBG.height-bgHeight)/2)
            imgBG=imgBG.crop((xCornerOnBlur,yCornerOnBlur,imgBG.width-xCornerOnBlur,imgBG.height-yCornerOnBlur))
            imgBG=imgBG.filter(ImageFilter.GaussianBlur(10))
        #Put picture on BG
        (xCornerOnBG,yCornerOnBG)=(int((MAX_INSTA_IMG_LandSide_SIZE-imgOut.width)/2),int((bgHeight-imgOut.height)/2))
        imgOut=imgBG.paste(imgOut,(xCornerOnBG,yCornerOnBG))
        #backGround.save('sid.jpg', 'jpeg')
    return(imgOut)

def resizeLstImgInsta(lstImgOrig,useBGBlurInsteadOfWhiteBG=False):
    lstImgNew=[]
    for imgOrig in lstImgOrig:
        lstImgNew.append(resizeImgInsta((imgOrig), useBGBlurInsteadOfWhiteBG, True))
    return lstImgNew

def resizeImgDisc(img):

    return img

def downloadImg(url='https://www.lg.com/bg/img/news/LG_34UC97_MULTISCREEN.jpg'):#https://www.fresher.ru/images7/vertikalnye-panoramnye-fotografii/2.jpg'):#'https://sun9-59.userapi.com/UkTMbOBwZuGketC_uTm9POa4338FRptGpnOzQw/9r5QJElnq0M.jpg'):
    #from PIL import Image
    import requests

    try:
        resp = requests.get(url, stream=True).raw
    except requests.exceptions.RequestException as e:
        print("Error: %s" % e)

    try:
        img = Image.open(resp)
    except IOError:
        print("Unable to open image")

    try:
        img.load()  #LazyDownLoad -> we need NOW
    except Exception as e:
        print("Unable to download image %s" % e)
        
    #img=resizeImgInsta(img,True)#onlyTest
    #commment after debug
    #img.save('sid.jpg', 'jpeg')
    return(img)


if __name__ == '__main__':
     downloadImg()
