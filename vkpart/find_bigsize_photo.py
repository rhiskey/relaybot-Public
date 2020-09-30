def findBigPhoto(response):
    dict = list(response)[10]
    subdict1 = dict[1]
    subdict2 = subdict1[0]
    resp1=list(subdict2.values())
    # print(resp1)
    resp2=resp1[1]
    resp3 = resp2['sizes']

    bigsize_height = 0
    bigsize_width = 0
    bigsize_url = ""

    for item in resp3:
        # print(item)
        # print(item['url'],"ширина и высота:",item['width'],"x",item['height'])
        # print()

        # Нахождение самой большой фотки
        width = item['width']
        height = item['height']

        if height> bigsize_height or width>bigsize_width:
            bigsize_height=height
            bigsize_width=width
            bigsize_url = item['url']
        # print("Самое большое фото: ", bigsize_width, bigsize_height)
        # # Вернуть ссылку на это фото
        # print("Его ссылка: ", bigsize_url)
    return bigsize_url

# findBigPhoto(response_to)
