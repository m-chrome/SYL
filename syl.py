import urllib.parse
import urllib.request
import os, re, sys

# Бета 0.2
# TODO: Починить хентай-баг (отсутствие множественного выкачивания пикч)
# TODO: Разбить на функции и классы

def take_file_name(server_name):
    """Задает имя для изображения, согласно хранимому на сервере"""
    name_end = i = len(server_name)-1
    while server_name[i] != '/':
        i -= 1
    name_begin = i+1
    return server_name[name_begin: name_end]

def take_full_file_name(html_tag):
    """Извлекает полное имя файла из html-тэга"""
    i = 0
    name_end = len(html_tag)
    while html_tag[i] != "\"":
        i += 1
    return html_tag[i+1:name_end-1]

# Парсинг ссылки
LINK = sys.argv[1]
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
    original_pic = re.findall('data-large-file-url="/[_,\w, /]+.\w+\.jpg"', str((urllib.request.urlopen(site+post)).read()))
    print(original_pic)
    print("Обнаружено", len(original_pic), "изображений. Будут скачаны все [beta: почти все].")
    image_full_name = take_full_file_name(original_pic[0])
    image_name = take_file_name(original_pic[0])
    print("Ссылка:", site+image_full_name)

    # Скачивание изображения(й)
    image_link = urllib.request.urlopen(site+image_full_name)
    image_file = open(image_name, 'wb')
    image_file.write(image_link.read())
    image_file.close()
    print("Изображение", image_name, "скачано!\n")
