from typing import Any

import pandas as pd
from unittest.mock import patch

from src.views import generate_user_answer

from src.utils import read_xls_file


@patch('src.views.get_currency_rates')
@patch('src.views.get_greeting')
@patch('src.views.get_stock_prices')
def test_generate_user_answer(mock_get_stock_prices: Any, mock_get_greeting: Any, mock_get_currency_rates: Any) -> None:
    # Создаем тестовые данные
    data_time = '31.12.2021 16:44:00'
    df = read_xls_file("data/operations.xls")
    data_frame = pd.DataFrame(df)
    user_currencies = ['USD', 'EUR']
    user_stocks = ['AAPL', 'GOOGL']

    mock_get_currency_rates.return_value = {'USD': 1.2, 'EUR': 0.9}
    mock_get_greeting.return_value = 'Добрый день'
    mock_get_stock_prices.return_value = {'AAPL': 150.0, 'GOOGL': 2500.0}

    result = generate_user_answer(data_time, data_frame, user_currencies, user_stocks)

    assert result['greeting'] == 'Добрый день'
    assert result['currency_rates'] == {'USD': 1.2, 'EUR': 0.9}
    assert result['stock_prices'] == {'AAPL': 150.0, 'GOOGL': 2500.0}

    mock_get_currency_rates.assert_called_once_with(['USD', 'EUR'])
    mock_get_stock_prices.assert_called_once_with(['AAPL', 'GOOGL'])
