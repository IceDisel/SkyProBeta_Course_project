import json
import logging
from typing import Callable, Optional, Any

import pandas as pd
import xlwt
from requests.exceptions import ConnectionError
from yahoo_fin import stock_info as si

logger = logging.getLogger(__name__)


def read_xls_file(path: str) -> pd.DataFrame:
    """
    Функция чтение XLS файла
    :param path: путь до файла
    :return: pd.DataFrame
    """
    try:
        data = pd.read_excel(path)
        logger.info("Файл-XLS успешно прочитан")
        return data
    except FileNotFoundError:
        logger.warning("Произошла ошибка при чтении XLS-файла")
        return pd.DataFrame()


def read_json_file(file_path: str) -> tuple:
    """
    Функция чтения JSON-файла с пользовательскими настройками
    :param file_path: путь до файла
    :return: Кортеж данных
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            user_currencies = data['user_currencies']
            user_stocks = data['user_stocks']
            logger.info("Файл-JSON успешно прочитан")
            return user_currencies, user_stocks
    except FileNotFoundError:
        logger.warning("Произошла ошибка при чтении JSON-файла")
        return " ", " "


def get_greeting(time: str) -> str:
    """
    Реализация функции приветствия в зависимости от времени суток
    :param time: Время
    :return: Добрый ???, где ??? - утро/день/вечер/ночь в зависимости от текущего времени
    """
    hour = int(time.split(":")[0])
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_stock_prices(symbols: list) -> list:
    """
    Функция запроса цен акций с сайта Yahoo
    :param symbols: Акции
    :return: Список цен на акции
    """
    result = []

    try:
        for symbol in symbols:
            df = si.get_data(symbol)
            price = df.close.iloc[-1]
            stock_data = {
                "stock": symbol,
                "price": round(price, 2)
            }
            result.append(stock_data)

        return result
    except (AssertionError, ConnectionError):
        logger.warning("Произошла ошибка запроса цен акций")
        return []


def get_currency_rates(currencies: list) -> list:
    """
    Функция запроса цен валюты с сайта Yahoo
    :param currencies: Валюта
    :return: Список цен на валюту
    """
    result = []

    try:
        for currency in currencies:
            df = si.get_data(f"{currency}RUB=X")
            rate = df.close.iloc[-1]
            rates = {
                "currency": currency,
                "rate": round(rate, 2)
            }
            result.append(rates)

        return result
    except (AssertionError, ConnectionError):
        logger.warning("Произошла ошибка запроса цен курса валют")
        return []


def report_decorator(filename: Optional[str] = None) -> Callable:
    """
    Декоратор записи отчетов в файл XLS
    :param filename:
    :return:
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            if filename is None:
                report_filename = "report.xls"
            else:
                report_filename = filename

            result = func(*args, **kwargs)

            if isinstance(result, pd.DataFrame):
                workbook = xlwt.Workbook()
                sheet = workbook.add_sheet('Sheet1')

                for i, row in enumerate(result.values):
                    for j, value in enumerate(row):
                        sheet.write(i, j, value)

                workbook.save(report_filename)
            else:
                logger.warning("Результат функции не является DataFrame")

            return result

        return wrapper

    return decorator
