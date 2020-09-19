from datetime import date
from settings import marquee_api, gov_api
import pandas as pd

# pull the UK data into a Pandas dataframe
try:
    gov_frame = pd.read_json("data/gov.json")
except ValueError:
    gov_frame = gov_api.get_dataframe()
    gov_frame.to_json("data/gov.json")

try:
    marquee_frame = pd.read_json("data/marquee.json")
except ValueError:
    pass
    marquee_frame = marquee_api.get_data(
        countryId='GB', start=date(2020, 1, 3), fields=["ccgCode", "count"])
    marquee_frame = marquee_frame.drop("countryId", axis=1)
    # marquee_frame.to_csv("data/marquee.csv")
