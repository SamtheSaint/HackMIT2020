import requests
from requests import HTTPError
from geopy import distance


def get_lat_long(area_code):
    try:
        response = requests.get("https://findthatpostcode.uk/areas/" + area_code + ".json")
        geojson = response.json()
        return tuple(geojson.get("included")[0].get("attributes").get("location").values())
    except HTTPError:
        pass


def dist(outer_area_code, inner_area_code):
    outer_loc = get_lat_long(outer_area_code)
    inner_loc = get_lat_long(inner_area_code)
    return distance.distance(outer_loc, inner_loc).km
