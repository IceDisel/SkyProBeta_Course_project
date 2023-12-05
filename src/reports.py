from typing import Optional

import pandas as pd

from src.utils import report_decorator


@report_decorator("report.xls")
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает средние траты в каждый из дней недели за последние 3 месяца от переданной даты
    :param transactions: Данные с XLS файла
    :param date: Дата
    :return: Результат функции
    """
    if date is None:
        date = pd.to_datetime('today').strftime('%d.%m.%Y')

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')

    three_months_ago = pd.to_datetime(date, format='%d.%m.%Y') - pd.DateOffset(months=3)
    filtered_transactions = transactions[
        (transactions['Дата операции'] >= three_months_ago) & (transactions['Дата операции'] <= date)]

    filtered_transactions = filtered_transactions[filtered_transactions['Сумма операции'] < 0]

    spend_by_weekday = filtered_transactions.groupby(filtered_transactions['Дата операции'].dt.dayofweek)[
        'Сумма операции'].mean()

    spend_by_weekday = spend_by_weekday.round(2)

    df_with_weekday = pd.DataFrame(spend_by_weekday)
    df_with_weekday['Дни недели'] = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    df_with_weekday = df_with_weekday[['Дни недели', 'Сумма операции']]

    return df_with_weekday
