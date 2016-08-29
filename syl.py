import urllib.parse
import urllib.request
import os, re, sys

# Бета 0.1
# TODO: Починить хентай-баг (отсутствие множественного выкачивания пикч)
# TODO: Починить баг с неправильной обрезкой имени
# TODO: Разбить на функции и классы

# Парсинг ссылки
LINK = str(sys.argv[1])
url = urllib.parse.urlparse(LINK)
site = url.scheme + '://' + url.netloc
print("Открыт сайт: ", site)
print("Ваша ссылка: ", LINK, "\n")

# Создание директории под аниме-пикчи
BACKUP_DIRECTORY = "loli_backup"
try:
    os.mkdir(BACKUP_DIRECTORY, 777)
    os.chdir(BACKUP_DIRECTORY)
except FileExistsError:
    print("Папка уже создана!")
    os.chdir(BACKUP_DIRECTORY)
print("Переход в", os.getcwd(), '\n')

# Получение списка ссылок на посты с пикчами из html-кода
posts_html = re.findall('/posts/\d*\d', str((urllib.request.urlopen(LINK)).read()))
posts_links = []

for post in posts_html:

    # Обработка поста
    print("Пост", site + post, "открыт.")
    original_pic = re.findall('data-large-file-url="[_,\w, /]+.\w+.jpg"', str((urllib.request.urlopen(site+post)).read()))
    print(original_pic)
    print("Обнаружено", len(original_pic), "изображений. Будут скачаны все [beta: почти все].")
    pic = original_pic[0][21:len(original_pic[0])-1]
    image_name = pic[13:]
    print("Ссылка:", site+pic)

    # Скачивание изображения(й)
    image_link = urllib.request.urlopen(site+pic)
    image_file = open(image_name, 'wb')
    image_file.write(image_link.read())
    image_file.close()
    print("Изображение", image_name, "скачано!\n")
