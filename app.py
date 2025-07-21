# app.py
from flask import Flask, render_template, jsonify, request
# (필요 시 다른 모듈 import)

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_lightnings')
    def get_lightnings():
        # 데이터 로직 불러오기
        pass

    @app.route('/check_lightning', methods=['POST'])
    def check_lightning():
        data = request.get_json()
        # 처리
        return jsonify({})

    @app.route('/predict_path')
    def predict_path():
        # 예측 로직
        return jsonify({})

    return app

# 로컬 개발용
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=10000)
