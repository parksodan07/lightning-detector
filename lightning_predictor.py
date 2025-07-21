from lightning_logic import lightning_data
import math

def predict_lightning_path():
    if len(lightning_data) < 2:
        return []

    path = []
    for i in range(len(lightning_data) - 1):
        p1 = lightning_data[i]
        p2 = lightning_data[i + 1]
        dir_lat = p2['latitude'] - p1['latitude']
        dir_lon = p2['longitude'] - p1['longitude']

        predicted_lat = p2['latitude'] + dir_lat
        predicted_lon = p2['longitude'] + dir_lon

        path.append({
            "from": {"lat": p2['latitude'], "lon": p2['longitude']},
            "to": {"lat": predicted_lat, "lon": predicted_lon}
        })
    return path
