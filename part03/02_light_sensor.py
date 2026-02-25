# 출처: PART 03. 다양한 센서 연동/01장. 환경 센서/02. 조도 센서.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: light_basic.py
from gpiozero import DigitalInputDevice    # 디지털 입력 장치 클래스
from time import sleep                      # 대기 함수

# 조도 센서를 GPIO 17번 핀에 연결
light_sensor = DigitalInputDevice(17)

print("조도 센서 테스트 시작")
print("센서를 손으로 가려보세요")

try:
    while True:
        if light_sensor.value == 0:
            print("밝음 (value=0)")      # 빛이 충분한 상태
        else:
            print("어두움 (value=1)")    # 빛이 부족한 상태

        sleep(0.5)    # 0.5초마다 상태 확인

except KeyboardInterrupt:
    print("\n종료합니다.")

# ==================================================

# filename: light_event.py
from gpiozero import DigitalInputDevice    # 디지털 입력 장치 클래스
from datetime import datetime              # 시간 표시를 위한 모듈
from signal import pause                   # 프로그램을 계속 실행 상태로 유지

# 조도 센서 초기화
light_sensor = DigitalInputDevice(17)

def on_dark():
    """어두워졌을 때 호출되는 함수 (value가 1이 될 때)."""
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] 어두워졌습니다!")

def on_light():
    """밝아졌을 때 호출되는 함수 (value가 0이 될 때)."""
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] 밝아졌습니다!")

# 상태 변화 시 호출할 함수를 연결합니다
light_sensor.when_activated = on_dark      # value가 0→1이 될 때 (밝음→어두움)
light_sensor.when_deactivated = on_light   # value가 1→0이 될 때 (어두움→밝음)

print("조도 변화 감지 중... (Ctrl+C로 종료)")

pause()    # 이벤트를 기다리며 프로그램을 계속 실행 상태로 유지

# ==================================================

# filename: auto_light.py
from gpiozero import LED, DigitalInputDevice    # LED와 디지털 입력 클래스
from signal import pause                          # 이벤트 대기

# 장치 초기화
led = LED(27)                         # LED - GPIO 27번 핀
light_sensor = DigitalInputDevice(17)  # 조도 센서 - GPIO 17번 핀

def update_light():
    """조도 상태에 따라 LED를 제어하는 함수."""
    if light_sensor.value == 1:    # 어두움 감지
        led.on()                   # LED 켜기
        print("조명 ON - 어두움 감지")
    else:                          # 밝음 감지
        led.off()                  # LED 끄기
        print("조명 OFF - 밝음 감지")

# 조도 변화 이벤트에 함수 연결
light_sensor.when_activated = update_light      # 어두워질 때
light_sensor.when_deactivated = update_light    # 밝아질 때

# 프로그램 시작 시 현재 상태를 반영합니다
update_light()

print("자동 조명 시스템 동작 중 (Ctrl+C로 종료)")
print("센서를 손으로 가려보세요")

pause()    # 이벤트를 기다립니다