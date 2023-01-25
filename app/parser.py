import requests
import logging
from logging.handlers import RotatingFileHandler
from bs4 import BeautifulSoup
import json

# from app import config
### For the docker container we have to import it like this
import config


class Shop:
    def __init__(self):
        self.session = requests.Session()

    def start(self):
        logging.info(f"shop.kz -  Parser START")
        all_raw_items = []
        for category, url in config.CATEGORIES.items():
            logging.info(f"category - {category} START")
            page = 1
            response = self.get_response(url, page)
            if not response:
                return
            logging.info(f"url - {response.url}")
            items, next_page_link = self.get_soup(response)
            all_raw_items.extend(items)
            while next_page_link:
                page += 1
                response_next = self.get_response(url, page)
                if not response_next:
                    continue
                logging.info(f"url - {response_next.url}")
                items, next_page_link = self.get_soup(response_next)
                all_raw_items.extend(items)
            parsed_data = self.parse_items(all_raw_items)
            all_raw_items.clear()
            self.data_to_json(parsed_data, category)
            logging.info(f"category - {category} END")
        logging.info(f"shop.kz -  Parser END")

    def get_response(self, url: str, page: int) -> requests.models.Response | None:
        params = {'PAGEN_1': page}
        response = self.session.get(url=url, headers=config.HEADERS, params=params)
        if response.status_code != 200:
            logging.error(f"{response.status_code} - {response.url}")
            return None
        return response

    def get_soup(self, response: requests.models.Response) -> tuple:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='bx-catalog-product-middle')
        next_page_link = soup.find('li', class_='bx-pag-next').a
        return items, next_page_link

    def parse_items(self, items: list) -> list[dict]:
        items_data_list = []
        items_count = 0
        for item in items:
            name = item.find('h4', class_='bx_catalog_item_title_text').text.strip()
            articul = item.find('div', class_='bx_catalog_item_XML_articul').text
            articul = articul.split(':')[-1].strip()
            price = item.find_all('span', class_='bx-more-price-text')[-1].text
            price = ''.join([k for k in price.split() if k.isdigit()])
            memory_size = str
            specifications: BeautifulSoup.element.ResultSet = item.find_all(class_='bx_catalog_item_value')
            for detail in specifications:
                if 'Объем встроенной памяти:' == detail.find_previous().text:
                    memory_size = detail.text

            items_data_list.append({
                'name': name,
                'articul': articul,
                'price': price,
                'memory-size': memory_size,
            })
            items_count += 1
        logging.info(f"total parsed items - {items_count}")
        return items_data_list

    def data_to_json(self, items_data_list: list[dict], category):
        with open(f"{category}.json", 'w', encoding='utf-8') as f:
            json.dump(items_data_list, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    logging.basicConfig(
        handlers=[RotatingFileHandler('../shop.log', mode='a+', maxBytes=10485760, backupCount=2, encoding='utf-8')],
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    Shop().start()
