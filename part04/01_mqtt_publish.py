# 출처: PART 04. MQTT와 IoT 통신/03. 센서 데이터 Publish.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: mqtt_publish_hello.py
import paho.mqtt.client as mqtt    # MQTT 클라이언트 라이브러리
import time                         # 시간 관련 함수

# MQTT 브로커 설정
BROKER = "localhost"    # 브로커 주소 (같은 라즈베리 파이)
PORT = 1883             # 기본 MQTT 포트
TOPIC = "home/test"     # 메시지를 보낼 Topic

# MQTT 클라이언트 생성
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# 브로커에 연결
client.connect(BROKER, PORT)

# 메시지 발행
client.publish(TOPIC, "안녕하세요 MQTT!")
print(f"'{TOPIC}' Topic으로 메시지를 보냈습니다.")

# 발행 후 잠시 대기 (전송 완료 보장)
time.sleep(0.5)

# 연결 종료
client.disconnect()

# ==================================================

# filename: mqtt_publish_json.py
import paho.mqtt.client as mqtt    # MQTT 클라이언트 라이브러리
import json                         # JSON 변환 라이브러리
import time                         # 시간 관련 함수
from datetime import datetime       # 날짜/시간 처리

# 브로커 설정
BROKER = "localhost"
PORT = 1883
TOPIC = "home/sensor/dht11"    # DHT11 데이터 Topic

# 클라이언트 생성 및 연결
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.connect(BROKER, PORT)

# 전송할 데이터 딕셔너리 생성
data = {
    "temperature": 25.3,                                   # 온도 (°C)
    "humidity": 60.5,                                       # 습도 (%)
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # 측정 시간
}

# 딕셔너리를 JSON 문자열로 변환
payload = json.dumps(data, ensure_ascii=False)    # ensure_ascii=False: 한글 유지

# JSON 메시지 발행
client.publish(TOPIC, payload)
print(f"발행 완료: {payload}")

time.sleep(0.5)     # 전송 완료 대기
client.disconnect()  # 연결 종료

# ==================================================

# filename: dht11_mqtt_publisher.py
import adafruit_dht                 # DHT11 라이브러리
import board                         # GPIO 핀 이름 모듈
import paho.mqtt.client as mqtt     # MQTT 클라이언트 라이브러리
import json                          # JSON 변환
import time                          # 시간 관련 함수
from datetime import datetime        # 날짜/시간 처리

# ---- 설정 ----
BROKER = "localhost"            # MQTT 브로커 주소
PORT = 1883                     # MQTT 포트
TOPIC = "home/sensor/dht11"    # 발행할 Topic
INTERVAL = 5                    # 측정 및 발행 간격 (초)

# ---- 장치 초기화 ----
dht = adafruit_dht.DHT11(board.D4)    # DHT11 센서 - GPIO 4번 핀

# ---- MQTT 연결 ----
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)    # 클라이언트 객체 생성
client.connect(BROKER, PORT)    # 브로커에 연결
client.loop_start()    # 백그라운드 네트워크 루프 시작 (연결 유지)

def read_dht11():
    """DHT11에서 온도와 습도를 읽습니다.

    최대 5번 시도하며, 성공하면 (온도, 습도) 반환.
    실패하면 (None, None) 반환.
    """
    for _ in range(5):        # 최대 5번 재시도
        try:
            temp = dht.temperature    # 온도 읽기
            hum = dht.humidity        # 습도 읽기
            if temp is not None and hum is not None:
                return temp, hum      # 성공 시 반환
        except RuntimeError:
            pass                      # 실패 시 다음 시도로
        time.sleep(1)                 # 재시도 전 1초 대기
    return None, None                 # 모든 시도 실패

print(f"DHT11 MQTT Publisher 시작")
print(f"브로커: {BROKER}:{PORT}")
print(f"Topic: {TOPIC}")
print(f"측정 간격: {INTERVAL}초")
print("Ctrl+C로 종료")

try:
    while True:
        temp, hum = read_dht11()    # 센서 데이터 읽기

        if temp is not None:
            # 전송할 데이터를 딕셔너리로 구성
            data = {
                "temperature": temp,                                        # 온도 (°C)
                "humidity": hum,                                             # 습도 (%)
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # 측정 시간
            }

            payload = json.dumps(data)    # 딕셔너리를 JSON 문자열로 변환

            result = client.publish(TOPIC, payload)    # MQTT로 발행

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"[{data['timestamp']}] 발행 성공: 온도 {temp}°C, 습도 {hum}%")
            else:
                print(f"발행 실패 (오류 코드: {result.rc})")
        else:
            print("센서 읽기 실패 - 건너뜀")

        time.sleep(INTERVAL)    # 다음 측정까지 대기

except KeyboardInterrupt:
    print("\n종료합니다.")
finally:
    client.loop_stop()    # 백그라운드 루프 중지
    client.disconnect()   # 브로커 연결 해제
    dht.exit()            # DHT11 센서 자원 해제