import json
from typing import Any
from unittest.mock import MagicMock
import os
import pandas as pd
import pytest
from yahoo_fin import stock_info as si

from src.utils import get_currency_rates, get_greeting, get_stock_prices, read_json_file, read_xls_file, \
    report_decorator


def test_read_xls_file() -> None:
    """
    Функция тестирования чтения файла XLS
    :return: None
    """
    path = 'tests/test_read_data.xls'
    expected_data = pd.DataFrame({'Name': ['John', 'Jane', 'Mike'], 'Age': [25, 30, 35]})

    actual_data = read_xls_file(path)

    assert actual_data.equals(expected_data)


def test_read_json_file(tmp_path: Any) -> None:
    """
    Функция тестирования чтения файла JSON
    :param tmp_path: путь
    :return: None
    """
    test_data = {
        'user_currencies': ['USD', 'EUR', 'JPY'],
        'user_stocks': ['AAPL', 'GOOGL', 'AMZN']
    }
    file_path = tmp_path / 'test_data.json'
    with open(file_path, 'w') as file:
        json.dump(test_data, file)

    user_currencies, user_stocks = read_json_file(file_path)

    assert user_currencies == test_data['user_currencies']
    assert user_stocks == test_data['user_stocks']


@pytest.mark.parametrize("time, expected_greeting", [
    ("06:58:59 UTC", "Доброе утро"),
    ("15:30:00 UTC", "Добрый день"),
    ("20:45:12 UTC", "Добрый вечер"),
    ("02:00:00 UTC", "Доброй ночи")
])
def test_get_greeting(time: str, expected_greeting: str) -> None:
    assert get_greeting(time) == expected_greeting


def test_get_stock_prices(mocker: Any) -> None:
    mocker.patch("yahoo_fin.stock_info.get_data")
    mock_df = MagicMock()
    mock_df.close.iloc[-1].__round__.return_value = 100.0
    si.get_data.return_value = mock_df

    symbols = ["AAPL", "GOOGL", "AMZN"]
    expected_result = [
        {"stock": "AAPL", "price": 100.0},
        {"stock": "GOOGL", "price": 100.0},
        {"stock": "AMZN", "price": 100.0}
    ]
    assert get_stock_prices(symbols) == expected_result


def test_get_currency_rates(mocker: Any) -> None:
    mocker.patch("yahoo_fin.stock_info.get_data")
    mock_df = MagicMock()
    mock_df.close.iloc[-1].__round__.return_value = 75.0
    si.get_data.return_value = mock_df

    currencies = ["USD", "EUR", "GBP"]
    expected_result = [
        {"currency": "USD", "rate": 75.0},
        {"currency": "EUR", "rate": 75.0},
        {"currency": "GBP", "rate": 75.0}
    ]
    assert get_currency_rates(currencies) == expected_result


@pytest.fixture
def tmp_report_file() -> str:
    return "tests/test_data.xls"


def dummy_function() -> pd.DataFrame:
    data = {
        'Дата операции': ['31.12.2021 16:44:00', '31.12.2021 16:42:04', '31.12.2021 16:39:04', '31.12.2021 15:44:39',
                          '31.12.2021 01:23:42', '31.12.2021 00:12:53'],
        'Описание': ['Колхоз', 'Колхоз', 'Магнит', 'Колхоз', 'Ozon.ru', 'Константин Л.'],
        'Категория': ['Супермаркеты', 'Супермаркеты', 'Супермаркеты', 'Супермаркеты', 'Различные товары', 'Переводы']
    }
    return pd.DataFrame(data)


def test_report_decorator(tmp_report_file: str) -> None:
    """
    Функция тестирование декоратора
    :param tmp_report_file: путь до файла
    :return: None
    """
    decorated_function = report_decorator(filename=tmp_report_file)(dummy_function)
    result = decorated_function()

    assert os.path.exists(tmp_report_file)
    assert isinstance(result, pd.DataFrame)
    assert result.equals(dummy_function())
