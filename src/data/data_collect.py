import requests
from datetime import timedelta, datetime as dt
from geopy.geocoders import Nominatim


GEOLOCATOR = Nominatim(user_agent="Your Name")


def coordinates_from_location(location):
    coordinates = GEOLOCATOR.geocode(location)
    return coordinates.latitude, coordinates.longitude


def location_from_coordinates(coordinates):
    str_coordinates = str(coordinates["lat"]) + ", " + str(coordinates["lon"])
    location = GEOLOCATOR.reverse(str_coordinates)
    return (location.raw["address"])["municipality"]


"""
    returns a JSON dataset of the air pollution of a city between 2 defined times
"""
def pollution_data(location, start_time, end_time):
    start_time = round(dt.timestamp(start_time))
    end_time = round(dt.timestamp(end_time))
    coordinates = coordinates_from_location(location)
    address = (
        "http://api.openweathermap.org/data/2.5/air_pollution/history?lat="
        + str(coordinates[0])
        + "&lon="
        + str(coordinates[1])
        + "&start="
        + str(start_time)
        + "&end="
        + str(end_time)
        + "&appid=a11c2b0cb799b0a23392091a02453e2f"
    )  # the HTTP address on OpenWeather to get the data in JSON format
    response = requests.get(address)
    return response.json()

"""
    Collects a set of air pollution data from several cities in France
"""
def collect_pollution_data(delta):
    locs = ["Versailles", "Nice", "Brest", "Bayonne", "Strasbourg", "Lille"]
    collected_data = []
    for i in range(len(locs)):
        loc_data = pollution_data(
            location=locs[i], start_time=dt.now() - timedelta(delta), end_time=dt.now()
        )
        collected_data.append(loc_data)
    return collected_data
