# analytics.py (desktop helper)
import requests
from config_loader import API_BASE_URL  # your app uses this already (from your upload)

def fetch_daily_analytics():

    url = f"{API_BASE_URL}/api/analyticsAppointments"
    try:
        resp = requests.get(url, timeout=2)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        # fallback to zeros if API fails
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        values = [0]*7
        return days, values

    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    values = [int(data.get(d, 0)) for d in days]
    return days, values


