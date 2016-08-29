from urllib import parse
from urllib import request
import os, re, sys

class Image(object):
    def __init__(self, link, name):
        self.link = link
        self.name = name

    def download(self):
        """Скачивание изображения по ссылке"""
        file = open(self.name, "wb")
        print("Ссылка:", self.link)
        file.write(request.urlopen(self.link).read())
        file.close()
        print("Изображение", self.name, "скачано успешно\n")

def html_parser(link, regexp):
    """Поиск по регулярному выражению regexp в html-коде ссылки на страницу link"""
    return re.findall(regexp, str((request.urlopen(link)).read()))

def create_backup_dir(dirname = "loli_backup"):
    """Создание директории под скачанные изображения"""
    try:
        os.mkdir(dirname, 777)
        os.chdir(dirname)
    except FileExistsError:
        print("Папка уже создана!")
        os.chdir(dirname)
    print("Переход в", os.getcwd(), '\n')

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
url = parse.urlparse(LINK)
site = url.scheme + '://' + url.netloc
print("Открыт сайт: ", site)
print("Ваша ссылка: ", LINK, "\n")

# Создание директории под аниме-пикчи
create_backup_dir()

# Получение списка ссылок на посты с пикчами из html-кода
posts_html = html_parser(LINK, '/posts/\d*\d')

for post in posts_html:
    print("Открыт пост", site + post)
    pics = html_parser(site+post, 'data-large-file-url="/[_,\w, /]+.\w+\.jpg"')
    print("Обнаружено изображений [jpg]:", len(pics))
    for i in pics:
        print("Ресурс:", i)
        image = Image(site+take_full_file_name(i), take_file_name(i))
        image.download()
