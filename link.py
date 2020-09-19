import requests
from requests import HTTPError


def get_geojson(area_code):
    try:
        response = requests.get("https://findthatpostcode.uk/areas/" + area_code + ".geojson")
        return response.json()
    except HTTPError:
        pass


def geojson_contains(outer_area_code, inner_area_code):
    outer_json = get_geojson(outer_area_code)
    # TODO: Implement Shapely contains method


geojson_contains("E38000001", "E38000001")
