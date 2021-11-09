import requests
import csv
from bs4 import BeautifulSoup



session = requests.Session()


def load_page(url):  # - функция  получения ссылки фирм производителей на запрос конкретной автозапчасти
    article = '+'.join(input('Введите название автозапчасти или ее каталожный номер с маркой автомобиля : ').split())
    link = url.format(article=article)
    response = session.get(link)
    if response.ok:
        return response.text
    print(response.status_code)


def parse_link_company(enter_parts):  # - функция получения ссылки на оригинальный бренд выбранного автомобиля
    soup = BeautifulSoup(enter_parts, 'lxml')
    trs = soup.find('table', class_='alt-step-table').find('tbody').find_all('tr')
    brand = 'KIA / HYUNDAI / MOBIS'
    for tr in trs:
        tds = tr.find_all('td')
        name_comp = tr.find('td', class_='alt-step-table__cell alt-step-table__cell_type_brand').text.strip()
        if name_comp == brand:  # - для автоматического выбора только фирмы оригинала нужной марки
            link_comp = 'https://ryazan.1001z.ru' + tds[2].find('a').get('href')
            return link_comp
    print('Такой фирмы нет !')
    return None


def parse_parts(get_link):  # - функция парсинга наличия вариантов искомой запчасти
    response_2 = session.get(get_link).text
    soup = BeautifulSoup(response_2, 'lxml')
    trs = soup.select('tr[class^="search-row"]')
    data = []
    for tr in trs:
        brand = tr.select('span[class^="search-results__info-text"]')  # - Производитель
        if not brand:
            continue
        else:
            brand = brand[0].text.strip()
            # print(brand)

        number_parts = tr.select('div[class="search-results__article_group"]')   # - Код товара
        if not number_parts:
            continue
        else:
            number_parts = number_parts[0].text.strip()
            # print(number_parts)

        name_parts = tr.select('td[class="search-col search-col__spare_info"]')  # - Наименование товара
        if not name_parts:
            continue
        else:
            name_parts = name_parts[0].text.strip()
            # print(name_parts)

        rating = tr.select('span[class="column-val__count"]')  # -  Рейтинг
        rating = rating[0].text.strip()
        # print(rating)

        delivery_time = tr.select('div[class^="search-col__term-wrapper"]')   # - Срок доставки
        delivery_time = delivery_time[0].text.strip()
        # print(delivery_time)

        parts_location = tr.select('td[class="search-col search-col__destination_display"]')  # - Местоположение товара
        parts_location = parts_location[0].text.strip()
        # print(parts_location)

        availability_parts = tr.select('td[class="search-col search-col__remains"]')    # - Наличие
        availability_parts = availability_parts[0].text.strip()
        # print(availability_parts)

        price = tr.select('td[class="search-col search-col__final_price"]')   # - Цена
        price = price[0].text.strip()
        # print(price)

        data.append({'Производитель': brand, 'Код товара': number_parts, 'Наименование товара': name_parts,
                     'Рейтинг': rating, 'Срок доставки': delivery_time, 'Местоположение товара': parts_location,
                     'Наличие': availability_parts, 'Цена': price})
    return data


def writer_csv(auto_parts):  # - функция записи в csv файл
    with open('auto_parts.csv', 'w', newline='', encoding='utf-8') as file:
        fields = ['Производитель', 'Код товара', 'Наименование товара', 'Рейтинг',
                  'Срок доставки', 'Местоположение товара', 'Наличие', 'Цена']
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
        writer.writeheader()
        for i in auto_parts:
            writer.writerow(i)


def main():
    url = 'https://ryazan.1001z.ru/search.html?article={article}&brand=&st=groups&term=0&chk_smode=A&smode=A&sort___search_results_by=final_price&smart_search=1'
    enter_parts = load_page(url)
    get_link = parse_link_company(enter_parts)
    auto_parts = parse_parts(get_link)
    writer_csv(auto_parts)


if __name__ == "__main__":
    main()
