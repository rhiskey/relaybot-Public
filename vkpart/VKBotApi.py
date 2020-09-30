# Авторизация пользователя:
"""
login, password = 'python@vk.com', 'mypassword'
vk_session = vk_api.VkApi(login, password)
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
    return
"""
# Авторизация группы (для групп рекомендуется использовать VkBotLongPoll):
# при передаче token вызывать vk_session.auth не нужно
"""
vk_session = vk_api.VkApi(token='токен с доступом к сообщениям и фото')
"""

""" Пример использования bots longpoll
    https://vk.com/dev/bots_longpoll
"""

# # Обработчики EVENT из VK LongPoll APi
# if event.type == VkBotEventType.MESSAGE_NEW:
#     print('Новое сообщение:')
#
#     print('Для меня от: ', end='')
#
#     print(event.obj.from_id)
#
#     print('Текст:', event.obj.text)
#     print()

# elif event.type == VkBotEventType.MESSAGE_REPLY:
#     print('Новое сообщение:')
#
#     print('От меня для: ', end='')
#
#     print(event.obj.peer_id)
#
#     print('Текст:', event.obj.text)
#     print()
#
# elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
#     print('Печатает ', end='')
#
#     print(event.obj.from_id, end=' ')
#
#     print('для ', end='')
#
#     print(event.obj.to_id)
#     print()
#
# elif event.type == VkBotEventType.GROUP_JOIN:
#     print(event.obj.user_id, end=' ')
#
#     print('Вступил в группу!')
#     print()
#
# elif event.type == VkBotEventType.GROUP_LEAVE:
#     print(event.obj.user_id, end=' ')
#
#     print('Покинул группу!')
#     print()