const map = L.map('map').setView([36.5, 127.5], 7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

function loadLightning() {
    fetch('/get_lightnings')
        .then(res => res.json())
        .then(data => {
            data.forEach(l => {
                L.circle([l.latitude, l.longitude], {
                    radius: 300,
                    color: 'red'
                }).addTo(map);
            });
        });
}

function loadPrediction() {
    fetch('/predict_path')
        .then(res => res.json())
        .then(data => {
            data.path.forEach(p => {
                L.polyline([
                    [p.from.lat, p.from.lon],
                    [p.to.lat, p.to.lon]
                ], {color: 'blue', dashArray: '5, 5'}).addTo(map);
            });
        });
}

map.on('click', function(e) {
    const lat = e.latlng.lat;
    const lon = e.latlng.lng;

    fetch('/check_lightning', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({latitude: lat, longitude: lon})
    })
    .then(res => res.json())
    .then(data => {
        if (data.nearby_lightnings.length > 0) {
            alert("⚠️ 5km 내에 번개가 접근 중입니다!");
        } else {
            alert("🌤️ 현재 주변에는 번개가 없습니다.");
        }
    });
});

loadLightning();
loadPrediction();
