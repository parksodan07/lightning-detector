from flask import Flask, render_template, request, jsonify
from lightning_logic import collect_lightning_data, is_within_5km, get_latest_lightnings
from lightning_predictor import predict_lightning_path

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_lightnings', methods=['GET'])
    def get_lightnings():
        return jsonify(get_latest_lightnings())

    @app.route('/check_lightning', methods=['POST'])
    def check_lightning():
        data = request.get_json()
        lat = data['latitude']
        lon = data['longitude']
        near = is_within_5km(lat, lon)
        return jsonify({"nearby_lightnings": near})

    @app.route('/predict_path', methods=['GET'])
    def predict_path():
        path = predict_lightning_path()
        return jsonify({"path": path})

    return app

# ✅ 반드시 추가해야 실행됨!
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=10000)
