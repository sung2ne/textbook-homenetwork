# 출처: PART 03. 다양한 센서 연동/01장. 환경 센서/01. DHT11 온습도 센서.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: dht11_basic.py
import adafruit_dht          # Adafruit DHT 라이브러리 불러오기
import board                  # 핀 번호 이름을 편하게 쓰기 위한 모듈
from time import sleep        # 대기 함수

# DHT11 센서 초기화 - GPIO 4번 핀 사용 (board.D4)
dht = adafruit_dht.DHT11(board.D4)

print("DHT11 온습도 센서 시작")

try:
    while True:
        try:
            temperature = dht.temperature    # 온도 읽기 (단위: °C)
            humidity = dht.humidity          # 습도 읽기 (단위: %)

            # None이 아닐 때만 출력 (센서가 값을 제대로 못 읽을 때 None 반환)
            if temperature is not None and humidity is not None:
                print(f"온도: {temperature}°C  |  습도: {humidity}%")
            else:
                print("센서 값 없음 - 다시 시도 중...")

        except RuntimeError as e:
            # DHT 센서는 가끔 읽기에 실패합니다 - 이것은 정상입니다
            # RuntimeError를 무시하고 다음 반복을 기다립니다
            print(f"읽기 실패 (정상): {e}")

        sleep(2)    # 반드시 2초 이상 기다려야 합니다

except KeyboardInterrupt:
    print("\nCtrl+C로 종료합니다.")
finally:
    dht.exit()    # 센서 자원을 해제합니다

# ==================================================

# filename: dht11_stable.py
import adafruit_dht          # Adafruit DHT 라이브러리
import board                  # GPIO 핀 이름 모듈
from time import sleep        # 대기 함수

# 센서 초기화
dht = adafruit_dht.DHT11(board.D4)

def read_dht11(retries=5):
    """재시도 포함 DHT11 읽기 함수.

    최대 retries번 시도하며, 성공하면 (온도, 습도) 튜플을 반환합니다.
    모두 실패하면 (None, None)을 반환합니다.
    """
    for attempt in range(retries):           # 최대 retries번 반복
        try:
            temp = dht.temperature           # 온도 읽기
            hum = dht.humidity               # 습도 읽기
            if temp is not None and hum is not None:
                return temp, hum             # 성공하면 즉시 반환
        except RuntimeError:
            pass                             # 실패하면 다음 시도로 넘어감
        sleep(1)                             # 재시도 전 1초 대기
    return None, None                        # 모든 시도 실패

print("안정적인 DHT11 읽기 시작")

try:
    while True:
        temp, hum = read_dht11()    # 재시도 함수 호출

        if temp is not None:
            print(f"온도: {temp}°C  |  습도: {hum}%")
        else:
            print("읽기 실패 - 센서 연결을 확인하세요")

        sleep(3)    # 측정 간격 3초

except KeyboardInterrupt:
    print("\n종료합니다.")
finally:
    dht.exit()    # 센서 자원 해제

# ==================================================

# filename: dht11_control.py
import adafruit_dht          # DHT11 라이브러리
import board                  # GPIO 핀 이름 모듈
from gpiozero import LED      # LED 제어를 위한 gpiozero
from time import sleep        # 대기 함수

# 장치 초기화
dht = adafruit_dht.DHT11(board.D4)    # DHT11 센서 (GPIO 4)
warning_led = LED(27)                   # 경고 LED (GPIO 27)

TEMP_THRESHOLD = 28    # 경고 온도 임계값 (°C)

def read_dht11():
    """DHT11 값을 읽어 (온도, 습도) 반환합니다."""
    for _ in range(5):
        try:
            temp = dht.temperature
            hum = dht.humidity
            if temp is not None and hum is not None:
                return temp, hum
        except RuntimeError:
            pass
        sleep(1)
    return None, None

print(f"온도 모니터링 시작 (경고 임계값: {TEMP_THRESHOLD}°C)")

try:
    while True:
        temp, hum = read_dht11()

        if temp is not None:
            print(f"온도: {temp}°C  |  습도: {hum}%", end="")

            if temp >= TEMP_THRESHOLD:
                warning_led.on()     # 임계값 이상이면 경고 LED 켜기
                print(f"  [경고] 온도 높음!")
            else:
                warning_led.off()    # 정상이면 LED 끄기
                print("  [정상]")
        else:
            print("센서 읽기 실패")

        sleep(3)    # 3초 간격으로 측정

except KeyboardInterrupt:
    print("\n종료합니다.")
    warning_led.off()    # 종료 시 LED 끄기
finally:
    dht.exit()    # 센서 자원 해제