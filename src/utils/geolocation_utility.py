""" This module is responsible for the geolocation of the address. It uses the Here API to get the geolocation of the address and the reverse geolocation of the lat and lon. """
import requests


class GeolocationUtility:
    """ This class is responsible for the geolocation of the address. It uses the Here API to get the geolocation of the address and the reverse geolocation of the lat and lon."""

    @staticmethod
    def geolocate(address):
        """ This method is responsible for the geolocation of the address. It uses the Here API to get the geolocation of the address. """
        try:
            api_key = "KHKPpYn2p2aNvLQwUOA1TwbTRJa6n-ntaitcRBkCwag"

            url = "https://discover.search.hereapi.com/v1/geocode?q=%s&apiKey=%s" % (address,
                                                                                     api_key)
            response = requests.get(url, timeout=10)
            status_code = response.status_code
            response = response.json()
            if (status_code == 200):
                if (response["items"] and response["items"][0] and
                        response["items"][0]["position"] and response["items"][0]["scoring"]):
                    address = response["items"][0]["address"]["label"]
                    postal_code = response["items"][0]["address"]["postalCode"]
                    lat = response["items"][0]["position"]["lat"]
                    lon = response["items"][0]["position"]["lng"]
                    quality = response["items"][0]["scoring"]["queryScore"]

                    data = {
                        "lat": lat,
                        "lon": lon,
                        "quality_geolocation": quality,
                        "wrong": quality < 0.85,
                        "formatted_address": address,
                        "c_p": postal_code
                    }
                    return data

                return {
                    "Error": "Something went wront during the geolocation",
                    "wrong": True,
                    "quality": 0
                }
            else:
                return {
                    "Error": "Something went wront during the geolocation. Problem related to API",
                    "wrong": True,
                    "quality": 0
                }

        except Exception as e:
            print(e)
            return {
                "Error": "Something went wront during the geolocation",
                "Exception that caused the error": str(e),
                "wrong": True,
                "quality": 0
            }

    @staticmethod
    def reverse_geolocate(lat, lon):
        """ This method is responsible for the reverse geolocation of the lat and lon. It uses the Here API to get the reverse geolocation of the lat and lon."""
        try:
            api_key = "KHKPpYn2p2aNvLQwUOA1TwbTRJa6n-ntaitcRBkCwag"
            lat = str(lat)
            lon = str(lon)

            url = "https://revgeocode.search.hereapi.com/v1/revgeocode?at=%s,%s&lang=en-US&apiKey=%s" % (
                lat, lon, api_key)

            response = requests.get(url, timeout=10)
            status_code = response.status_code
            response = response.json()
            if (status_code == 200):
                if (response["items"], response["items"][0]["address"]):
                    address = response["items"][0]["address"]

                    data = {"address": response["items"][0]
                            ["title"], "detailedAddress": address}
                    return data

                return {
                    "Error": "Something went wront during the geolocation",
                    "wrong": True,
                    "quality": 0
                }
            else:
                return {
                    "Error": "Something went wront during the geolocation. Problem related to API",
                    "wrong": True,
                    "quality": 0
                }

        except Exception as e:
            print(e)
            return {
                "Error": "Something went wront during the geolocation",
                "Exception that caused the error": str(e),
                "wrong": True,
                "quality": 0
            }
