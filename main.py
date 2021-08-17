from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LON" #please insert IATA code of your departure city

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
user_data = data_manager.get_user_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()


tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today,
    )

    if flight is None:
        continue

    if destination['lowestPrice'] > flight.price:
        notification_manager = NotificationManager()
        message=f"Low price alert! Only {flight.price}£ to fly from {flight.origin_city}-" \
                f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, " \
                f"from {flight.out_date} to {flight.return_date}.\nhttps://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}." \
                f"{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

        # if flight.stop_overs > 0:
        #     message += f"Flight has {flight.stop_overs} stop over, via {flight.via_city}."
        #     print(message)

        notification_manager.sending_message(message)

        for row in user_data:
            addressee = row["email"]
            message_text = f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
            notification_manager.send_emails(addressee, message_text)