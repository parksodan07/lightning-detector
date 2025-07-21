import datetime
import random
from geopy.distance import geodesic

lightning_data = []

def collect_lightning_data():
    now = datetime.datetime.now().isoformat()
    lat = random.uniform(33.0, 38.0)
    lon = random.uniform(124.0, 130.0)
    lightning = {
        "timestamp": now,
        "latitude": lat,
        "longitude": lon,
        "intensity": random.randint(1, 5)
    }
    lightning_data.append(lightning)

def is_within_5km(lat, lon):
    user_loc = (lat, lon)
    return [l for l in lightning_data if geodesic(user_loc, (l['latitude'], l['longitude'])).km <= 5]
