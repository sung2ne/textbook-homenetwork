# 출처: PART 06. AI와 함께하는 바이브코딩/01장. Gemini CLI 입문/03. 첫 번째 바이브코딩.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: led_blink.py
from gpiozero import LED      # gpiozero 라이브러리에서 LED 클래스 가져오기
from time import sleep         # 시간 지연을 위한 sleep 함수 가져오기

# GPIO 17번 핀에 연결된 LED 객체 생성
led = LED(17)

print("LED 깜빡이기 시작")

# 5번 반복하여 LED 깜빡임
for i in range(5):
    led.on()                   # LED 켜기
    print(f"LED ON ({i+1}/5)")
    sleep(1)                   # 1초 대기
    led.off()                  # LED 끄기
    print("LED OFF")
    sleep(1)                   # 1초 대기

print("깜빡이기 완료!")

# ==================================================

# filename: sensor_mqtt.py
import paho.mqtt.client as mqtt   # MQTT 클라이언트 라이브러리
import adafruit_dht                # DHT11 센서 라이브러리
import board                       # 핀 번호 상수
import json                        # JSON 변환
from time import sleep             # 시간 지연
from datetime import datetime      # 현재 시각

# MQTT 클라이언트 생성 및 연결
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)             # 클라이언트 객체 생성
client.connect("localhost", 1883)  # Mosquitto 브로커에 연결

# DHT11 센서 초기화 (GPIO 4번 핀)
dht_sensor = adafruit_dht.DHT11(board.D4)

print("MQTT 센서 데이터 발행 시작 (Ctrl+C로 종료)")

try:
    while True:
        try:
            # 온도와 습도 읽기
            temperature = dht_sensor.temperature   # 섭씨 온도
            humidity = dht_sensor.humidity         # 습도 (%)

            if temperature is not None:
                # JSON 형식으로 데이터 구성
                data = {
                    "temperature": temperature,
                    "humidity": humidity,
                    "timestamp": datetime.now().isoformat()  # ISO 8601 형식
                }

                # MQTT로 발행
                client.publish("sensor/dht11", json.dumps(data))
                print(f"발행: 온도={temperature}°C, 습도={humidity}%")

        except RuntimeError as e:
            # DHT11은 가끔 읽기 오류 발생, 무시하고 재시도
            print(f"센서 읽기 오류 (재시도): {e}")

        sleep(5)   # 5초 대기

except KeyboardInterrupt:
    print("\n종료 중...")
    client.disconnect()   # MQTT 연결 해제
    dht_sensor.exit()     # 센서 정리
    print("정상 종료 완료")