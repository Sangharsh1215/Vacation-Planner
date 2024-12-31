import pandas as pd
import requests

url = "https://priceline-com2.p.rapidapi.com/cars/search"

pick_up_location = input("Enter the pickup location code (e.g., BOM for Mumbai): ").strip()
drop_off_location = input("Enter the drop-off location code (e.g., BOM for Mumbai): ").strip()
pick_up_date = input("Enter the pickup date (YYYY-MM-DD): ").strip()
drop_off_date = input("Enter the drop-off date (YYYY-MM-DD): ").strip()
pick_up_time = input("Enter the pickup time (HH:MM, 24-hour format): ").strip()
drop_off_time = input("Enter the drop-off time (HH:MM, 24-hour format): ").strip()

querystring = {
    "pickUpLocation": pick_up_location,
    "dropOffLocation": drop_off_location,
    "pickUpDate": pick_up_date,
    "dropOffDate": drop_off_date,
    "pickUpTime": pick_up_time,
    "dropOffTime": drop_off_time
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


