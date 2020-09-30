import base64
import io
import json
from os import path

# New Method with save token
from instagram_private_api import Client

from ImageWorker.ImageWorkerTest1 import downloadImg


from PIL import Image
from PIL import ImageFilter
import botconfig as cfg


def insta_api(message, photo_list, user_name, password, hashtag):
    api = Client(user_name, password)
    caption = str(message) + " " + hashtag

    # Generate new credintails or load existing
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "credentials.json"))

    with open(filepath, "r") as read_file:
        data = json.load(read_file)
        print(data)

    # Force api credits (saved)

    api.uuid = data['uuid']
    api.device_id = data['device_id']
    api.ad_id = data['ad_id']
    api.session_id = data['session_id']

    # if len(photo_list) == 1:  # Если пришла 1 фотка в списке

    one_image = photo_list[0]
    print(one_image)

    buf = io.BytesIO()
    one_image.save(buf, format='JPEG')
    byte_im = buf.getvalue()
    print(byte_im)

    size = (one_image.width, one_image.height)
    print(size)

    api.login()
    api.post_photo(byte_im, size, caption)

  