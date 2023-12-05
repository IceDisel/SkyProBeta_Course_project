from src import log
from src.reports import spending_by_weekday
from src.services import search_transactions
from src.utils import read_json_file, read_xls_file
from src.views import generate_user_answer
import pandas as pd

logger = log.setup_logging()

PATH = "data/operations.xls"
PATH_JSON = "user_settings.json"

user_currencies, user_stocks = read_json_file(PATH_JSON)
data_frame = read_xls_file(PATH)
data_frame1 = read_xls_file(PATH)

print(generate_user_answer("31.12.2021 16:44:00", data_frame, user_currencies, user_stocks))

print(search_transactions(data_frame1, "ж/д билеты"))

spending_by_weekday(data_frame, "31.12.2021")
