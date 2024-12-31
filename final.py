import http.client
import json  # Import the JSON module for parsing and formatting
import pandas as pd

# Prompt the user for inputs
from_entity = input("Enter the origin airport code (e.g., DEL for Delhi): ").strip()
to_entity = input("Enter the destination airport code (e.g., BOM for Mumbai): ").strip()
depart_date = input("Enter the departure date (YYYY-MM-DD): ").strip()
return_date = input("Enter the return date (YYYY-MM-DD): ").strip()
City = input("Enter the city name for hotel (e.g. Mumbai): ").strip()

# Connection to the SkyScanner API
conn = http.client.HTTPSConnection("sky-scanner3.p.rapidapi.com")

# Headers
headers = {
    'x-rapidapi-key': "7f1bea6bb4msh78929f2c5e64eefp1988d4jsnece92c6405d1",
    'x-rapidapi-host': "sky-scanner3.p.rapidapi.com"
}

# Construct request with query parameters
url = f"/flights/search-roundtrip?fromEntityId={from_entity}&toEntityId={to_entity}&departDate={depart_date}&returnDate={return_date}&adults=1&currency=INR"

# Send GET request
conn.request("GET", url, headers=headers)

# Response
res = conn.getresponse()
data = res.read()

# Parse JSON and pretty-print
try:
    parsed_data = json.loads(data)  # Parse the JSON response
    pretty_json = json.dumps(parsed_data, indent=4)  # Format the JSON with 4 spaces of indentation
except json.JSONDecodeError:
    print("Failed to parse JSON response.")




# Convert parsed JSON data into a DataFrame for easy manipulation
def process_itinerary_data(parsed_data):
    try:
        # Extract itineraries from the parsed JSON
        itineraries = parsed_data.get('data', {}).get('itineraries', [])
        processed_data = []
        
        for itinerary in itineraries:
            # Extract key details
            price = itinerary.get('price', {}).get('formatted', 'N/A')
            legs = itinerary.get('legs', [])
            
            # Collect details for each leg
            for leg in legs:
                leg_info = {
                    'Itinerary ID': itinerary.get('id', 'N/A'),
                    'Price': price,
                    'Origin': leg.get('origin', {}).get('name', 'N/A'),
                    'Destination': leg.get('destination', {}).get('name', 'N/A'),
                    'Departure': leg.get('departure', 'N/A'),
                    'Arrival': leg.get('arrival', 'N/A'),
                    'Duration (minutes)': leg.get('durationInMinutes', 'N/A'),
                    'Carrier': ', '.join([carrier.get('name', 'N/A') for carrier in leg.get('carriers', {}).get('marketing', [])]),
                }
                processed_data.append(leg_info)
        
        # Create a DataFrame
        df = pd.DataFrame(processed_data)
        return df

    except Exception as e:
        print(f"Error processing data: {e}")
        return None

# Example usage

processed_df = process_itinerary_data(parsed_data)

processed_df = processed_df.drop('Itinerary ID', axis=1)

df = processed_df

df['Departure'] = df['Departure'].str.replace('T', ' ').str.slice(0, 16)
df['Arrival'] = df['Arrival'].str.replace('T', ' ').str.slice(0, 16)

# Step 1: Remove ₹ and commas, convert to integer
df['Price'] = df['Price'].str.replace('₹', '', regex=False)  # Remove ₹
df['Price'] = df['Price'].str.replace(',', '', regex=False)  # Remove commas
df['Price'] = df['Price'].astype(int)  # Convert to integer

# Step 2: Sort the DataFrame by the Price column
df = df.sort_values(by='Price', ascending=True)

# Reset index if needed
df = df.reset_index(drop=True)

# Save the DataFrame to a CSV file named 'flights.csv', overwriting if it exists
df.to_csv('flights.csv', index=False)

print("DataFrame has been successfully saved to 'flights.csv'.")


import requests
import json
dest_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"



dest_params = {
    "query": City,  # Replace with your desired location
    "languagecode": "en-us"
}

# Headers
headers = {
	"x-rapidapi-key": "3cf4a51d9dmsh00a3b36b8746643p1d63cbjsn0a0868139292",
	"x-rapidapi-host": "booking-com15.p.rapidapi.com"
}

dest_response = requests.get(dest_url, headers=headers, params=dest_params)

formatted_dest_response = json.dumps(dest_response.json(), indent=4)


response_dict = json.loads(formatted_dest_response)

# Extract the first dest_id
dest_id = response_dict["data"][0]["dest_id"]


import requests
import json  # Import JSON module for formatting

url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"


params = {
    "dest_id": dest_id,
    "search_type": "CITY",
    "arrival_date": depart_date,
    "departure_date": return_date,
    "adults": 2,
    "room_qty": 1,
    "sort_by": "PRICE_ASC",
    "categories_filter": "budget",
    "units": "metric",
    "temperature_unit": "c",
    "languagecode": "en-us",
    "currency_code": "INR"
}
headers = {
	"x-rapidapi-key": "3cf4a51d9dmsh00a3b36b8746643p1d63cbjsn0a0868139292",
	"x-rapidapi-host": "booking-com15.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)

# Format the JSON response for readability
formatted_response = json.dumps(response.json(), indent=4)


import pandas as pd

# Assuming response contains the JSON response from the API call
try:
    data = response.json()  # Parse the JSON response
    hotels = data.get('data', {}).get('hotels', [])  # Extract the 'hotels' list from the JSON
    
    # Extract relevant hotel details into a structured list
    hotel_list = []
    for hotel in hotels:
        property_data = hotel.get('property', {})
        price_breakdown = property_data.get('priceBreakdown', {})
        
        hotel_info = {
            "Hotel Name": property_data.get('name', 'N/A'),
            "Review Score": property_data.get('reviewScore', 'N/A'),
            "Review Word": property_data.get('reviewScoreWord', 'N/A'),
            "Review Count": property_data.get('reviewCount', 'N/A'),
            "Gross Price": price_breakdown.get('grossPrice', {}).get('value', 'N/A'),
            "Currency": price_breakdown.get('grossPrice', {}).get('currency', 'N/A'),
            "Excluded Taxes ": price_breakdown.get('excludedPrice', {}).get('value', 'N/A'),
            "Strikethrough Price ": price_breakdown.get('strikethroughPrice', {}).get('value', 'N/A'),
            "Check-in Date": property_data.get('checkinDate', 'N/A'),
            "Check-out Date": property_data.get('checkoutDate', 'N/A'),
            "Location (Latitude)": property_data.get('latitude', 'N/A'),
            "Location (Longitude)": property_data.get('longitude', 'N/A'),
            "Photo URL": property_data.get('photoUrls', ['N/A'])[0],  # Get the first photo URL
        }
        hotel_list.append(hotel_info)
    
    # Convert to DataFrame for easy display and manipulation
    df = pd.DataFrame(hotel_list)
    
except Exception as e:
    print(f"Error processing data: {e}")

df1 = df[["Hotel Name", "Gross Price", "Check-in Date", "Check-out Date", "Photo URL"]]

# Sort the DataFrame by 'Gross Price' in ascending order
df1 = df1.sort_values(by="Gross Price", ascending=True)

# Reset the index if required
df1 = df1.reset_index(drop=True)



df1.to_csv('hotels.csv', index=False)

print("DataFrame has been successfully saved to 'hotels.csv'.")

import pandas as pd
import requests

url = "https://priceline-com2.p.rapidapi.com/cars/search"


querystring = {
    "pickUpLocation": to_entity,
    "dropOffLocation": to_entity,
    "pickUpDate": depart_date,
    "dropOffDate": return_date,
    "pickUpTime": "10:00",
    "dropOffTime": "10:00"
}

headers = {
    "x-rapidapi-key": "7f1bea6bb4msh78929f2c5e64eefp1988d4jsnece92c6405d1",
    "x-rapidapi-host": "priceline-com2.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Initialize an empty list to store vehicle data
vehicles_data = []

# Loop through the vehicles in the response
for vehicle in data.get('data', {}).get('vehicles', []):
    vehicle_info = {
        'Name': vehicle.get('name'),
        'Category': vehicle.get('categoryCodes', [None])[0],
        'Example': vehicle.get('example'),
        'Price': vehicle.get('rate', [{}])[0].get('totalPrice'),
        'Pickup Location': vehicle.get('pickupLocation', {}).get('line1'),
        'Return Location': vehicle.get('returnLocation', {}).get('line1'),
        'Fuel Type': vehicle.get('vehicleFeatures', {}).get('fuelType'),
        'AC': vehicle.get('vehicleFeatures', {}).get('isAC'),
        'Transmission': vehicle.get('vehicleFeatures', {}).get('transmission'),
        'People Capacity': vehicle.get('vehicleFeatures', {}).get('peopleCapacity'),
        'Image URL': vehicle.get('imageUrl')
    }
    vehicles_data.append(vehicle_info)

# Create DataFrame from the list of dictionaries
df = pd.DataFrame(vehicles_data)


df["Price"] = df["Price"] * 84

df2 = df[["Name","Price", "Category", "Example", "Pickup Location", "Return Location","People Capacity", "Image URL"]]
# Sort the DataFrame by 'Gross Price' in ascending order
df2 = df2.sort_values(by="Price", ascending=True)

# Reset the index if required
df2 = df2.reset_index(drop=True)

df2.to_csv('Cab.csv', index=False)

print("DataFrame has been successfully saved to 'Cab.csv'.")


import requests

url = "https://travel-guide-api-city-guide-top-places.p.rapidapi.com/check"

querystring = {"noqueue":"1"}

payload = {
	"region": City,
	"language": "en",
	"interests": ["historical", "cultural", "food"]
}
headers = {
	"x-rapidapi-key": "7f1bea6bb4msh78929f2c5e64eefp1988d4jsnece92c6405d1",
	"x-rapidapi-host": "travel-guide-api-city-guide-top-places.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, params=querystring)
import json
formatted_response = json.dumps(response.json(), indent=4)

import pandas as pd

# The response JSON from the API
response_data = response.json()

# Extract the 'result' data from the response
places_data = response_data.get("result", [])

# Convert the list of places data into a DataFrame
df = pd.DataFrame(places_data)

# If the coordinates are in a nested dictionary, expand them into separate columns
df_coordinates = pd.json_normalize(df['coordinates'])
df = pd.concat([df.drop(columns=['coordinates']), df_coordinates], axis=1)


df.to_csv('Activity.csv', index=False)

print("DataFrame has been successfully saved to 'Activity.csv'.")    