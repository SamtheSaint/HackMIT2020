import os
from datetime import date
from settings import dataset_online

# pull the UK data into a Pandas dataframe
frame = dataset_online.get_data(countryId='GB', start=date(2019, 1, 1))

print(frame)
