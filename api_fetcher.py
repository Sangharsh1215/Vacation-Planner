import requests
import os
from dotenv import load_dotenv

# Load API credentials from .env file
load_dotenv()
API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

# Get access token function
def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        return data['access_token']
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Test the function
if __name__ == "__main__":
    token = get_access_token()
    print("Access Token:", token)
