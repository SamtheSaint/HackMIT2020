from datetime import date
from settings import marquee_api, gov_api
import pandas as pd

# pull the UK data into a Pandas dataframe
try:
    gov_frame = pd.read_json("data/gov.json")
except ValueError:
    gov_frame = gov_api.get_dataframe()
    gov_frame.to_json("data/gov.json")
    gov_frame.to_csv("data/gov.csv")

try:
    marquee_frame = pd.read_json("data/marquee.json")
except ValueError:
    marquee_frame = marquee_api.get_data(
        countryId='GB', start=date(2020, 1, 3), fields=["ccgCode", "count"])
    marquee_frame = marquee_frame.drop("countryId", axis=1)
    marquee_frame = marquee_frame.groupby(
        ["date", "ccgCode"]).aggregate({"count": "sum"}).reset_index()
    marquee_frame.to_json("data/marquee.json")
    marquee_frame.to_csv("data/marquee.csv")

df = pd.read_csv('data/link_table.csv', delimiter=',')
coords = [list(row) for row in df.values]
ts_list = []
# Generates time-series for both datasets
for coord in coords:
    ts_cases = gov_frame[gov_frame['areaCode'] == coord[1].strip()]
    ts_phones = marquee_frame[marquee_frame['ccgCode'] == coord[0].strip()]
    ts_link = (ts_phones, ts_cases)
    ts_list.append(ts_link)

# print(ts_list)
# TODO: Perform time-series analysis to both to find lag correlation!
