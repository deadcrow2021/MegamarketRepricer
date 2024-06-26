import pandas as pd
import json
import os

from src.constants import prices_dir

files_names: list[str] = []
files_data: dict[str, pd.DataFrame] = {}
unique_item_names = set()

for (dirpath, dirnames, filenames) in os.walk(prices_dir):
    files_names.extend(filenames)
    break

for file in files_names:
    files_data[file] = pd.read_excel(prices_dir / file)

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
    # items_column_name = data.columns[5] # колонка названия товаров
    
    for file, data_frame in files_data.items():
        items_column_name = data_frame.columns[5]
        
        for item in data_frame[items_column_name]:
            if title == item:
                cards[file] = item
    
    return json.dumps(
        {'result': cards}
    )
