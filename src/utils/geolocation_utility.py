import requests


class GeolocationUtility:

    def geolocate(address):
        try:
            apiKey = "KHKPpYn2p2aNvLQwUOA1TwbTRJa6n-ntaitcRBkCwag"

            url = "https://discover.search.hereapi.com/v1/geocode?q=%s&apiKey=%s" % (
                address, apiKey)
            response = requests.get(url)
            statusCode = response.status_code
            response = response.json()
            if (statusCode == 200):
                if (response["items"] and response["items"][0] and response["items"][0]["position"] and response["items"][0]["scoring"]):
                    address = response["items"][0]["address"]["label"]
                    postalCode = response["items"][0]["address"]["postalCode"]
                    lat = response["items"][0]["position"]["lat"]
                    lon = response["items"][0]["position"]["lng"]
                    quality = response["items"][0]["scoring"]["queryScore"]

                    data = {
                        "lat": lat,
                        "lon": lon,
                        "quality_geolocation": quality,
                        "wrong": quality < 0.85,
                        "formatted_address": address,
                        "c_p": postalCode
                    }
                    return data

                return {"Error": "Something went wront during the geolocation", "wrong": True, "quality": 0}
            else:
                return {"Error": "Something went wront during the geolocation. Problem related to API", "wrong": True, "quality": 0}

        except Exception as e:
            print(e)
            return {"Error": "Something went wront during the geolocation", "Exception that caused the error": str(e), "wrong": True, "quality": 0}

    def reverseGeolocate(lat, lon):
        try:
            apiKey = "KHKPpYn2p2aNvLQwUOA1TwbTRJa6n-ntaitcRBkCwag"
            lat = str(lat)
            lon = str(lon)

            url = "https://revgeocode.search.hereapi.com/v1/revgeocode?at=%s,%s&lang=en-US&apiKey=%s" % (
                lat, lon, apiKey)

            response = requests.get(url)
            statusCode = response.status_code
            response = response.json()
            if (statusCode == 200):
                if (response["items"], response["items"][0]["address"]):
                    address = response["items"][0]["address"]

                    data = {
                        "address": response["items"][0]["title"],
                        "detailedAddress": address
                    }
                    return data

                return {"Error": "Something went wront during the geolocation", "wrong": True, "quality": 0}
            else:
                return {"Error": "Something went wront during the geolocation. Problem related to API", "wrong": True, "quality": 0}

        except Exception as e:
            print(e)
            return {"Error": "Something went wront during the geolocation", "Exception that caused the error": str(e), "wrong": True, "quality": 0}
