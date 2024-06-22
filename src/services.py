import pandas as pd

from src.constants import prices_file


def get_similar_data(title) -> list[str]:
    '''
    Получить список товаров, названия
    которых совпадает с переданным названием товара.
    '''
    data = pd.read_excel(prices_file)
    items_names = data.columns[5] 
    print(data[items_names]) # список товаров, циклом пройтись
