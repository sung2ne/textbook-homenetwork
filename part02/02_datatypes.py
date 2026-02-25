# 출처: PART 02. Python과 GPIO 제어/01장. Python 기초/02. 자료형과 제어문.md
# 교재: 소설처럼 읽는 홈네트워크

# 자료형과 변수 선언
temperature = 25.3      # 실수 (float)
humidity = 60           # 정수 (int)
room_name = "거실"      # 문자열 (str)
is_window_open = False  # 불린 (bool)

# 자료형 확인
print(type(temperature))   # <class 'float'>
print(type(humidity))      # <class 'int'>
print(type(room_name))     # <class 'str'>
print(type(is_window_open))# <class 'bool'>

# ==================================================

# 정수 (int): 소수점 없는 수
sensor_value = 1024
led_pin = 17
count = 0

# 실수 (float): 소수점 있는 수
temperature = 25.3
voltage = 3.3
duty_cycle = 0.75

# 사칙연산
total = sensor_value + 100    # 1124
half = sensor_value / 2       # 512.0 (나누기는 항상 float)
integer_div = sensor_value // 2  # 512 (몫만)
remainder = sensor_value % 3     # 1 (나머지)
power = 2 ** 10               # 1024 (거듭제곱)

# ==================================================

# 문자열 (str): 따옴표로 감쌈
device_name = "라즈베리 파이"
status = '동작 중'

# f-string: 변수를 문자열 안에 넣기 (가장 많이 씀)
temperature = 25.3
message = f"현재 온도: {temperature}도"
print(message)  # 현재 온도: 25.3도

# 문자열 메서드
print(device_name.upper())   # 라즈베리 파이 (영어면 대문자)
print(len(device_name))      # 글자 수
print("라즈베리" in device_name)  # True (포함 여부)

# ==================================================

# 불린 (bool): True 또는 False
is_running = True
has_error = False

# 비교 연산의 결과는 불린
temperature = 25.3
print(temperature > 30)   # False
print(temperature < 30)   # True
print(temperature == 25.3) # True
print(temperature != 30)  # True

# ==================================================

# IoT 예시: 온도에 따른 제어
temperature = 28.5

if temperature >= 30:
    print("너무 덥습니다. 에어컨을 켭니다.")
elif temperature >= 25:
    print("조금 덥습니다. 선풍기를 켭니다.")
elif temperature >= 20:
    print("적당합니다. 아무것도 하지 않습니다.")
else:
    print("춥습니다. 히터를 켭니다.")

# ==================================================

temperature = 28.5
humidity = 70

# and: 둘 다 True일 때
if temperature >= 28 and humidity >= 70:
    print("불쾌지수가 높습니다.")

# or: 하나라도 True일 때
if temperature >= 35 or humidity >= 90:
    print("매우 위험한 환경입니다.")

# not: 반전
is_door_open = False
if not is_door_open:
    print("문이 닫혀 있습니다.")

# ==================================================

# 5번 반복
for i in range(5):
    print(f"측정 {i+1}회: 센서 읽는 중...")

# range(시작, 끝, 간격)
for brightness in range(0, 101, 10):
    print(f"LED 밝기: {brightness}%")
    # 실제로는 led.value = brightness / 100 처럼 사용

# 리스트를 순서대로 처리
rooms = ["거실", "침실", "주방", "화장실"]
for room in rooms:
    print(f"{room} 조명 확인 중...")

# ==================================================

import time

# 온도가 정상 범위가 될 때까지 반복
temperature = 35

while temperature > 30:
    print(f"온도 {temperature}도 - 냉각 중...")
    temperature -= 1   # 1도씩 낮춰서 시뮬레이션
    time.sleep(0.5)

print(f"온도 정상화: {temperature}도")

# ==================================================

import time

# 무한 루프로 센서 모니터링
count = 0
while True:
    count += 1
    # 센서 읽기 시뮬레이션
    simulated_value = count * 2

    print(f"센서 값: {simulated_value}")

    if simulated_value >= 20:
        print("임계값 도달! 모니터링 중단.")
        break

    time.sleep(0.3)

# ==================================================

# print: 화면에 출력
temperature = 25.3
print("온도:", temperature)           # 온도: 25.3
print(f"온도: {temperature}도")       # 온도: 25.3도
print(f"온도: {temperature:.1f}도")  # 온도: 25.3도 (소수점 1자리)

# input: 키보드 입력 받기
name = input("이름을 입력하세요: ")
print(f"안녕하세요, {name}님!")

# 숫자 입력 (input은 항상 문자열로 받음, 변환 필요)
threshold = float(input("임계 온도를 입력하세요: "))
print(f"설정된 임계 온도: {threshold}도")

# ==================================================

# temperature_monitor.py - 온도 모니터링 시뮬레이터
import random
import time

TEMP_MIN = 18.0   # 최저 적정 온도
TEMP_MAX = 28.0   # 최고 적정 온도
MEASURE_COUNT = 10

print("온도 모니터링 시작")
print(f"적정 범위: {TEMP_MIN}~{TEMP_MAX}도")
print("-" * 30)

for i in range(MEASURE_COUNT):
    # 15~35도 사이의 랜덤 온도 생성
    temperature = round(random.uniform(15.0, 35.0), 1)

    if temperature > TEMP_MAX:
        status = "너무 더움"
        action = "에어컨 ON"
    elif temperature < TEMP_MIN:
        status = "너무 추움"
        action = "히터 ON"
    else:
        status = "적정"
        action = "유지"

    print(f"[{i+1:2d}] 온도: {temperature:5.1f}도 | 상태: {status} | 조치: {action}")
    time.sleep(0.5)

print("-" * 30)
print("모니터링 완료")