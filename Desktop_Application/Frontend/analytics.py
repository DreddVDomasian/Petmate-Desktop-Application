# analytics.py (desktop helper)
import requests
from config_loader import API_BASE_URL  # your app uses this already (from your upload)

def fetch_json(url):
    try:
        print(f"\nFetching: {url}")

        response = requests.get(url, timeout=5)

        print("STATUS:", response.status_code)
        print("RAW TEXT:", response.text)

        # Try decoding JSON
        try:
            data = response.json()
        except Exception as e:
            print("❌ ERROR: Response is NOT JSON!", e)
            return None

        print("PARSED JSON:", data)
        return data

    except Exception as e:
        print("❌ REQUEST FAILED:", e)
        return None



