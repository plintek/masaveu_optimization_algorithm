import json
import os
from time import time
import requests
from src.entities.Address.Address import Address
from src.entities.Location.Location import Location
from src.utils.cache_utility import CacheUtility


def calculate_multiple_locations_with_here(start_location: Location, intermediate_locations: list[Location], end_location: Location):
    start_time = time()

    api_key = "KHKPpYn2p2aNvLQwUOA1TwbTRJa6n-ntaitcRBkCwag"
    intermediate_points_url = ""
    for intermediate_point in intermediate_locations:
        intermediate_points_url += "&via={},{}".format(
            intermediate_point.latitude, intermediate_point.longitude)

    url = "https://router.hereapi.com/v8/routes?origin={},{}&transportMode=car&destination={},{}{}&return=summary,polyline&apiKey={}".format(
        start_location.latitude, start_location.longitude, end_location.latitude, end_location.longitude, intermediate_points_url, api_key)

    cache = CacheUtility.read_cache(url, "here")
    if cache:
        return cache

    print("HERE PETITION")

    response = requests.get(url)
    data = response.json()

    CacheUtility.write_cache(url, data, "here")

    end_time = time()
    print("HERE PETITION TIME: {}".format(end_time - start_time))

    return data


def calculate_route_from_addresses_with_here(delegation, addresses):
    start_location = delegation
    end_location = delegation
    intermediate_locations = []
    for address in addresses:
        intermediate_locations.append(address)

    route = calculate_multiple_locations_with_here(
        start_location, intermediate_locations, end_location)
    if ("notices" in route and len(route["notices"]) > 0):
        raise Exception(route["notices"][0]["title"])
    return route


def calculate_time_on_road_from_here_route(result):
    time_on_road = 0
    for here_section in result['routes'][0]['sections']:
        time_on_road += get_duration_from_here_section(here_section)

    return time_on_road


def get_distance_from_here_section(here_section):
    return here_section['summary']['length']


def get_duration_from_here_sections(here_sections):
    total_duration = 0
    for here_section in here_sections:
        total_duration += get_duration_from_here_section(here_section)

    return total_duration


def get_duration_from_here_section(here_section):
    try:
        return here_section['summary']['baseDuration']
    except:
        # If transportation is not car, there is no baseDuration
        return here_section['summary']['duration']


def calculate_total_time_of_route(calculated_route, addresses):
    time_on_road = calculate_time_on_road_from_here_route(calculated_route)
    time_on_spots = Address.calculate_time_on_spots(addresses)

    return time_on_road + time_on_spots


def get_total_time_of_here_section_and_address(here_section, address):
    return get_duration_from_here_section(here_section) + address.time_on_spot


def get_average_duration_of_here_sections(here_sections):
    total_duration = 0
    for here_section in here_sections:
        total_duration += get_duration_from_here_section(here_section)

    return total_duration / len(here_sections)
