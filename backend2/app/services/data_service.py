import requests

API_URL = "http://localhost:8000"

def get_medicines(user_id):
    r = requests.get(f"{API_URL}/medicamentos/{user_id}")
    return r.json()