def find_big_photo(elem):
    photo = elem['photo']
    sizes = photo['sizes']

    bigsize_height = 0
    bigsize_width = 0
    bigsize_url = ""

    for item in sizes:
        # Нахождение самой большой фотки
        width = item['width']
        height = item['height']

        if height > bigsize_height or width > bigsize_width:
            bigsize_height = height
            bigsize_width = width
            bigsize_url = item['url']
    # Вернуть ссылку на это фото
    return bigsize_url
