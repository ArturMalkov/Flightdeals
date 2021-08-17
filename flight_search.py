import requests
from flight_data import FlightData
from pprint import pprint
import os

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY") #please register with Tequila to obtain your own API KEY


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, params=query, headers=headers)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):

        flight_search_endpoint = "https://tequila-api.kiwi.com/v2/search"

        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "flight_type": "round",
            "curr": "GBP",
            "max_stopovers": 0,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 0,
        }
        #
        headers = {"apikey": TEQUILA_API_KEY}
        #
        response = requests.get(url=flight_search_endpoint, headers=headers, params=query)

        try:
            data = response.json()["data"][0]
            print(f"{destination_city_code}: £{data['price']}")

        except IndexError:
            # query["max_stopovers"] = 1
            # response = requests.get(url=flight_search_endpoint, headers=headers, params=query)
            # data = response.json()["data"][0]

            print(f"No flights found for {destination_city_code}.")
            # flight_data = FlightData(
            #     price=data["price"],
            #     origin_city=data["route"][0]["cityFrom"],
            #     origin_airport=data["route"][0]["flyFrom"],
            #     destination_city=data["route"][1]["cityTo"],
            #     destination_airport=data["route"][1]["flyTo"],
            #     out_date=data["route"][0]["local_departure"].split("T")[0],
            #     return_date=data["route"][2]["local_departure"].split("T")[0],
            #     stop_overs=1,
            #     via_city=data["route"][0]["cityTo"]
            # )
            # return flight_data
            return None

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
            return flight_data
