# 출처: PART 03. 다양한 센서 연동/02장. 거리 & 모션 센서/01. HC-SR04 초음파 센서.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: ultrasonic_basic.py
from gpiozero import DistanceSensor    # 거리 센서 클래스
from time import sleep                  # 대기 함수

# 초음파 센서 초기화
# echo: 수신 핀 (GPIO 24), trigger: 송신 핀 (GPIO 23)
sensor = DistanceSensor(echo=24, trigger=23)

print("초음파 센서 거리 측정 시작")
print("손을 센서 앞에 가까이 또는 멀리 해보세요")

try:
    while True:
        distance_m = sensor.distance          # 거리 읽기 (단위: 미터)
        distance_cm = distance_m * 100        # 미터를 센티미터로 변환

        print(f"거리: {distance_cm:.1f}cm")   # 소수점 한 자리로 표시

        sleep(0.5)    # 0.5초마다 측정

except KeyboardInterrupt:
    print("\n종료합니다.")

# ==================================================

# filename: ultrasonic_zone.py
from gpiozero import DistanceSensor, LED    # 거리 센서와 LED 클래스
from time import sleep                       # 대기 함수

# 장치 초기화
sensor = DistanceSensor(echo=24, trigger=23)    # 초음파 센서
led = LED(17)                                    # 경고 LED

print("거리 구간 감지 시작")

try:
    while True:
        distance = sensor.distance * 100    # cm 단위로 변환

        if distance > 50:
            # 50cm 이상 - 안전
            led.off()
            print(f"{distance:.1f}cm - 안전")
        elif distance > 20:
            # 20~50cm - 주의
            led.blink(on_time=0.3, off_time=0.3)    # 느린 깜빡임
            print(f"{distance:.1f}cm - 주의")
        else:
            # 20cm 미만 - 경고
            led.on()    # 계속 켜짐
            print(f"{distance:.1f}cm - 경고!")

        sleep(0.3)    # 0.3초마다 측정

except KeyboardInterrupt:
    print("\n종료합니다.")
    led.off()    # 종료 시 LED 끄기

# ==================================================

# filename: parking_assistant.py
from gpiozero import DistanceSensor, LED    # 거리 센서와 LED
from time import sleep                       # 대기 함수

# 장치 초기화
sensor = DistanceSensor(echo=24, trigger=23)    # 초음파 센서
led = LED(17)                                    # 경고 LED

print("주차 보조 시스템 시작")
print("물체를 센서에 가까이 가져가 보세요")

try:
    while True:
        d = sensor.distance * 100    # 거리 (cm)

        if d > 100:
            # 100cm 이상 - 진입 가능 구역
            led.off()
            status = "안전 - 진입 가능"
        elif d > 50:
            # 50~100cm - 서행 구역
            led.blink(on_time=0.5, off_time=0.5)    # 0.5초 간격 깜빡임
            status = "주의 - 천천히 이동"
        elif d > 20:
            # 20~50cm - 경고 구역
            led.blink(on_time=0.2, off_time=0.2)    # 0.2초 간격 빠른 깜빡임
            status = "경고 - 감속 필요"
        else:
            # 20cm 미만 - 정지 구역
            led.on()     # 계속 켜짐
            status = "정지!"

        print(f"거리: {d:5.1f}cm  |  {status}")
        sleep(0.3)    # 0.3초마다 갱신

except KeyboardInterrupt:
    print("\n종료합니다.")
    led.off()    # 종료 시 LED 끄기