# 출처: PART 03. 다양한 센서 연동/02장. 거리 & 모션 센서/02. PIR 모션 센서.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: pir_basic.py
from gpiozero import MotionSensor    # 모션 센서 클래스
from time import sleep               # 대기 함수
from signal import pause             # 이벤트 대기

# PIR 센서 초기화 - GPIO 4번 핀
pir = MotionSensor(4)

def motion_detected():
    """움직임이 감지됐을 때 호출되는 함수."""
    print("움직임 감지!")

def motion_stopped():
    """움직임이 멈췄을 때 호출되는 함수."""
    print("움직임 없음...")

# 이벤트에 함수를 연결합니다
pir.when_motion = motion_detected       # 움직임 시작 시
pir.when_no_motion = motion_stopped     # 움직임 종료 시

print("PIR 센서 테스트")
print("안정화 대기 중... (약 30초)")
sleep(30)    # 센서 안정화를 위해 30초 대기
print("준비 완료! 앞에서 움직여 보세요.")

pause()    # 이벤트를 기다리며 계속 실행

# ==================================================

# filename: pir_alarm.py
from gpiozero import MotionSensor, LED    # 모션 센서와 LED 클래스
from time import sleep                     # 대기 함수
from signal import pause                   # 이벤트 대기
from datetime import datetime              # 시간 기록

# 장치 초기화
pir = MotionSensor(4)    # PIR 센서 - GPIO 4번 핀
led = LED(17)             # 경고 LED - GPIO 17번 핀

motion_count = 0    # 감지 횟수 카운터

def on_motion():
    """움직임 감지 시 실행되는 함수."""
    global motion_count              # 전역 변수 사용 선언
    motion_count += 1                # 감지 횟수 증가

    now = datetime.now().strftime("%H:%M:%S")    # 현재 시간
    print(f"[{now}] 침입 감지! (#{motion_count}회)")

    led.on()    # 경고 LED 켜기

def on_no_motion():
    """움직임이 멈췄을 때 실행되는 함수."""
    led.off()    # 경고 LED 끄기
    print("   대기 중...")

# 이벤트 연결
pir.when_motion = on_motion
pir.when_no_motion = on_no_motion

print("보안 시스템 활성화")
print("안정화 대기 중... (30초)")
sleep(30)    # 센서 안정화 대기
print("보안 모드 작동 중! (Ctrl+C로 종료)")

pause()    # 이벤트 대기

# ==================================================

# filename: pir_logger.py
from gpiozero import MotionSensor, LED    # 모션 센서와 LED 클래스
from time import sleep                     # 대기 함수
from signal import pause                   # 이벤트 대기
from datetime import datetime              # 시간 기록

# 장치 초기화
pir = MotionSensor(4)    # PIR 센서 - GPIO 4번 핀
led = LED(17)             # 경고 LED - GPIO 17번 핀

LOG_FILE = "motion_log.txt"    # 로그 파일 이름

def log(message):
    """타임스탬프와 함께 화면 출력 및 파일 저장."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # 날짜+시간
    line = f"[{now}] {message}"
    print(line)                              # 화면 출력
    with open(LOG_FILE, "a") as f:          # 파일에 추가 저장
        f.write(line + "\n")

def on_motion():
    """움직임 감지 시 실행."""
    led.on()           # LED 켜기
    log("움직임 감지!")

def on_no_motion():
    """움직임 종료 시 실행."""
    led.off()          # LED 끄기
    log("대기 중")

# 이벤트 연결
pir.when_motion = on_motion
pir.when_no_motion = on_no_motion

# 로그 파일 초기화
with open(LOG_FILE, "w") as f:
    f.write("=== 보안 로그 시작 ===\n")

print(f"보안 시스템 시작 (로그: {LOG_FILE})")
print("안정화 대기 중... (30초)")
sleep(30)    # 센서 안정화 대기
log("시스템 준비 완료")
print("Ctrl+C로 종료")

pause()    # 이벤트 대기