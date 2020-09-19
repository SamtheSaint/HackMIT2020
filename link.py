import requests
from requests import HTTPError
from geopy import distance
import numpy as np


def get_lat_long(area_code):
    try:
        response = requests.get(
            "https://findthatpostcode.uk/areas/" + area_code + ".json")
        geojson = response.json()
        return tuple(geojson.get("included")[0].get("attributes").get("location").values())
    except HTTPError:
        pass


def dist(outer_area_code, inner_area_code):
    outer_loc = get_lat_long(outer_area_code)
    inner_loc = get_lat_long(inner_area_code)
    return distance.distance(outer_loc, inner_loc).km


def link_ccg_to_areacode():
    with open("data/codes.txt") as f:
        area_codes = list(map(lambda x: x.strip(), f.readlines()))
    with open("data/marquee-codes.txt") as f:
        marquee_codes = list(map(lambda x: x.strip(), f.readlines()))
    with open("data/codes-lat-long.txt") as f:
        area_codes_lat_log = list(map(lambda x: tuple(map(float, x.strip("()").split(
            ", "))), map(lambda x: x.strip(), f.readlines())))
    with open("data/marquee-codes-lat-long.txt") as f:
        marquee_codes_lat_log = list(map(lambda x: tuple(map(float, x.strip("()").split(
            ", "))), map(lambda x: x.strip(), f.readlines())))
    print("ccgCode, areaCode")
    for i, marquee_lat_long in enumerate(marquee_codes_lat_log):
        distances = list(map(lambda area_lat_long: distance.distance(
            area_lat_long, marquee_lat_long), area_codes_lat_log))
        min_distance_index = np.argmin(distances)
        print(f"{marquee_codes[i]}, {area_codes[min_distance_index]}")


if __name__ == '__main__':
    link_ccg_to_areacode()
