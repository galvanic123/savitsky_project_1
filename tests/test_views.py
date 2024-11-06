import json
from unittest.mock import patch

from src.config import date
from src.views import main


@patch("src.config.data_json", return_value={})
def test_main(mock_data_json):      # type: ignore[no-untyped-def]
    # Mock the dependencies
    @patch("src.utils.get_response")
    def mock_get_response(date, mock_get_response):         # type: ignore[no-untyped-def]
        return "Добрый день"

    @patch("src.utils.filter_transactions")
    def mock_filter_transactions(mock_filter_transactions):            # type: ignore[no-untyped-def]
        return [
            {"last_digits": "*7197", "total_spent": -23562.64, "cashback": 0},
            {"last_digits": "*5091", "total_spent": -12742.92, "cashback": 0},
            {"last_digits": "Неизвестная карта", "total_spent": -55046.56, "cashback": 0},
            {"last_digits": "*4556", "total_spent": 198770.3, "cashback": 181.0},
        ]

    @patch("src.utils.getting_top_specified_period")
    def mock_getting_top_specified_period(transactions,
                                          mock_getting_top_specified_period):          # type: ignore[no-untyped-def]
        return [
            {
                "date": "30.12.2021",
                "amount": 174000.0,
                "category": "Пополнения",
                "description": "Пополнение через Газпромбанк",
            },
            {
                "date": "22.12.2021",
                "amount": -28001.94,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "date": "22.12.2021",
                "amount": 28001.94,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {"date": "23.12.2021", "amount": 20000.0, "category": "Другое", "description": "Иван С."},
            {"date": "30.12.2021", "amount": -20000.0, "category": "Переводы", "description": "Константин Л."},
        ]

    @patch("src.utils.getting_data_currencies")
    def mock_getting_data_currencies(url, data_json, mock_getting_data_currencies):      # type: ignore[no-untyped-def]
        return [{"currency": "USD", "rate": "64.1824"}, {"currency": "EUR", "rate": "69.244"}]

    @patch("src.utils.getting_data_stock_prices")
    def mock_getting_data_stock_prices(url_stocks, data_json,
                                       mock_getting_data_stock_prices):        # type: ignore[no-untyped-def]
        return [
            {'price': 223.73, 'stock': 'AAPL'},
            {'price': 205.425, 'stock': 'AMZN'},
            {'price': 176.455, 'stock': 'GOOGL'},
            {'price': 419.65, 'stock': 'MSFT'},
            {'price': 287.8202, 'stock': 'TSLA'}
        ]

    result = main(date)

    expected_result = {
        "greeting": "Добрый день",
        "cards": [
            {"last_digits": "*7197", "total_spent": -23562.64, "cashback": 0},
            {"last_digits": "*5091", "total_spent": -12742.92, "cashback": 0},
            {"last_digits": "Неизвестная карта", "total_spent": -55046.56, "cashback": 0},
            {"last_digits": "*4556", "total_spent": 198770.3, "cashback": 181.0},
        ],
        "top_transactions": [
            {
                "date": "30.12.2021",
                "amount": 174000.0,
                "category": "Пополнения",
                "description": "Пополнение через Газпромбанк",
            },
            {
                "date": "22.12.2021",
                "amount": -28001.94,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "date": "22.12.2021",
                "amount": 28001.94,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {"date": "23.12.2021", "amount": 20000.0, "category": "Другое", "description": "Иван С."},
            {"date": "30.12.2021", "amount": -20000.0, "category": "Переводы", "description": "Константин Л."},
        ],
        "currency_rates": [{"currency": "USD", "rate": "64.1824"}, {"currency": "EUR", "rate": "69.244"}],
        "stock_prices": [
            {'price': 222.72, 'stock': 'AAPL'},
            {'price': 207.09, 'stock': 'AMZN'},
            {'price': 176.51, 'stock': 'GOOGL'},
            {'price': 420.18, 'stock': 'MSFT'},
            {'price': 288.53, 'stock': 'TSLA'}
        ],
    }
    assert json.loads(result) == expected_result
