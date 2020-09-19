from datetime import date
from settings import marquee_api, gov_api
import pandas as pd
import gs_quant.timeseries as ts
import matplotlib.pyplot as plt

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

# Generates time-series for both datasets
for coord in coords:
    ts_cases = gov_frame[gov_frame['areaCode'] == coord[1].strip()]
    ts_phones = marquee_frame[marquee_frame['ccgCode'] == coord[0].strip()]
    ts_link = (ts_phones.drop(columns=["ccgCode"]),
               ts_cases.drop(columns=["areaCode"]))
    # if phones or cases < n
    if len(ts_cases) < 30 or len(ts_phones) < 30:
        continue
    ts_list.append(ts_link)

for pair in ts_list:
    plt.figure(figsize=(12, 5))
    # TODO: Calculate optimal correlation lag time for each and do statistical analysis on results, i.e. median, S.D.,
    #  etc.
    print(ts.econometrics.correlation(
        pair[0]["count"], pair[1]["newCasesBySpecimenDate"], 10))
    pair[0]["count"].name = "Phone Calls"
    pair[0]["count"].plot(color='blue', grid=True)
    pair[1]["newCasesBySpecimenDate"].name = "Cases"
    pair[1]["newCasesBySpecimenDate"].plot(color='red', grid=True, secondary_y=True)
    plt.show()
    # TODO: Trim data to match time for visualisation, shouldn't matter for correlation
    break
