class Post:
    # конструктор
    def __init__(self, text):
        self.__text = text  # устанавливаем сообщенку
        # if images is None:
        #     image = set()   # this is to avoid possible erros later.
        self.__attachments = [] # устанавливаем картинки в виде списка!

    # деструктор
    def __del__(self):
        print(self.__text, "- пост удален из памяти")

    # # Инкапсуляция
    def add_attachment(self, url):
        self.__attachments.append(url)

    def get_attachments(self):
        return self.__attachments

    def get_text(self):
        return self.__text

    def display_info(self):
        print("Сообщение поста: ", self.__text, "\tВложения: ", self.__attachments)
