import json
import os
from time import time
import requests
from src.entities.location import Location
from src.utils.cache_utility import CacheUtility


def calculate_locations_with_here(start_location: Location, end_location: Location):
    start_time = time()

    api_key = "KHKPpYn2p2aNvLQwUOA1TwbTRJa6n-ntaitcRBkCwag"

    url = "https://router.hereapi.com/v8/routes?origin={},{}&transportMode=truck&destination={},{}&return=summary,polyline,turnbyturnactions,elevation&apiKey={}".format(
        start_location.lat, start_location.lon, end_location.lat, end_location.lon, api_key)

    cache = CacheUtility.read_cache(url, "here")
    if cache:
        return cache

    print("HERE: {} -> {}".format(start_location, end_location))

    response = requests.get(url)
    data = response.json()

    CacheUtility.write_cache(url, data, "here")

    end_time = time()
    print("HERE: {} seconds".format(end_time - start_time))
        
    turn_by_turn_actions = data['routes'][0]['sections'][0]['turnByTurnActions']
    max_turn_angle = 0
    for turn_by_turn_action in turn_by_turn_actions:
        if 'turnAngle' in turn_by_turn_action:
            turn_angle = abs(turn_by_turn_action['turnAngle'])
            if turn_angle > max_turn_angle:
                max_turn_angle = turn_angle
    
    print("HERE: Max turn angle: {}".format(max_turn_angle))

    return data



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
