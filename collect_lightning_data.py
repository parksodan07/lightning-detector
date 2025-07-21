import requests
import os

def fetch_lightning_data():
    api_key = os.getenv("WEATHER_API_KEY")  # 환경 변수에서 키 불러오기

    if not api_key:
        raise ValueError("기상청 API 키가 설정되지 않았습니다.")

    url = f"https://apihub.kma.go.kr/api/typ01/url/to/lightning?authKey={api_key}&type=json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("⚠️ 번개 데이터 가져오기 실패:", e)
        return None
