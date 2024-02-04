from time import time
import requests
from src.entities.location import Location
from src.utils.cache_utility import CacheUtility


def calculate_locations_with_here(start_location: Location, end_location: Location):
    """ Calculate the route between two locations with Here API """
    start_time = time()

    api_key = "KHKPpYn2p2aNvLQwUOA1TwbTRJa6n-ntaitcRBkCwag"

    url = "https://router.hereapi.com/v8/routes?origin={},{}&transportMode=truck&destination={},{}&return=summary,polyline&apiKey={}".format(
        start_location.lat, start_location.lon, end_location.lat, end_location.lon, api_key)

    cache = CacheUtility.read_cache(url, "here")
    if cache:
        return cache

    print(f"HERE: {start_location} -> {end_location}")

    response = requests.get(url, timeout=5)
    data = response.json()

    CacheUtility.write_cache(url, data, "here")

    end_time = time()
    print(f"HERE: {end_time - start_time} seconds")

    return data


def calculate_time_on_road_from_here_route(result):
    """ Calculate the time on road from the Here API response """
    time_on_road = 0
    for here_section in result['routes'][0]['sections']:
        time_on_road += get_duration_from_here_section(here_section)

    return time_on_road


def get_distance_from_here_section(here_section):
    """ Get the distance from a Here API section """
    return here_section['summary']['length']


def get_duration_from_here_sections(here_sections):
    """ Get the duration from a list of Here API sections """
    total_duration = 0
    for here_section in here_sections:
        total_duration += get_duration_from_here_section(here_section)

    return total_duration


def get_duration_from_here_section(here_section):
    """ Get the duration from a Here API section """
    try:
        return here_section['summary']['baseDuration']
    except KeyError:
        # If transportation is not car, there is no baseDuration
        return here_section['summary']['duration']


# def calculate_total_time_of_route(calculated_route, addresses):
#     """ Calculate the total time of a route with Here API """
#     time_on_road = calculate_time_on_road_from_here_route(calculated_route)
#     time_on_spots = Address.calculate_time_on_spots(addresses)

#     return time_on_road + time_on_spots


def get_total_time_of_here_section_and_address(here_section, address):
    """ Get the total time of a Here API section and an address """
    return get_duration_from_here_section(here_section) + address.time_on_spot


def get_average_duration_of_here_sections(here_sections):
    """ Get the average duration of a list of Here API sections """
    total_duration = 0
    for here_section in here_sections:
        total_duration += get_duration_from_here_section(here_section)

    return total_duration / len(here_sections)
