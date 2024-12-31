import http.client
import json  # Import the JSON module for parsing and formatting
import pandas as pd

# Prompt the user for inputs
from_entity = input("Enter the origin airport code (e.g., DEL for Delhi): ").strip()
to_entity = input("Enter the destination airport code (e.g., BOM for Mumbai): ").strip()
depart_date = input("Enter the departure date (YYYY-MM-DD): ").strip()
return_date = input("Enter the return date (YYYY-MM-DD): ").strip()

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