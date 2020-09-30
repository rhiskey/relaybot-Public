
from PIL import Image


imageFile = "big_img.jpg"

# def resizeToPost(imageFile):
    #imageFile = 'big_img.jpg'
    # adjust width and height to your needs
max_width = 1080
max_height = 1080

img = Image.open(imageFile)

heigth = img.height
width = img.width
resize_ratio_w = max_width/width
resize_ratio_h = max_height/heigth

new_img = img.resize((width*resize_ratio_w,height*resize_ratio_h))
new_img.save("big_resized.jpg", "JPEG", optimize=True)

    #return resized_image
