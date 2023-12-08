import logging
from datetime import datetime

import pandas as pd

from src.utils import get_currency_rates, get_greeting, get_stock_prices

logger = logging.getLogger(__name__)


def generate_user_answer(data_time: str, data_frame: pd.DataFrame, user_currencies: list, user_stocks: list) -> dict:
    """
    Функция принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS,
    и возвращающую json-ответ со следующими данными:
        Приветствие в формате “Добрый ???”
        По каждой карте:
            Последние 4 цифры карты
            Общая сумма расходов
            Кэшбэк (1 рубль на каждые 100 рублей)
        Топ-5 транзакции по сумме платежа
        Курс валют
        Стоимость акций
    :param data_time: Дата и время
    :param data_frame: Данные полученные из файла
    :param user_currencies: Валюта
    :param user_stocks: Акции
    :return: JSON-ответ
    """

    required_columns = ['Дата операции', 'Дата платежа', 'Номер карты', 'Статус', 'Сумма операции', 'Валюта операции',
                        'Сумма платежа', 'Валюта платежа', 'Кэшбэк', 'Категория', 'MCC', 'Описание',
                        'Бонусы (включая кэшбэк)', 'Округление на инвесткопилку', 'Сумма операции с округлением']

    missing_columns = [col for col in required_columns if col not in data_frame.columns]

    if missing_columns:
        logger.warning(f"Отсутствуют следующие столбцы: {missing_columns}. В файле не найдены поля")
        return {}
    else:

        time_now = datetime.now().strftime("%H:%M:%S")

        data_frame['Дата операции'] = pd.to_datetime(data_frame['Дата операции'], dayfirst=True)

        input_date = datetime.strptime(data_time, '%d.%m.%Y %H:%M:%S')
        start_date = input_date.replace(day=1, hour=0, minute=0, second=0)

        filtered_date = data_frame[
            (data_frame['Дата операции'] >= start_date) & (data_frame['Дата операции'] <= input_date)]
        filtered_df = filtered_date[filtered_date['Сумма операции'] < 0]
        grouped_df = filtered_df.groupby('Номер карты').agg({'Сумма операции': 'sum', 'Бонусы (включая кэшбэк)': 'sum'})

        cards = []
        for card_number, row in grouped_df.iterrows():
            card_data = {
                "last_digits": card_number[-4:],
                "total_spent": round(abs(row['Сумма операции']), 2),
                "cashback": round(row['Бонусы (включая кэшбэк)'], 2)
            }
            cards.append(card_data)

        top5_transactions = filtered_date.nlargest(5, 'Сумма операции с округлением')

        top_transactions = []
        for _, row in top5_transactions.iterrows():
            transaction_data = {
                "date": row['Дата операции'].strftime('%d.%m.%Y'),
                "amount": row['Сумма платежа'],
                "category": row['Категория'],
                "description": row['Описание']
            }
            top_transactions.append(transaction_data)

        answer = {
            "greeting": get_greeting(time_now),
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": get_currency_rates(user_currencies),
            "stock_prices": get_stock_prices(user_stocks)
        }

        logger.info("Ответ для веб построен в JSON формате")

        return answer
