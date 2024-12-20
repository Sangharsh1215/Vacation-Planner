import requests
import json  # Import JSON module for formatting

url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"

# Query Parameters
params = {
    "dest_id": "-2092174",
    "search_type": "CITY",
    "arrival_date": "2024-12-25",
    "departure_date": "2024-12-30",
    "adults": 2,
    "children_age": "0,5,10",
    "room_qty": 1,
    "page_number": 1,
    "price_min": 100,
    "price_max": 500,
    "sort_by": "PRICE_ASC",
    "categories_filter": "luxury,budget",
    "units": "metric",
    "temperature_unit": "c",
    "languagecode": "en-us",
    "currency_code": "USD"
}

headers = {
    "x-rapidapi-key": "7f1bea6bb4msh78929f2c5e64eefp1988d4jsnece92c6405d1",
    "x-rapidapi-host": "booking-com15.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)

# Format the JSON response for readability
formatted_response = json.dumps(response.json(), indent=4)

# Print the readable JSON response
print(formatted_response)
