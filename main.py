import os
from datetime import date
from settings import dataset_online, api_covid

# pull the UK data into a Pandas dataframe
frame_covid = api_covid.get_dataframe()
print(frame_covid)

frame_online = dataset_online.get_data(countryId='GB', start=date(2019, 1, 1))
print(frame_online)
