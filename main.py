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

marquee_gov_link = pd.read_csv('data/link_table.csv')
gov_lat_long_link = pd.read_csv(
    "data/codes-lat-long_link.csv", index_col="areaCode")

codes = [tuple(row) for row in marquee_gov_link.values]
marquee_gov_frame = pd.DataFrame(columns=[
                                 "date", "latitude", "longitude", "num_of_phone_calls", "num_of_new_cases"])
tolerance = 30
for code in codes:
    ts_gov = gov_frame[gov_frame['areaCode'] == (area_code := code[1].strip())]
    ts_marquee = marquee_frame[marquee_frame['ccgCode']
                               == code[0].strip()]
    if len(ts_gov) < tolerance or len(ts_marquee) < tolerance:
        continue
    else:
        try: #This is temporary and bypasses duplicate tuple entries, i.e. multiple links to single place
            ts_gov_marquee = ts_gov.join(ts_marquee, on="date")
            ts_gov_marquee['latitude'] = gov_lat_long_link.loc[area_code]['Latitude']
            ts_gov_marquee['longitude'] = gov_lat_long_link.loc[area_code]['Longitude']
            ts_gov_marquee['num_of_phone_calls'] = ts_gov_marquee['count']
            ts_gov_marquee['num_of_new_cases'] = ts_gov_marquee['newCasesBySpecimenDate']
            ts_gov_marquee = ts_gov_marquee.drop(
                columns=["areaCode", "ccgCode", "count", "newCasesBySpecimenDate"]).reset_index()
            marquee_gov_frame = marquee_gov_frame.append(ts_gov_marquee)
        except:
            continue

marquee_gov_frame.set_index("date", inplace=True)
marquee_gov_frame.sort_index(inplace=True)

marquee_gov_frame.to_csv(f'data.csv')


def generate_timeseries():
    ts_list, ts_tolerance = [], 30
    # Generates time-series for both datasets
    for code in codes:
        ts_gov = gov_frame[gov_frame['areaCode'] == code[1].strip()]
        ts_marquee = marquee_frame[marquee_frame['ccgCode']
                                   == code[0].strip()]
        if len(ts_gov) > ts_tolerance and len(ts_marquee) > ts_tolerance:
            ts_list.append((ts_marquee, ts_gov))

    for (ts_marquee, ts_gov) in ts_list:
        area_code = ts_gov["areaCode"][0]
        curr_max = -1
        for i in range(1,30):
            curr_max = max(ts.econometrics.correlation(
                ts_marquee["count"], ts_gov["newCasesBySpecimenDate"], ).mean(), curr_max)
        print(f'{curr_max} at lag {i}')

        # TODO: Trim data to match time for visualisation, shouldn't matter for correlation
        ts_marquee.to_csv(f"exports/marquee{area_code}.csv")
        ts_gov.to_csv(f"exports/gov{area_code}.csv")


if __name__ == "__main__":
    # generate_timeseries()
    pass
