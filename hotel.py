import requests
import json
dest_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"

City = input("Enter the city name (e.g. Mumbai): ").strip()
arrival_date = input("Enter the arrival date (YYYY-MM-DD): ").strip()
departure_date = input("Enter the departure date (YYYY-MM-DD): ").strip()

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

# Extract the first `dest_id`
dest_id = response_dict["data"][0]["dest_id"]


import requests
import json  # Import JSON module for formatting

url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"


params = {
    "dest_id": dest_id,
    "search_type": "CITY",
    "arrival_date": arrival_date,
    "departure_date": departure_date,
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

# Assuming `response` contains the JSON response from the API call
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