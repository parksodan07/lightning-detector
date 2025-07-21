import streamlit as st
from streamlit_folium import st_folium
import folium
import requests

st.set_page_config(layout="wide")
st.title("⚡ 실시간 번개 감지 시스템")

# 기본 위치 (대한민국 중심)
default_lat = 36.5
default_lon = 127.5

# 세션 상태 초기화
if "latitude" not in st.session_state:
    st.session_state.latitude = default_lat
if "longitude" not in st.session_state:
    st.session_state.longitude = default_lon

# 지도 표시 함수
def show_map():
    m = folium.Map(location=[st.session_state.latitude, st.session_state.longitude], zoom_start=8)

    # 마커 추가
    folium.Marker(
        [st.session_state.latitude, st.session_state.longitude],
        popup="선택 위치",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    # 예측 경로 표시 (Flask 서버에서 가져오기)
    try:
        res = requests.get("http://localhost:10000/predict_path")
        if res.status_code == 200:
            path = res.json().get("path", [])
            if path:
                folium.PolyLine(locations=path, color="red", weight=3).add_to(m)
    except Exception as e:
        st.error(f"예측 경로 가져오기 실패: {e}")

    # 지도 클릭 이벤트 처리
    map_data = st_folium(m, width=700, height=500)
    if map_data and map_data.get("last_clicked"):
        coords = map_data["last_clicked"]
        st.session_state.latitude = coords["lat"]
        st.session_state.longitude = coords["lng"]

# 지도 표시
show_map()

# 위치 출력
st.write(f"🧭 현재 선택 위치: 위도 `{st.session_state.latitude:.6f}`, 경도 `{st.session_state.longitude:.6f}`")

# 버튼 → Flask로 POST 요청
if st.button("⚡ 번개 감지 요청"):
    try:
        resp = requests.post(
            "http://localhost:10000/check_lightning",
            json={"latitude": st.session_state.latitude, "longitude": st.session_state.longitude},
            timeout=5
        )
        if resp.status_code == 200:
            result = resp.json()
            near = result.get("nearby_lightnings", [])
            if near:
                st.error("⚠️ 5km 이내에 번개가 감지되었습니다!")
                for l in near:
                    st.write(f" - 감지 위치: 위도 {l['lat']}, 경도 {l['lon']}")
            else:
                st.success("✅ 현재 위치는 안전합니다.")
        else:
            st.error(f"서버 응답 오류: {resp.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Flask 서버가 실행되고 있는지 확인하세요 (localhost:10000)")
    except Exception as e:
        st.error(f"오류 발생: {e}")
