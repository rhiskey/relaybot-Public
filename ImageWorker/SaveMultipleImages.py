from PIL import Image


def save_from_ram_jpg(photo_list):
    jpg_list_inner = []
    photo_index = 1
    img_name = "img_"
    for url in photo_list:
        filename = img_name+str(photo_index)+".jpg"
        url.save(filename, 'JPEG')
        jpg_list_inner.append(filename)
        photo_index += 1
    return jpg_list_inner
