from datetime import date
from settings import marquee_api, gov_api
import pandas as pd

# pull the UK data into a Pandas dataframe
try:
    gov_frame = pd.read_csv("data/gov.csv")
except:
    gov_frame = gov_api.get_dataframe()
    gov_frame.to_csv("data/gov.csv")

try:
    marquee_frame = pd.read_csv("data/marquee.csv")
except:
    pass
    marquee_frame = marquee_api.get_data(
        countryId='GB', start=date(2020, 1, 3))
    # TODO - process marquee data in required format
    # marquee_frame.to_csv("data/marquee.csv")
