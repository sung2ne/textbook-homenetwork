# 출처: PART 02. Python과 GPIO 제어/01장. Python 기초/03. 함수와 모듈.md
# 교재: 소설처럼 읽는 홈네트워크

# 함수의 기본 형태
def 함수이름(매개변수1, 매개변수2):
    # 함수 내부 코드
    return 반환값

# ==================================================

# 온도 상태를 판단하는 함수
def check_temperature(temperature):
    if temperature > 30:
        return "위험 (너무 더움)"
    elif temperature < 18:
        return "위험 (너무 추움)"
    else:
        return "정상"

# 함수 호출
status = check_temperature(35.0)
print(f"온도 상태: {status}")   # 온도 상태: 위험 (너무 더움)

status = check_temperature(22.5)
print(f"온도 상태: {status}")   # 온도 상태: 정상

# ==================================================

# 기본값이 있는 매개변수
def read_sensor(pin=17, unit="celsius"):
    # 실제로는 센서에서 읽지만, 여기서는 시뮬레이션
    value = 25.3
    print(f"핀 {pin}에서 {value}{unit} 읽음")
    return value

# 기본값 사용
read_sensor()              # 핀 17에서 25.3celsius 읽음
# 직접 값 지정
read_sensor(18, "°C")      # 핀 18에서 25.3°C 읽음

# ==================================================

def read_dht_sensor():
    # DHT11 센서 시뮬레이션
    temperature = 25.3
    humidity = 65.0
    return temperature, humidity

# 두 값을 한 번에 받기
temp, hum = read_dht_sensor()
print(f"온도: {temp}도, 습도: {hum}%")

# ==================================================

import time

# sleep: 지정한 초만큼 대기
print("시작")
time.sleep(2)   # 2초 대기
print("2초 후")

# 현재 시각 가져오기
current_time = time.time()         # 유닉스 타임스탬프
local_time = time.localtime()      # 로컬 시간 구조체
formatted = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
print(f"현재 시각: {formatted}")

# 경과 시간 측정
start = time.time()
time.sleep(1.5)
elapsed = time.time() - start
print(f"경과 시간: {elapsed:.2f}초")

# ==================================================

import random

# 정수 랜덤 값
pin_num = random.randint(1, 40)    # 1~40 사이 정수
print(f"랜덤 핀: {pin_num}")

# 실수 랜덤 값
temperature = random.uniform(18.0, 32.0)
print(f"랜덤 온도: {temperature:.1f}도")

# 리스트에서 랜덤 선택
devices = ["LED", "부저", "서보", "센서"]
selected = random.choice(devices)
print(f"선택된 장치: {selected}")

# ==================================================

# from 모듈 import 기능
from time import sleep, time
from random import uniform

# 이제 time. 없이 바로 사용
sleep(1)
temperature = uniform(18.0, 32.0)

# ==================================================

# 스마트 전구 클래스
class SmartBulb:
    def __init__(self, name, pin):
        self.name = name      # 이름
        self.pin = pin        # GPIO 핀 번호
        self.is_on = False    # 현재 상태
        self.brightness = 1.0 # 밝기 (0.0~1.0)

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} 켜짐 (밝기: {self.brightness*100:.0f}%)")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} 꺼짐")

    def set_brightness(self, level):
        if 0.0 <= level <= 1.0:
            self.brightness = level
            print(f"{self.name} 밝기: {level*100:.0f}%")
        else:
            print("밝기는 0.0~1.0 사이여야 합니다.")

    def status(self):
        state = "ON" if self.is_on else "OFF"
        return f"{self.name}: {state}, 밝기 {self.brightness*100:.0f}%"


# 클래스 사용
living_room = SmartBulb("거실 조명", pin=17)
bedroom = SmartBulb("침실 조명", pin=27)

living_room.turn_on()
living_room.set_brightness(0.5)
bedroom.turn_on()

print(living_room.status())
print(bedroom.status())

# ==================================================

# sensor_loop.py - 주기적 센서 읽기 루프
import time
import random

INTERVAL = 2      # 측정 간격 (초)
DURATION = 10     # 총 실행 시간 (초)


def read_temperature():
    """온도 센서 읽기 (시뮬레이션)"""
    return round(random.uniform(20.0, 32.0), 1)


def read_humidity():
    """습도 센서 읽기 (시뮬레이션)"""
    return round(random.uniform(40.0, 80.0), 1)


def check_environment(temp, hum):
    """환경 상태 판단"""
    warnings = []
    if temp > 30:
        warnings.append("고온 경보")
    if hum > 75:
        warnings.append("고습 경보")
    return warnings


def main():
    print(f"환경 모니터링 시작 ({DURATION}초간)")
    print(f"측정 간격: {INTERVAL}초")
    print("=" * 40)

    start_time = time.time()
    count = 0

    while time.time() - start_time < DURATION:
        count += 1
        temperature = read_temperature()
        humidity = read_humidity()
        warnings = check_environment(temperature, humidity)

        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {count:3d}회 | 온도: {temperature}도 | 습도: {humidity}%", end="")

        if warnings:
            print(f" | ⚠ {', '.join(warnings)}")
        else:
            print(" | 정상")

        time.sleep(INTERVAL)

    print("=" * 40)
    print(f"모니터링 완료 (총 {count}회 측정)")


main()