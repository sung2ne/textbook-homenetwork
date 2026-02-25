# 출처: PART 06. AI와 함께하는 바이브코딩/02장. AI로 IoT 구현하기/03. 웹 대시보드 만들기.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: dashboard_server.py
from flask import Flask, jsonify, render_template_string   # 웹 서버
import paho.mqtt.client as mqtt                             # MQTT 클라이언트
import json                                                  # JSON 처리
import threading                                             # 백그라운드 실행

# Flask 앱 초기화
app = Flask(__name__)

# 최신 센서 데이터를 저장하는 전역 변수 (초기값 설정)
sensor_data = {
    "temperature": None,    # 온도 (아직 데이터 없음)
    "humidity": None,       # 습도
    "state": "연결 대기",    # 시스템 상태
    "timestamp": "N/A"      # 마지막 업데이트 시각
}

# ── MQTT 콜백 함수들 ──────────────────────────────────

def on_connect(client, userdata, flags, rc):
    """MQTT 브로커에 연결됐을 때 실행"""
    if rc == 0:
        print("MQTT 브로커 연결 성공")
        # 센서 데이터 토픽 구독 시작
        client.subscribe("sensor/environment")
    else:
        print(f"MQTT 연결 실패: 코드 {rc}")

def on_message(client, userdata, msg):
    """MQTT 메시지를 받았을 때 실행"""
    global sensor_data            # 전역 변수 수정
    try:
        # JSON 문자열을 Python 딕셔너리로 변환
        data = json.loads(msg.payload.decode())
        sensor_data.update(data)  # 최신 데이터로 업데이트
        print(f"데이터 수신: 온도 {data.get('temperature')}°C")
    except json.JSONDecodeError:
        print("JSON 파싱 오류")

# ── MQTT 클라이언트 설정 ──────────────────────────────

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)            # MQTT 클라이언트 생성
mqtt_client.on_connect = on_connect    # 연결 콜백 등록
mqtt_client.on_message = on_message    # 메시지 콜백 등록
mqtt_client.connect("localhost", 1883) # Mosquitto 브로커에 연결

# MQTT 루프를 별도 스레드에서 실행 (Flask와 동시 실행)
mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
mqtt_thread.daemon = True              # 메인 프로그램 종료 시 함께 종료
mqtt_thread.start()

# ── Flask 웹 엔드포인트 ───────────────────────────────

@app.route("/api/sensor")
def api_sensor():
    """최신 센서 데이터를 JSON으로 반환하는 API 엔드포인트"""
    return jsonify(sensor_data)

# HTML 대시보드 템플릿 (문자열로 직접 작성)
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>홈 IoT 대시보드</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; padding: 20px; }
        .card { background: white; border-radius: 8px; padding: 20px; margin: 10px;
                display: inline-block; width: 150px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
        .value { font-size: 2em; font-weight: bold; color: #333; }
        .label { color: #888; margin-top: 5px; }
        .status { padding: 8px 16px; border-radius: 20px; background: #4CAF50; color: white; }
        .status.hot { background: #f44336; }
    </style>
</head>
<body>
    <h1>홈 IoT 대시보드</h1>
    <div id="data-container">불러오는 중...</div>

    <script>
        // 2초마다 센서 데이터 새로고침
        function fetchData() {
            fetch('/api/sensor')
                .then(response => response.json())
                .then(data => {
                    // 데이터를 HTML로 변환해서 표시
                    document.getElementById('data-container').innerHTML = `
                        <div class="card">
                            <div class="value">${data.temperature ?? '--'}°C</div>
                            <div class="label">온도</div>
                        </div>
                        <div class="card">
                            <div class="value">${data.humidity ?? '--'}%</div>
                            <div class="label">습도</div>
                        </div>
                        <div>
                            <span class="status ${data.state === 'HOT' ? 'hot' : ''}">
                                상태: ${data.state ?? '연결 대기'}
                            </span>
                        </div>
                        <p style="color: #888; font-size: 0.9em;">
                            마지막 업데이트: ${data.timestamp ?? 'N/A'}
                        </p>
                    `;
                });
        }
        fetchData();              // 처음 로드 시 즉시 실행
        setInterval(fetchData, 2000);  // 2초마다 반복
    </script>
</body>
</html>
"""

@app.route("/")
def dashboard():
    """HTML 대시보드 페이지 반환"""
    return render_template_string(DASHBOARD_HTML)

# ── 서버 실행 ─────────────────────────────────────────

if __name__ == "__main__":
    print("대시보드 서버 시작: http://[라즈베리파이 IP]:5000")
    # host="0.0.0.0": 모든 네트워크 인터페이스에서 접속 허용 (같은 와이파이의 다른 기기도 접속 가능)
    app.run(host="0.0.0.0", port=5000, debug=False)