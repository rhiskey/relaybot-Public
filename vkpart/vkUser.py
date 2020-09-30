import vk_api

import botconfig as cfg
from vkpart.find_bisize_photoDOM import find_big_photo as findBig


def get_last_post():
    login = cfg.vk['login']
    password = cfg.vk['pass']
    # groupId = cfg.vk['groupid']
    public_id = cfg.vk['publId']

    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    # tools = vk_api.VkTools(vk_session)

    """ VkTools.get_all позволяет получить все объекты со всех страниц.
        Соответственно get_all используется только если метод принимает
        параметры: count и offset.
        Например может использоваться для получения всех постов стены,
        всех диалогов, всех сообщений, etc.
        При использовании get_all сокращается количество запросов к API
        за счет метода execute в 25 раз.
        Например за раз со стены можно получить 100 * 25 = 2500, где
        100 - максимальное количество постов, которое можно получить за один
        запрос (обычно написано на странице с описанием метода)
    """

    # Выделение списка для URL вложений
    attachments = []
    # Очистка если заполнен
    attachments.clear()

    # Получаем последний опубликованный пост
    vk = vk_session.get_api()
    response = vk.wall.get(owner_id=public_id, count=1)  # Используем метод wall.get

    if response['items']:
        items = response['items'][0]
        print("Ответ из ВК: ")
        print(response['items'][0])
        try:
            # Только для постов от имени сообщества
            if items['attachments']:
                atts = items['attachments']
                for elem in atts:
                    # Формируем список картинок
                    if elem['type'] == "photo":
                        image_big_url = findBig(elem)
                        # Добавить каждую картинку в список, самые большие размеры
                        attachments.append(image_big_url)

                    # if elem['type'] == "video":
                    #     # Получение ссылки на видео
                    #

            # # Если репост
            # if items['copy_history']:
            #     repost = items['copy_history']
            #     atts = repost['attachments']
            #     print(atts[0])

        except Exception as e:
            print("Error: %s" % e)
    print("После парсинга: ")
    print(attachments)
    return attachments


if __name__ == '__main__':
    get_last_post()
