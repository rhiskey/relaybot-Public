from InstagramAPI import InstagramAPI

from ImageWorker.ImageWorkerTest1 import downloadImg
from ImageWorker.SaveMultipleImages import save_from_ram_jpg
from randomSleep import sleep_time

from PIL import Image
from PIL import ImageFilter

# DEBUG
import botconfig as cfg

import json
from os import path

# Для ожидания
minwait = 3
maxwait = 15


# Обновить в фефрале 2020, ввести в терминал: , затем получить через api.login токен и сохранить его
# python instapart/savesettings_logincallback.py -u "login" -p "pass" -settings "kolovanja_credentials.json"

# На вход приходит список картинок в памяти RAM photolist = [<PIL.Image.Image image mode=RGB size=148x129 at
# 0xD9C7770>, <PIL.Image.Image image mode=RGB size=120x90 at 0xD054E500>]
def insta_photo(message, photo_list, hashtag, api):
    # Сохранение картинки из памяти
    resized_img_name = 'big_resized.jpg'
    result = None

    if len(photo_list) == 1:  # Если пришла 1 фотка в списке
        try:
            # Получаем 1ый элемент списка (картинка из памяти) = <PIL.Image.Image image mode=RGB size=148x129 at
            # 0xD9C7770>
            onep = photo_list[0]
            onep.save(resized_img_name, 'JPEG')
        except Exception as ex:
            print("Невозможно сохранить фото: %s" % ex)
        try:

            # Генерируем псевдослучайную задержку
            sleep_time(minwait, maxwait)

            caption = str(message) + " " + hashtag
            result = api.uploadPhoto(resized_img_name, caption=caption)

        except Exception as ex:
            print(ex)

    elif len(photo_list) > 1 and len(
            photo_list) <= 10:  # Если фоток много >=2 , то каждую добавить в карусель в инсту
        # Сохраняем каждый элемент из списка ссылок в качестве картинки
        # список названия и пути фоток
        jpg_list = []
        media = []  # формат для инсты
        att_dict = []  # список словарей картинок

        # Сохранение всех картинок из памяти
        try:
            jpg_list = save_from_ram_jpg(photo_list)
        except Exception as ex:
            print("Невозможно сохранить несколько фото: %s" % ex)

        # Каждую картинку добавляем как словарь
        for jpg in jpg_list:
            # Создаем новый каждый раз
            new = {'type': 'photo', 'file': jpg}
            # Добавляяем в список словарь
            att_dict.append(new)

        # append список словарей в media список
        for elem in att_dict:
            media.append(elem)

        print(media)

        caption_text = str(message) + " " + hashtag

        # Генерируем псевдослучайную задержку
        sleep_time(minwait, maxwait)

        result = api.uploadAlbum(media, caption=caption_text)
        # print("Пост в инстаграм: %s" % result)
    else:
        print("Нельзя залить 0 или больше 10 фоток, как ты смог?!")

    print("Пост в инстаграм: %s" % result)




