__author__ = "legendax24"
__version__ = "1.1"
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm
import requests


def get_query_settings():
    img_sizes = {"Large": "isz:l",
                 "Medium": "isz:m", 
                 "Icon": 'isz:i'
                }

    print('\nРазмер картинок:\n0. Любой\n1. Большой\n2. Средний\n3. Значок')
    size_num = input('(Оставить пусто или 0 чтобы пропустить)\nНомер: ')
    if size_num == '0' or size_num == '':
        img_size = None
    else:
        img_size = list(img_sizes.values())[int(size_num)-1]


    aspects_ratio = {"Tall": "iar:t",
                     "Square": "iar:s",
                     "Wide": "iar:w", 
                     "Panoramic": "iar:xw"
                    }

    print('\nФорма картинок:\n0. Любой\n1. Узкий(вертикальный)\n2. Квадрат\n3. Широкий(горизонтальный)\n4. Панорама')
    ratio_num = input('(Оставить пусто или 0 чтобы пропустить)\nНомер: ')
    if ratio_num == '0' or ratio_num == '':
        aspect_ratio = None
    else:
        aspect_ratio = list(aspects_ratio.values())[int(ratio_num)-1]


    img_colours = {"Full colour": "ic:color",
                   "Black&White": "ic:gray", 
                   "Transparent": "ic:trans"
                  }

    print('\nФильтр цвета картинок:\n0. Любой\n1. Цветные\n2. Черно-белые\n3. Прозрачные')
    colour_num = input('(Оставить пусто или 0 чтобы пропустить)\nНомер: ')
    if colour_num == '0' or colour_num == '':
        img_colour = None
    else:
        img_colour = list(img_colours.values())[int(colour_num)-1]


    img_types = {"Face": "itp:face",
                 "Photo": "itp:photo",
                 "Clip Art": "itp:clipart",
                 "Line Drawing": "itp:lineart",
                 "Animated(gif)": "itp:animated"
                }

    print('\nТип картинок:\n0. Любой\n1. Портреты(лица)\n2. Фотографии\n3. Клип-арт\n4. Черно-белые рисунки\n5. Анимированные(гиф)')
    type_num = input('(Оставить пусто или 0 чтобы пропустить)\nНомер: ')
    if type_num == '0' or type_num == '':
        img_type = None
    else:
        img_type = list(img_types.values())[int(type_num)-1]


    file_types = {"JPG": "ift:jpg",
                  "GIF": "ift:gif",
                  "PNG": "ift:png",
                  "BMP": "ift:bmp",
                  "SVG": "ift:svg",
                  "WEBP": "ift:webp",
                  "ICO": "ift:ico",
                  "RAW": "ift:raw"
                 } 

    print('\nТип файла картинок:\n0. Любой\n1. JPG\n2. GIF\n3. PNG\n4. BMP\n5. SVG\n6. WEBP\n7. ICO\n8. RAW')
    file_num = input('(Оставить пусто или 0 чтобы пропустить)\nНомер: ')
    if file_num == '0' or file_num == '':
        file_type = None
    else:
        file_type = list(file_types.values())[int(file_num)-1]


    usage_rights = {"Free to use or share": "sur:f",
                    "Free to use or share, even commercially": "sur:fc",
                    "Free to use share or modify": "sur:fm",
                    "Free to use, share or modify, even commercially": "sur:fmc"
                   }

    print('''\nПрава на использование картинок:\n0. Любой\n1. С лицензией на использование в некоммерческих целях
2. С лицензией на использование в коммерческих целях\n3. С лицензией на использование и изменение в некоммерческих целях
4. С лицензией на использование и изменение в коммерческих целях''')

    right_num = input('(Оставить пусто или 0 чтобы пропустить)\nНомер: ')
    if right_num == '0' or right_num == '':
        usage_right = None
    else:
        usage_right = list(usage_rights.values())[int(right_num)-1]

    return [img_size, aspect_ratio, img_colour, img_type, file_type, usage_right]


def create_urls():
    query = input('Введите запрос: ')
    url = f"https://www.google.com/search?q={query}&tbm=isch&tbs="
    query_settings = get_query_settings()
    query_settings = list(filter(None, query_settings))
    if len(query_settings) == 0:
            url += "itp"
    else:
        for num, setting in enumerate(query_settings):
            if num == 0:
                url += setting
            else:
                url += f",{setting}"

    urls = []
    img_num = int(input('\nКол-во картинок: '))
    for i in range(1, img_num//14+2):
        urls.append(f"{url}&start={14*i}")

    return urls, img_num


def get_img_links():
    urls, img_num = create_urls()

    img_links = []
    for url in tqdm(urls, desc="Парсинг ссылок", bar_format="{l_bar}{bar}| {elapsed}<{remaining}"):
        response = requests.get(url, headers={'User-Agent': "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"})
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        raw_img_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['image'])
        raw_img_links = [link.attrs['href'] for link in raw_img_links]

        for link in raw_img_links:
            img_links.append(link.split('/imgres?imgurl=')[1].split('&imgrefurl')[0])

    return img_links[:img_num]


def download_images():
    img_links = get_img_links()
    choice = input('\nВыводить ссылки файлов?(д/н): ')

    skipped_urls = []
    errors = 0
    for num, img_link in enumerate(img_links):
        if choice == 'д':
            print(f'Ссылка файла #{num+1}:', img_link)

        try:
            response = requests.get(img_link, headers={'User-Agent': UserAgent().chrome})
            filename = img_link.split('/')[-1]
            with open(filename, "wb") as out:
                out.write(response.content)
                print(f'Завершенный файл #{num+1} ====>', filename)
        except:
            print(f'Пропускаю ссылку #{num+1}:', img_link)
            skipped_urls.append(f'#{num+1} {img_link}')
            errors += 1
            pass

    print('\n\nВсего ошибок: ', errors)
    print('\nПропущенные ссылки:')
    for skipped_url in skipped_urls:
        print(skipped_url)

    input('\nНажмите Enter чтобы выйти: ')


if __name__ == "__main__":
    download_images()

