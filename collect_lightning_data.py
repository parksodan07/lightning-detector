    import requests
    import pandas as pd
    from datetime import datetime, timedelta
    import os

    # --- 설정값 ---
    # ⚠️ 본인의 실제 기상청 날씨누리 OpenAPI 인증키로 변경해주세요.
    AUTH_KEY = "LuYp_PlVThimKfz5Vf4Ygw" # 예시 키, 본인 키로 변경 필요
    API_URL = "https://apihub.kma.go.kr/api/typ01/url/lgt_pnt.php" # 낙뢰 발생정보 조회 API URL
    SAVE_DIR = "C:\\Users\\이선희\\Desktop\\라이트닝프로젝트" # CSV 파일을 저장할 폴더 (현재 프로젝트 폴더)
    CSV_FILE_NAME = "recent_lightnings.csv" # 저장할 CSV 파일 이름
    # --- 설정값 끝 ---

    def collect_lightning_data_standalone():
        """
        기상청 API에서 최신 번개 데이터를 수집하여 CSV 파일로 저장합니다.
        이 함수는 APScheduler에 의해 주기적으로 실행됩니다.
        """
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 번개 데이터 수집 시작...")

        now_korea = datetime.now()
        time_start = now_korea - timedelta(hours=1)
        time_end = now_korea

        tm1 = time_start.strftime("%Y%m%d%H%M")
        tm2 = time_end.strftime("%Y%m%d%H%M")

        params = {
            "tm1": tm1,
            "tm2": tm2,
            "help": "1",
            "authkey": AUTH_KEY
        }

        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()

            data_lines = response.text.strip().split('\n')
            if data_lines and "lat" in data_lines[0] and "lon" in data_lines[0]:
                data_lines = data_lines[1:]

            lightning_data = []
            for line in data_lines:
                if ',' in line:
                    try:
                        lat, lon = map(float, line.split(','))
                        lightning_data.append({'lat': lat, 'lon': lon, 'timestamp': now_korea.strftime("%Y-%m-%d %H:%M:%S")})
                    except ValueError:
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 경고: 유효하지 않은 데이터 줄입니다: {line}")
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 경고: 예상치 못한 API 응답 형식입니다: {line}")

            if not lightning_data:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 수집된 번개 데이터가 없습니다.")
                return

            new_df = pd.DataFrame(lightning_data)

            csv_path = os.path.join(SAVE_DIR, CSV_FILE_NAME)
            if os.path.exists(csv_path):
                existing_df = pd.read_csv(csv_path)
                df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['lat', 'lon'], keep='last')
                df = df.sort_values(by='timestamp', ascending=False).head(200)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 기존 {CSV_FILE_NAME}에 데이터 추가 및 정리됨.")
            else:
                df = new_df
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 새 {CSV_FILE_NAME} 파일 생성됨.")

            df.to_csv(csv_path, index=False)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 번개 데이터가 {csv_path} 에 성공적으로 저장되었습니다.")

        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] API 요청 중 오류 발생: {e}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 데이터 처리 중 오류 발생: {e}")

    if __name__ == '__main__':
        collect_lightning_data_standalone()
    