# 출처: PART 04. MQTT와 IoT 통신/04. 원격 제어 Subscribe.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: mqtt_subscribe_basic.py
import paho.mqtt.client as mqtt    # MQTT 클라이언트 라이브러리

# 브로커 설정
BROKER = "localhost"
PORT = 1883
TOPIC = "home/control/test"    # 구독할 Topic

def on_connect(client, userdata, flags, rc):
    """브로커 연결 성공 시 호출되는 콜백 함수.

    rc=0이면 연결 성공, 다른 값이면 실패.
    """
    if rc == 0:
        print(f"브로커 연결 성공!")
        client.subscribe(TOPIC)    # 연결 성공 후 Topic 구독 등록
        print(f"'{TOPIC}' 구독 시작")
    else:
        print(f"연결 실패 (오류 코드: {rc})")

def on_message(client, userdata, msg):
    """메시지 수신 시 호출되는 콜백 함수.

    msg.topic: 수신한 Topic 이름
    msg.payload: 수신한 메시지 (bytes 타입)
    """
    topic = msg.topic                        # Topic 이름
    payload = msg.payload.decode("utf-8")    # bytes를 문자열로 변환

    print(f"수신 - Topic: {topic}, 메시지: {payload}")

# 클라이언트 생성 및 콜백 등록
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect    # 연결 이벤트 콜백
client.on_message = on_message    # 메시지 수신 이벤트 콜백

# 브로커 연결
client.connect(BROKER, PORT)

print("구독자 시작... (Ctrl+C로 종료)")

# 이벤트 루프 시작 - 메시지를 기다리며 계속 실행
client.loop_forever()

# ==================================================

# filename: mqtt_led_control.py
import paho.mqtt.client as mqtt    # MQTT 클라이언트 라이브러리
from gpiozero import LED           # LED 제어 클래스
from signal import pause            # 이벤트 대기

# ---- 설정 ----
BROKER = "localhost"
PORT = 1883
TOPIC = "home/control/led"    # LED 제어 Topic

# ---- 장치 초기화 ----
led = LED(27)    # GPIO 27번 핀에 연결된 LED

def on_connect(client, userdata, flags, rc):
    """브로커 연결 성공 시 자동 호출."""
    if rc == 0:
        print("브로커 연결 성공!")
        client.subscribe(TOPIC)    # LED 제어 Topic 구독
        print(f"'{TOPIC}' 구독 시작")
        print("명령 대기 중... (ON 또는 OFF)")

def on_message(client, userdata, msg):
    """메시지 수신 시 자동 호출."""
    command = msg.payload.decode("utf-8").strip().upper()    # 메시지를 대문자로 변환

    if command == "ON":
        led.on()                              # LED 켜기
        print("LED ON - 조명이 켜졌습니다.")
    elif command == "OFF":
        led.off()                             # LED 끄기
        print("LED OFF - 조명이 꺼졌습니다.")
    else:
        print(f"알 수 없는 명령: {command}")  # 예상 외 명령 처리

# 클라이언트 설정
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect    # 연결 콜백 등록
client.on_message = on_message    # 메시지 콜백 등록

# 브로커 연결 및 루프 시작
client.connect(BROKER, PORT)
client.loop_start()    # 백그라운드 루프 시작

print("LED 원격 제어 시작 (Ctrl+C로 종료)")
print("테스트: mosquitto_pub -h localhost -t home/control/led -m ON")

try:
    pause()    # 이벤트를 기다립니다
except KeyboardInterrupt:
    print("\n종료합니다.")
finally:
    client.loop_stop()     # 루프 종료
    client.disconnect()    # 연결 해제
    led.off()              # 종료 시 LED 끄기

# ==================================================

# filename: mqtt_advanced_control.py
import paho.mqtt.client as mqtt    # MQTT 클라이언트 라이브러리
import json                         # JSON 파싱
from gpiozero import LED            # LED 제어 클래스
from signal import pause             # 이벤트 대기

# ---- 설정 ----
BROKER = "localhost"
PORT = 1883
CONTROL_TOPIC = "home/control/led"    # 제어 명령 수신 Topic
STATUS_TOPIC = "home/status/led"      # 현재 상태 발행 Topic

# ---- 장치 초기화 ----
led = LED(27)    # GPIO 27번 핀 LED

def on_connect(client, userdata, flags, rc):
    """브로커 연결 성공 시 호출."""
    if rc == 0:
        print("브로커 연결 성공!")
        client.subscribe(CONTROL_TOPIC)    # 제어 Topic 구독
        print(f"'{CONTROL_TOPIC}' 구독 완료")

def on_message(client, userdata, msg):
    """메시지 수신 시 호출."""
    try:
        # 수신한 JSON 메시지를 딕셔너리로 변환
        command = json.loads(msg.payload.decode("utf-8"))

        action = command.get("action", "").upper()    # "action" 키 값 추출

        if action == "ON":
            led.on()                                      # LED 켜기
            status = {"state": "ON", "success": True}    # 상태 응답 데이터
            print("LED ON")

        elif action == "OFF":
            led.off()                                      # LED 끄기
            status = {"state": "OFF", "success": True}    # 상태 응답 데이터
            print("LED OFF")

        elif action == "BLINK":
            speed = command.get("speed", 1.0)              # 깜빡임 속도 (기본 1초)
            led.blink(on_time=speed, off_time=speed)       # 깜빡임 시작
            status = {"state": "BLINK", "speed": speed, "success": True}
            print(f"LED BLINK (속도: {speed}초)")

        else:
            status = {"state": "ERROR", "message": f"알 수 없는 명령: {action}", "success": False}
            print(f"알 수 없는 명령: {action}")

        # 현재 상태를 STATUS_TOPIC으로 발행 (피드백)
        client.publish(STATUS_TOPIC, json.dumps(status))

    except json.JSONDecodeError:
        # JSON 파싱 실패 시 처리
        print(f"JSON 파싱 오류: {msg.payload}")

# 클라이언트 설정
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_start()

print("고급 LED 제어 시스템 시작")
print('ON:    mosquitto_pub -h localhost -t home/control/led -m \'{"action": "ON"}\'')
print('OFF:   mosquitto_pub -h localhost -t home/control/led -m \'{"action": "OFF"}\'')
print('BLINK: mosquitto_pub -h localhost -t home/control/led -m \'{"action": "BLINK", "speed": 0.5}\'')

try:
    pause()
except KeyboardInterrupt:
    print("\n종료합니다.")
finally:
    client.loop_stop()
    client.disconnect()
    led.off()

# ==================================================

# filename: smart_home.py
import adafruit_dht                  # DHT11 라이브러리
import board                          # GPIO 핀 이름 모듈
import paho.mqtt.client as mqtt      # MQTT 클라이언트 라이브러리
import json                           # JSON 처리
import time                           # 시간 관련 함수
from gpiozero import LED              # LED 제어 클래스
from signal import pause              # 이벤트 대기
from datetime import datetime         # 날짜/시간 처리
import threading                      # 백그라운드 작업 실행

# ---- 설정 ----
BROKER = "localhost"
PORT = 1883
SENSOR_TOPIC = "home/sensor/dht11"     # 센서 데이터 발행 Topic
CONTROL_TOPIC = "home/control/led"     # LED 제어 명령 수신 Topic
PUBLISH_INTERVAL = 10                   # 센서 발행 간격 (초)

# ---- 장치 초기화 ----
dht = adafruit_dht.DHT11(board.D4)    # DHT11 센서 - GPIO 4번
led = LED(27)                           # LED - GPIO 27번

def read_dht11():
    """DHT11 값을 읽어 (온도, 습도) 반환."""
    for _ in range(5):
        try:
            temp = dht.temperature
            hum = dht.humidity
            if temp is not None and hum is not None:
                return temp, hum
        except RuntimeError:
            pass
        time.sleep(1)
    return None, None

def sensor_publisher(client):
    """백그라운드 스레드에서 주기적으로 센서 데이터를 발행."""
    while True:
        temp, hum = read_dht11()    # 센서 데이터 읽기

        if temp is not None:
            data = {
                "temperature": temp,
                "humidity": hum,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            payload = json.dumps(data)    # JSON 문자열로 변환
            client.publish(SENSOR_TOPIC, payload)    # 발행
            print(f"[발행] 온도: {temp}°C, 습도: {hum}%")

        time.sleep(PUBLISH_INTERVAL)    # 다음 발행까지 대기

def on_connect(client, userdata, flags, rc):
    """브로커 연결 성공 시 호출."""
    if rc == 0:
        client.subscribe(CONTROL_TOPIC)    # LED 제어 Topic 구독
        print("브로커 연결 및 구독 완료!")

        # 백그라운드 스레드로 센서 발행 시작
        thread = threading.Thread(target=sensor_publisher, args=(client,), daemon=True)
        thread.start()

def on_message(client, userdata, msg):
    """LED 제어 메시지 수신 시 호출."""
    command = msg.payload.decode("utf-8").strip().upper()    # 메시지 수신

    if command == "ON":
        led.on()          # LED 켜기
        print("[수신] LED ON")
    elif command == "OFF":
        led.off()         # LED 끄기
        print("[수신] LED OFF")
    else:
        print(f"[수신] 알 수 없는 명령: {command}")

# 클라이언트 설정
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("스마트홈 시스템 시작")
print(f"센서 발행: {SENSOR_TOPIC} (매 {PUBLISH_INTERVAL}초)")
print(f"LED 제어: {CONTROL_TOPIC}")

try:
    client.loop_forever()    # 메인 MQTT 루프 (블로킹)
except KeyboardInterrupt:
    print("\n종료합니다.")
finally:
    led.off()
    dht.exit()