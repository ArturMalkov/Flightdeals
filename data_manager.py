import requests
from pprint import pprint

#you'll need create your own Google Sheet with 2 tabs: one with destinations containing threshold prices and another one with users
SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/048eff315fe5903f3238db08d1766717/flightDeals/prices"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/048eff315fe5903f3238db08d1766717/flightDeals/users"


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
            )
            print(response.text)

    def get_user_data(self):
        response = requests.get(SHEETY_USERS_ENDPOINT)
        data = response.json()
        self.user_data = data["users"]
        return self.user_data

# for row in range(len(result["prices"])):
#     print(result["prices"][row]["city"])

