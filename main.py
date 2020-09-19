from datetime import date
from settings import dataset_online, api_covid
import pandas as pd

# pull the UK data into a Pandas dataframe
frame_covid = api_covid.get_dataframe()
pd.set_option('display.max_rows', len(frame_covid))
pd.set_option('display.max_columns', len(frame_covid.columns))
print(frame_covid)

frame_online = dataset_online.get_data(countryId='GB', start=date(2019, 1, 1))
print(frame_online)

