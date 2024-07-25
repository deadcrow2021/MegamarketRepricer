import threading
import requests
import pandas
import json
import os

from src.constants import prices_dir, keys

from src.custom_functions import (
    get_shop_name,
    decrypt_data,
    encrypt_data
)


files_names: list[str] = []
files_data: dict[str, pandas.DataFrame] = {}
unique_item_names = set()

for (dirpath, dirnames, filenames) in os.walk(prices_dir):
    files_names.extend(filenames)
    break

for file in files_names:
    files_data[file] = pandas.read_excel(prices_dir / file)

for data_frame in files_data.values():
    items_column_name = data_frame.columns[5]

    for item in data_frame[items_column_name]:
        unique_item_names.add(item)


def get_similar_data(title: str) -> str:
    '''
    Получить список товаров, названия
    которых совпадает с переданным названием товара.
    '''
    similar_items = []

    for item in unique_item_names:
        if title.lower() in item.lower():
            similar_items.append(item)

    similar_items.sort()

    return json.dumps(
        {'result': similar_items}
    )


def find_cards_by_title(title: str):
    cards: dict[str, str] = {}

    for file, data_frame in files_data.items():
        items_id_column = data_frame.columns[1]
        items_column_name = data_frame.columns[5]

        file_name = file.split('.')[0]
        api_key = encrypt_data(keys['api_keys'][file_name])

        shop_name = get_shop_name(file)

        for i, item in enumerate(data_frame[items_column_name]):
            if title == item:
                item_id = str(data_frame[items_id_column][i])

                cards[file] = {
                    'item': item,
                    'item_id': item_id,
                    'shop': shop_name,
                    'api_key': api_key
                    }

    return json.dumps(
        {'result': cards}
    )


def change_remote_price(data_list: list[dict]):
    result_storage = []

    def send_requests(api_key: str, item_id: str, shop: str, price: int):
        resp_result = {}
        api_key = decrypt_data(api_key)
        try:
            req = requests.post(
                'https://api.megamarket.tech/api/merchantIntegration/v1/offerService/manualPrice/save',
                json={
                    "meta": {},
                    "data": {
                        "token": api_key,
                        "prices": [
                            {
                                "offerId": item_id,
                                "price": price,
                                "isDeleted": False
                            }
                        ]
                    }
                }
            )
        except Exception as exc:
            resp_result.update({
                'status': '0',
                'shop': shop,
                'item_id': item_id,
                'error': f'Request Error. {exc}.',
            })
            return

        json_data = json.loads(req.content.decode())

        if req.status_code == 200:
            resp_result.update({
                'status': json_data['success'],
                'shop': shop,
                'item_id': item_id,
            })

            if resp_result['status'] == 0:
                try:
                    resp_result.update({
                        'error': json_data['error']['message'],
                    })
                except:
                    resp_result.update({
                        'error': 'Unexpected Error.',
                    })

        elif req.status_code >= 400:
            resp_result.update({
                'status': '0',
                'shop': shop,
                'item_id': item_id,
                'error': 'Unexpected data. Check if send data is valid.',
            })

        result_storage.append(resp_result)


    threads: list[threading.Thread] = []

    for shop_data in data_list:
        t = threading.Thread(
            target=send_requests,
            args=(
                shop_data['api_key'],
                shop_data['item_id'],
                shop_data['shop'],
                int(shop_data['price']),
            )
        )
        
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    return {'result': result_storage}
