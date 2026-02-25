# 출처: PART 02. Python과 GPIO 제어/02장. GPIO 기초/02. LED & 부저 제어.md
# 교재: 소설처럼 읽는 홈네트워크

# led_basic.py - LED 기본 제어
from gpiozero import LED
from time import sleep

led = LED(17)   # BCM 17번 핀

print("LED 제어 시작")

print("LED ON")
led.on()
sleep(2)

print("LED OFF")
led.off()
sleep(1)

print("LED 토글 5회")
for i in range(5):
    led.toggle()
    print(f"  Toggle {i+1}/5")
    sleep(0.5)

led.off()
print("완료!")

# ==================================================

# led_blink.py - 자동 깜빡임 패턴
from gpiozero import LED
from time import sleep

led = LED(17)

print("패턴 1: 기본 깜빡임 (0.5초 간격)")
led.blink(on_time=0.5, off_time=0.5)
sleep(3)

print("패턴 2: 빠른 깜빡임 (0.1초 간격)")
led.blink(on_time=0.1, off_time=0.1)
sleep(3)

print("패턴 3: 비대칭 (켜짐 길게)")
led.blink(on_time=0.8, off_time=0.2)
sleep(4)

print("패턴 4: 비대칭 (꺼짐 길게, 경보 패턴)")
led.blink(on_time=0.1, off_time=0.9)
sleep(5)

led.off()
print("완료!")

# ==================================================

# led_pwm.py - PWM 밝기 조절
from gpiozero import PWMLED
from time import sleep

led = PWMLED(17)

print("밝기 단계별 변화")
for brightness in [0.0, 0.25, 0.5, 0.75, 1.0]:
    led.value = brightness
    print(f"  밝기: {brightness*100:.0f}%")
    sleep(1)

print("\nFade In (서서히 밝아지기)")
for i in range(0, 101, 2):
    led.value = i / 100
    sleep(0.03)

print("Fade Out (서서히 어두워지기)")
for i in range(100, -1, -2):
    led.value = i / 100
    sleep(0.03)

led.off()
print("완료!")

# ==================================================

# led_pulse.py - 숨쉬기 효과
from gpiozero import PWMLED
from signal import pause

led = PWMLED(17)
led.pulse(fade_in_time=1, fade_out_time=1)

print("LED 숨쉬기 효과 (Ctrl+C로 종료)")
pause()

# ==================================================

# led_sos.py - SOS 모스부호
from gpiozero import LED
from time import sleep

led = LED(17)

def dot():
    """짧은 신호 (.)"""
    led.on()
    sleep(0.2)
    led.off()
    sleep(0.2)

def dash():
    """긴 신호 (-)"""
    led.on()
    sleep(0.6)
    led.off()
    sleep(0.2)

def letter_gap():
    """문자 간 간격"""
    sleep(0.4)

print("SOS 신호 전송 (3회)")

for i in range(3):
    print(f"SOS {i+1}/3")
    dot(); dot(); dot()     # S: ...
    letter_gap()
    dash(); dash(); dash()  # O: ---
    letter_gap()
    dot(); dot(); dot()     # S: ...
    sleep(1.5)

led.off()
print("완료!")

# ==================================================

# buzzer_basic.py - 부저 기본 제어
from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(18)

print("짧은 비프 3회")
for _ in range(3):
    buzzer.on()
    sleep(0.1)
    buzzer.off()
    sleep(0.2)

sleep(0.5)

print("긴 비프 1회")
buzzer.on()
sleep(1.0)
buzzer.off()

print("완료!")

# ==================================================

# buzzer_beep.py - 자동 비프
from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(18)

print("빠른 비프 5회")
buzzer.beep(on_time=0.1, off_time=0.1, n=5)
sleep(2)

print("느린 비프 3회")
buzzer.beep(on_time=0.5, off_time=0.5, n=3)
sleep(4)

print("완료!")

# ==================================================

# alert_system.py - LED + 부저 경보
from gpiozero import LED, Buzzer
from time import sleep

led = LED(17)
buzzer = Buzzer(18)

def alert(count=3):
    """경보 발생: LED 점멸 + 부저 비프"""
    print(f"경보 발생! ({count}회)")
    for i in range(count):
        led.on()
        buzzer.on()
        sleep(0.3)
        led.off()
        buzzer.off()
        sleep(0.2)

def clear_alert():
    """경보 해제: 긴 비프 1회"""
    print("경보 해제")
    led.on()
    buzzer.on()
    sleep(1.0)
    led.off()
    buzzer.off()

# 시뮬레이션
print("정상 상태...")
sleep(2)

alert(count=5)
sleep(1)

clear_alert()
print("시스템 정상화")