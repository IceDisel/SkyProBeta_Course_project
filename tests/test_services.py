import pytest
import pandas as pd
from src.services import search_transactions
import json


def test_search_transactions() -> None:
    data = {
        'Дата операции': ['31.12.2021 16:44:00', '31.12.2021 16:42:04', '31.12.2021 16:39:04', '31.12.2021 15:44:39',
                          '31.12.2021 01:23:42', '31.12.2021 00:12:53'],
        'Описание': ['Колхоз', 'Колхоз', 'Магнит', 'Колхоз', 'Ozon.ru', 'Константин Л.'],
        'Категория': ['Супермаркеты', 'Супермаркеты', 'Супермаркеты', 'Супермаркеты', 'Различные товары', 'Переводы']
    }
    df = pd.DataFrame(data)

    result = search_transactions(df, 'Колхоз')

    assert isinstance(result, str)

    try:
        json.loads(result)
    except ValueError:
        pytest.fail("Возвращенная строка не является JSON.")

    expected_data = [
        {
            "Дата операции": "31.12.2021 16:44:00",
            "Описание": "Колхоз",
            "Категория": "Супермаркеты"
        },
        {
            "Дата операции": "31.12.2021 16:42:04",
            "Описание": "Колхоз",
            "Категория": "Супермаркеты"
        },
        {
            "Дата операции": "31.12.2021 15:44:39",
            "Описание": "Колхоз",
            "Категория": "Супермаркеты"
        }
    ]
    assert json.loads(result) == expected_data

    df = pd.DataFrame()

    assert search_transactions(df, 'Колхоз') == []
