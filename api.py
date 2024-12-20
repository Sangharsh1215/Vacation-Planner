import http.client
import json

# Connection to the SkyScanner API
conn = http.client.HTTPSConnection("sky-scanner3.p.rapidapi.com")

# Replace these with actual values
from_entity = "PARI"  # Origin (e.g., Paris)
to_entity = "LOND"  # Destination (e.g., London)
depart_date = "2024-12-20"  # Departure date (YYYY-MM-DD)
return_date = "2024-12-22"  # Return date (YYYY-MM-DD)

headers = {
    'x-rapidapi-key': "7f1bea6bb4msh78929f2c5e64eefp1988d4jsnece92c6405d1",
    'x-rapidapi-host': "sky-scanner3.p.rapidapi.com"
}

# Construct request with query parameters
url = f"/flights/search-roundtrip?fromEntityId={from_entity}&toEntityId={to_entity}&departDate={depart_date}&returnDate={return_date}&adults=1"

# Send GET request
conn.request("GET", url, headers=headers)

# Response
res = conn.getresponse()
data = res.read()

# Parse JSON response
response = json.loads(data.decode("utf-8"))

# Check for data and extract useful information
if "itineraries" in response:
    print("\nAvailable Flights:\n" + "=" * 50)
    for idx, itinerary in enumerate(response["itineraries"], start=1):
        price = itinerary.get("price", {}).get("formatted", "N/A")
        legs = itinerary.get("legs", [])

        print(f"\nFlight Option {idx}:\n" + "-" * 50)
        print(f"Price: {price}")

        for leg in legs:
            origin_city = leg.get("origin", {}).get("city", "Unknown")
            destination_city = leg.get("destination", {}).get("city", "Unknown")
            departure = leg.get("departure", "Unknown").replace("T", " ")
            arrival = leg.get("arrival", "Unknown").replace("T", " ")
            airline = leg.get("carriers", {}).get("marketing", [{}])[0].get("name", "Unknown Airline")

            print(f"\nSegment Details:")
            print(f"  Airline: {airline}")
            print(f"  From: {origin_city}")
            print(f"  To: {destination_city}")
            print(f"  Departure: {departure}")
            print(f"  Arrival: {arrival}")
else:
    print("No flight data available. Please check the API response or input parameters.")
