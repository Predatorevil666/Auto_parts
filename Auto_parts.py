


import requests
# import csv
from bs4 import BeautifulSoup



# - Масляный фильтр hyundai solaris  (пример для ввода)

def search_parts(url):    # - функция  получения ссылки фирм производителей на запрос конкретной автозапчасти
    # r = requests.get(url)
    # if r.ok:
    article = '+'.join(input('Введите название автозапчасти или ее каталожный номер с маркой автомобиля : ').split())
    link = url.format(article=article)
    # print(link)
    response = requests.get(link).text
    # print(response)
    return response
#     # else:
#     #     print(r.status_code)
#
#
#
def get_page_company(html):           # - функция нахождения ссылки наличия наименований на выбранный бренд автозапчасти
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='alt-step-table').find('tbody').find_all('tr')
    link_brand = []
    for tr in trs:
        tds = tr.find_all('td')
        name_comp = tr.find('td', class_='alt-step-table__cell alt-step-table__cell_type_brand').text.strip()
        # print(name_comp)
        link_brand.append(name_comp)
        # print(link_brand)
        if 'KIA / HYUNDAI / MOBIS' in link_brand:        # - для автоматического выбора только фирмы оригинала нужной марки
            link_comp = 'https://ryazan.1001z.ru' + tds[2].find('a').get('href')
            print(link_comp)
            return link_comp
        else:
            print('Такой фирмы нет !')
            # break
            # print(link_brand.index())
        # try:

        #      # link_comp = 'https://ryazan.1001z.ru' + tds[2].find('a').get('href')
        #     # link_brand.append(link_comp)
        # except:
        #     link = ''
        #     print(link)

    # print(link_brand[6])

def get_html_page_pars(link_comp):        # - функция получения html кода страницы парсинга
    r = requests.get(link_comp)
    if r.ok:
        return r.text
    print(r.status_code)


def auto_pars(html):   # - функция парсинга нужных тегов
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='web_ar_datagrid search-results search-results_type_groups').find('tbody').find_all('tr')
    print(len(trs))



# def write_csv(data):    #  - функция записи в csv файл
#     with open('auto_parts.csv', 'a', encoding='utf-8') as file:
#
#         fields = ['Производитель, код товара', 'Рейтинг', 'Срок доставки', 'Местоположение товара', 'Наличие', 'Цена']
#         writer = csv.DictWriter(file, fields, delimiter=';')
#         writer.writeheader()
#         writer.writerow()
#         pass



def main():
    url = 'https://ryazan.1001z.ru/search.html?article={article}&brand=&st=groups&term=0&chk_smode=A&smode=A&sort___search_results_by=final_price&smart_search=1'
    enter_parts = search_parts(url)
    avail_parts = get_page_company(enter_parts)
    url_2 = get_html_page_pars(avail_parts)
    auto_parts = auto_pars(url_2)
    # data = write_csv(auto_parts)


if __name__ == "__main__":
    main()

    # url_2 = 'https://ryazan.1001z.ru/search.html?article=%D0%9C%D0%90%D0%A1%D0%9B%D0%AF%D0%9D%D0%AB%D0%99%D0%A4%D0%98%D0%9B%D0%AC%D0%A2%D0%A0HYUNDAISOLARIS&st=groups&term=0&chk_smode=A&smode=A&sort___search_results_by=final_price&smart_search=1&brand=KIA+%2F+HYUNDAI+%2F+MOBIS'
    # get_html_pars(url_2)









