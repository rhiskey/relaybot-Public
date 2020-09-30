# -*- coding: utf-8 -*-
# !/usr/bin/env python

import asyncio
# Потоки
import json
from os import path
from threading import Thread

import discord
import requests
import vk_api
from InstagramAPI import InstagramAPI
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Read Config from Py file
import botconfig as cfg
# Подключение классов
import postClass as PostClass
from ImageWorker.ImageWorkerTest1 import resizeImgInsta, downloadImg
from instapart.toInstagram import insta_photo
from vkpart.vkUser import get_last_post


# Пубикация в дискорд, Реализуем многопоточность
class DiscordPoster(Thread):
    """
    Пример скачивание файла используя многопоточность
    """

    def __init__(self, msg, photo_list, channel_id):
        """Инициализация потока"""
        Thread.__init__(self)
        self.__msg = msg
        self.__photoList = photo_list
        self.__channelId = channel_id

    def run(self):
        """Запуск потока"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        discord_token = cfg.discord['token']

        # Получение канала
        client = discord.Client()
        channel_id = int(self.__channelId)

        my_files = []
        jpg_list = []

        inner_photo_list = self.__photoList

        # Сохраняем фото в .jpg
        photo_index = 1
        img_name = "img_"
        if inner_photo_list is not None:
            for photo in inner_photo_list:
                if photo is not None:
                    filename = img_name + str(photo_index) + ".jpg"
                    photo.save(filename, 'JPEG')
                    jpg_list.append(filename)
                    photo_index += 1

            # Перебрать все картинки из списка в  discord.File(img)
            for img in jpg_list:
                # discord.File(img)
                my_files.append(discord.File(img))
            print(my_files)

        message = self.__msg

        # Корутина
        @client.event
        async def on_ready():

            print('We have logged in as {0.user}'.format(client))
            print(client.user.id)
            print('------')

            channel = client.get_channel(channel_id)

            # asyncio.sleep(delay)
            if my_files is not None:
                await channel.send(str(message), files=my_files)
            else:
                await channel.send(str(message))

        # msg = "%s  - отправлен в канал ID: %s!" % (message, channelId)
        # print(msg)
        client.run(discord_token)
        client.logout()


def main():
    print("Бот успешно запущен!")

    # VKAPI
    session = requests.Session()

    group_token = cfg.vk['grouptoken']
    vk_session = vk_api.VkApi(token=group_token)
    print("Авторизировались в ВК по токену группы")
    group_id = cfg.vk['groupid']
    longpoll = VkBotLongPoll(vk_session, group_id)

    vk = vk_session.get_api()

    login_instagram = cfg.instagram['login_insta']
    pass_instagram = cfg.instagram['pass_insta']
    disc_chan_id = cfg.discord['channel_ID']
    hashtag = cfg.instagram['hashtags']

    # # Подумать, а если нам нужно обновить токен через 90 дней?! А прога запущена и не обновляет, нужно проверять
    # внутри toInstagram

    # # Generate new credintails or load from json file
    # os.system("instapart/savesettings_logincallback.py -u \"\login" -p \"\password" -settings "
    #           "\"credentials.json\" ")

    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "credentials.json"))
    with open(filepath, "r") as read_file:
        json_data = json.load(read_file)
        print("Данные для авторизации Instagram:")
        print(json_data)

    # Объявляем API Instagram
    ig = InstagramAPI(login_instagram, pass_instagram)

    # session. Возможно стоит перенести это под login()
    ig.uuid = json_data['uuid']
    ig.device_id = json_data['device_id']
    ig.ad_id = json_data['ad_id']
    ig.session_id = json_data['session_id']

    # Эти параметры получил после вызова ig.login(), сохранил 1 раз и записал (ХАРДКОДИНГ)
    ig.token = 'token'
    ig.username_id = 'uid'

    if not ig.isLoggedIn:
        print("Авторизируемся в Instagram:")
        ig.login()

    # q = deque() # Очередь

    print("Запускаем LongPoll прослушку")
    # Добавили новый пост в группу ВК
    for event in longpoll.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            print('Новый пост:')
            print('Текст:', event.obj.text)
            print()
            post_text = event.obj.text
            # Объявили списки пустые
            attachments = []
            photo_objects = []

            # Формирование класса ПОСТ, вносим сообщение поста
            post_new = PostClass.Post(post_text)

            # #Получение картинки с поста если она есть
            try:
                attachments.clear()
                photo_objects.clear()
                # Вложения к посту
                attachments = get_last_post()  # Вложения, самые большие URL картинок что нашли

                # Изменяем картинки под инсту и т.д.
                for url in attachments:
                    downloaded = downloadImg(url)
                    # resized = resizeImgInsta(downloaded)
                    photo_objects.append(downloaded)

                # Переносим каждое вложение в класс
                for att in photo_objects:
                    post_new.add_attachment(att)

                # Формируем FIFO очередь, добавляем элемент(пост) в начало очереди. First Inpit First Output = первый
                # вошел первый вышел q.append(post_new) 

                # postInQueue = q.popleft()  # Достали, убрали из очереди, возможно неправльно

                # Список Масштабированных фото
                attachments_ram = post_new.get_attachments()
                print("Список в памяти: ")
                print(attachments_ram)  # [<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1280x720 at
                # 0xD480CD0>]
                # <PIL.Image.Image image mode=RGB size=120x90 at 0xD054E500>] 
                photo_list = []
                try:
                    if attachments_ram is not None:  # если вложение не пустое
                        # Ресазинг
                        for attach in attachments_ram:
                            resized_photo = resizeImgInsta(attach, True, False)
                            photo_list.append(resized_photo)
                        # photo_list = resizeLstImgInsta(attachments_ram, True)
                        print("Список фото после ресайза: ")
                        print(photo_list)
                        # Публикация в инсту  с подписью
                        print("Начинаем публикацию в инсту")
                        insta_photo(post_new.get_text(), photo_list, hashtag, ig)
                except Exception as e:
                    print("Невозможно опубликовать в Instagram: %s" % e)
                # finally:
                    # print("Выход из Instagram, деавторизация: %s" %res)
                    # res = ig.logout()
                    # print("Выход из Instagram, деавторизация: %s" % res)

                # В Discord
                try:
                    print("Начинаем публикацию в Дискорд поста")
                    thread = DiscordPoster(post_new.get_text(), attachments_ram, disc_chan_id)
                    thread.start()
                except Exception as e:
                    print("Невозможно опубликовать в Discord: %s" % e)

                # discPost(post_new.get_text(), photos_RAM, discChanId) #Старый способ прерывается

                # q.popleft() # Удаление элемента(поста) из очереди после публикации

                post_new.__del__()  # Удаляем класс из памяти

            except Exception as e:
                print("Error: %s" % e)

        else:
            print(event.type)
            print()


# # Read and Load YAML Config
# def readYMLConfig():
#     with open("config.yml", 'r') as ymlfile:
#         cfg = yaml.load(ymlfile)
#
#     for section in cfg:
#         print(section)
#     print(cfg['vk'])
#     print(cfg['discord'])
#     print(cfg['instagram'])


if __name__ == '__main__':
    main()
