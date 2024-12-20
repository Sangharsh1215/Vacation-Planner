import http.client

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

# Output response
print(data.decode("utf-8"))
