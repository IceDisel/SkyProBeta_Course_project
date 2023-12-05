import json
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def search_transactions(dataframe: pd.DataFrame, search_string: str) -> str | list:
    """
    Фильтруем дата фрейм по описанию и категории, содержащим поисковую строку
    :param dataframe: Данные с XLS файла
    :param search_string: запрос
    :return: JSON-ответ
    """

    try:
        filtered_df = dataframe[
            dataframe['Описание'].str.contains(search_string, case=False) | dataframe['Категория'].str.contains(
                search_string, case=False)]

        transactions = filtered_df.to_dict(orient='records')

        return json.dumps(transactions, ensure_ascii=False, indent=4)
    except KeyError:
        logger.warning("Нет нужных полей для поиска транзакций")
        return []
