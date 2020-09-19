from datetime import date
from settings import dataset_online, api_covid
import pandas as pd

# pull the UK data into a Pandas dataframe
frame_covid = api_covid.get_dataframe()
pd.set_option('display.max_rows', len(frame_covid))
pd.set_option('display.max_columns', len(frame_covid.columns))
frame_covid.to_json("gov.json")

# frame_online = dataset_online.get_data(countryId='GB', start=date(2019, 1, 1))
# pd.set_option('display.max_rows', len(frame_online))
# pd.set_option('display.max_columns', len(frame_online.columns))
# print(frame_online.head())

