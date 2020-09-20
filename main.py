from datetime import date

import gs_quant.timeseries as ts
import pandas as pd

from settings import marquee_api, gov_api

# pull the UK data into a Pandas dataframe
try:
    gov_frame = pd.read_csv("data/gov.csv")
    gov_frame['date'].apply(lambda x: date.fromisoformat(x))
    gov_frame.set_index("date", inplace=True)
except IOError:
    gov_frame = gov_api.get_dataframe()
    gov_frame.set_index("date", inplace=True)
    gov_frame.to_csv("data/gov.csv")

try:
    marquee_frame = pd.read_csv("data/marquee.csv")
    marquee_frame['date'].apply(lambda x: date.fromisoformat(x))
except IOError:
    marquee_frame = marquee_api.get_data(
        countryId='GB', start=date(2020, 1, 3), fields=["ccgCode", "count"])
    marquee_frame = marquee_frame.drop(columns=["countryId"])
    marquee_frame.to_csv("data/marquee.csv")
finally:
    marquee_frame = marquee_frame.groupby(["date", "ccgCode"]).aggregate({
        "count": "sum"}).reset_index()
    marquee_frame.set_index("date", inplace=True)

df = pd.read_csv('data/link_table.csv', delimiter=',')
coords = [list(row) for row in df.values]
ts_list = []
min_datapoints = 30
# Generates time-series for both datasets
for coord in coords:
    ts_gov = gov_frame[gov_frame['areaCode'] == coord[1].strip()]
    ts_marquee = marquee_frame[marquee_frame['ccgCode'] == coord[0].strip()]
    # if phones or cases < n
    if len(ts_gov) > min_datapoints and len(ts_marquee) > min_datapoints:
        ts_list.append((ts_marquee, ts_gov))

for (ts_marquee, ts_gov) in ts_list:
    area_code = ts_gov["areaCode"][0]
    # TODO: Calculate optimal correlation lag time for each and do statistical analysis on results, i.e. median, S.D.,
    #  etc.
    # TODO: Work out how to find the optimal correlation lag, possibly iterating over windows & mean?
    # curr_max = -1
    # for i in range(1,30):
    #     curr_max = max(ts.econometrics.correlation(
    #         pair[0]["count"], pair[1]["newCasesBySpecimenDate"], ).mean(), curr_max)
    # print(f'{curr_max} at lag {i}')

    # print(ts.econometrics.correlation(
    #     pair[0]["count"], pair[1]["newCasesBySpecimenDate"]))
    # print(ts.econometrics.correlation(
    #     ts_marquee["count"], ts_gov["newCasesBySpecimenDate"]))
    # TODO: Trim data to match time for visualisation, shouldn't matter for correlation
    ts_marquee.to_csv(f"exports/marquee{area_code}.csv")
    ts_gov.to_csv(f"exports/gov{area_code}.csv")
