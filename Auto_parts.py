


import requests
import csv
from bs4 import BeautifulSoup



# - Масляный фильтр hyundai solaris  (пример для ввода)

session = requests.Session()
def load_page(url):                                                              # - функция  получения ссылки фирм производителей на запрос конкретной автозапчасти
    article = '+'.join(input('Введите название автозапчасти или ее каталожный номер с маркой автомобиля : ').split())
    link = url.format(article=article)
    response = session.get(link).text
    return response




def parse_link_company(html):                                                   # - функция получения ссылки на оригинальный бренд выбранного автомобиля
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='alt-step-table').find('tbody').find_all('tr')
    brand = 'KIA / HYUNDAI / MOBIS'
    for tr in trs:
        tds = tr.find_all('td')
        name_comp = tr.find('td', class_='alt-step-table__cell alt-step-table__cell_type_brand').text.strip()
        if name_comp == brand:                                                  # - для автоматического выбора только фирмы оригинала нужной марки
            link_comp = 'https://ryazan.1001z.ru' + tds[2].find('a').get('href')
            return link_comp
    print('Такой фирмы нет !')
    return None



def parse_parts(link_comp):                                                      # - функция парсинга наличия вариантов искомой запчасти
    response_2 = session.get(link_comp).text
    soup = BeautifulSoup(response_2, 'lxml')
    trs = soup.find('table', class_='web_ar_datagrid search-results search-results_type_groups').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        try:
            brand = tds[1].find('span', class_='search-results__info-text').text.strip()       # - Производитель
            # print(brand)
        except (IndexError, AttributeError):
            brand = ''
        try:
            number_parts = tds[1].find('div', class_='search-results__article_group').text.strip()       # - Код товара
            # print(number_parts)
        except (IndexError, AttributeError):
            number_parts = ''
        try:
            rating = tds[3].find('span', class_='column-val__count').text.strip()       # -  Рейтинг
            # print(rating)
        except (IndexError, AttributeError):
            rating = ''
        try:
            delivery_time = tds[4].find('div', class_='search-col__term-wrapper').text.strip()      # - Срок доставки
            # print(delivery_time)
        except (IndexError, AttributeError):
            delivery_time = ''
        try:
            parts_location = tr.find('td', class_='search-col search-col__destination_display').text.strip()   # - Местоположение товара
            # print(parts_location)
        except (IndexError, AttributeError):
            parts_location = ''
        try:
            availability_parts = tr.find('td', class_='search-col search-col__remains').text.strip()   # - Наличие
            # print(availability_parts)
        except (IndexError, AttributeError):
            availability_parts = ''
        try:
            price = tr.find('td', class_='search-col search-col__final_price').text.strip()   # - Цена
            # print(price)
        except (IndexError, AttributeError):
            price = ''
        data = {'Производитель': brand, 'Код товара': number_parts, 'Рейтинг': rating, 'Срок доставки':  delivery_time,
                'Местоположение товара': parts_location, 'Наличие': availability_parts, 'Цена': price}
        return data


def writer_csv(data):    #  - функция записи в csv файл
    with open('auto_parts.csv', 'w', newline='', encoding='utf-8') as file:
        fields = ['Производитель', 'Код товара', 'Рейтинг', 'Срок доставки', 'Местоположение товара', 'Наличие', 'Цена']
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
        writer.writeheader()
        writer.writerow(data)





def main():
    url = 'https://ryazan.1001z.ru/search.html?article={article}&brand=&st=groups&term=0&chk_smode=A&smode=A&sort___search_results_by=final_price&smart_search=1'
    enter_parts = load_page(url)
    get_link = parse_link_company(enter_parts)
    auto_parts = parse_parts(get_link)
    dic_data = writer_csv(auto_parts)


if __name__ == "__main__":
    main()











