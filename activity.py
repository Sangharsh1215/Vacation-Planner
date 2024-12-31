import requests

url = "https://travel-guide-api-city-guide-top-places.p.rapidapi.com/check"

querystring = {"noqueue":"1"}

payload = {
	"region": "Mumbai",
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
