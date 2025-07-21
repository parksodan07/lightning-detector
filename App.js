import React, { useState } from 'react';
import { MapContainer, TileLayer, useMapEvents, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function LocationMarker({ onLocation }) {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      onLocation({ lat, lng });
    },
  });
  return null;
}

function App() {
  const [userLocation, setUserLocation] = useState(null);

  const handleLocation = async ({ lat, lng }) => {
    setUserLocation([lat, lng]);
    const response = await fetch("http://localhost:10000/check_lightning", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ latitude: lat, longitude: lng }),
    });
    const data = await response.json();
    if (data.nearby_lightnings.length > 0) {
      alert("⚡ 5km 내 번개 접근!");
    } else {
      alert("🌤️ 주변에 번개 없음");
    }
  };

  return (
    <div style={{ height: "100vh" }}>
      <MapContainer center={[36.5, 127.5]} zoom={7} style={{ height: "100%", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <LocationMarker onLocation={handleLocation} />
        {userLocation && <Marker position={userLocation} />}
      </MapContainer>
    </div>
  );
}

export default App;
