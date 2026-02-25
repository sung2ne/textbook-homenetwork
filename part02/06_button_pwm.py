# 출처: PART 02. Python과 GPIO 제어/02장. GPIO 기초/03. 버튼과 PWM.md
# 교재: 소설처럼 읽는 홈네트워크

# button_polling.py - 폴링 방식
from gpiozero import Button
from time import sleep

button = Button(4)

print("버튼 상태 확인 (Ctrl+C로 종료)")

while True:
    if button.is_pressed:
        print("버튼 눌림!")
    else:
        print("대기 중...")
    sleep(0.2)

# ==================================================

# button_event.py - 이벤트 방식
from gpiozero import Button
from signal import pause

button = Button(4)

def on_press():
    print("버튼 눌림!")

def on_release():
    print("버튼 뗌!")

button.when_pressed = on_press
button.when_released = on_release

print("버튼 이벤트 대기 중 (Ctrl+C로 종료)")
pause()

# ==================================================

# button_led.py - 버튼으로 LED 제어
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(4)

# 버튼 누르면 LED 켜기, 떼면 끄기
button.when_pressed = led.on
button.when_released = led.off

print("버튼을 누르면 LED가 켜집니다 (Ctrl+C로 종료)")
pause()

# ==================================================

# button_toggle.py - 버튼 토글
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(4)

button.when_pressed = led.toggle

print("버튼을 누를 때마다 LED가 토글됩니다 (Ctrl+C로 종료)")
pause()

# ==================================================

# button_hold.py - 길게 누르기 감지
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(4, hold_time=2)   # 2초 이상 누르면 held 이벤트

def on_short_press():
    print("짧게 눌림 - LED 토글")
    led.toggle()

def on_long_press():
    print("길게 눌림 (2초 이상) - LED 끄기")
    led.off()

button.when_pressed = on_short_press
button.when_held = on_long_press

print("짧게 누르면 토글, 길게(2초) 누르면 OFF (Ctrl+C로 종료)")
pause()

# ==================================================

# pwm_button.py - 버튼으로 밝기 조절
from gpiozero import PWMLED, Button
from signal import pause

led = PWMLED(17)
button = Button(4)

brightness_levels = [0.0, 0.25, 0.5, 0.75, 1.0]
current_level = 0

def increase_brightness():
    global current_level
    current_level = (current_level + 1) % len(brightness_levels)
    led.value = brightness_levels[current_level]
    print(f"밝기: {brightness_levels[current_level]*100:.0f}%")

button.when_pressed = increase_brightness

led.value = 0.0
print("버튼을 누를 때마다 밝기가 증가합니다 (Ctrl+C로 종료)")
pause()

# ==================================================

# servo_basic.py - 서보 기본 제어
from gpiozero import Servo
from time import sleep

servo = Servo(12)

print("서보 기본 제어")

print("최소 각도 (0도)")
servo.min()
sleep(1)

print("중간 각도 (90도)")
servo.mid()
sleep(1)

print("최대 각도 (180도)")
servo.max()
sleep(1)

print("중간으로 복귀")
servo.mid()
sleep(1)

print("완료!")

# ==================================================

# servo_angle.py - 각도 지정 제어
from gpiozero import AngularServo
from time import sleep

servo = AngularServo(12, min_angle=0, max_angle=180)

print("각도 순서대로 이동")
angles = [0, 45, 90, 135, 180, 90, 0]

for angle in angles:
    print(f"  각도: {angle}도")
    servo.angle = angle
    sleep(1)

print("완료!")

# ==================================================

# servo_smooth.py - 부드러운 서보 이동
from gpiozero import Servo
from time import sleep

servo = Servo(12)

print("부드러운 이동 (0도 → 180도)")
for i in range(-10, 11):
    servo.value = i / 10
    sleep(0.1)

sleep(0.5)

print("부드러운 이동 (180도 → 0도)")
for i in range(10, -11, -1):
    servo.value = i / 10
    sleep(0.1)

servo.mid()
print("완료!")

# ==================================================

# doorbell.py - 도어벨 시스템
from gpiozero import LED, Button, Buzzer
from time import sleep
from signal import pause

led = LED(17)
button = Button(4)
buzzer = Buzzer(18)

bell_count = 0

def ring_doorbell():
    global bell_count
    bell_count += 1
    print(f"딩동! (벨 #{bell_count})")

    led.on()

    # 딩 (짧게)
    buzzer.on()
    sleep(0.3)
    buzzer.off()
    sleep(0.1)

    # 동 (조금 길게)
    buzzer.on()
    sleep(0.5)
    buzzer.off()

    sleep(0.5)
    led.off()

button.when_pressed = ring_doorbell

print("도어벨 시스템 작동 중")
print("버튼을 눌러 벨을 울리세요 (Ctrl+C로 종료)")
pause()

# ==================================================

# door_control.py - 버튼으로 문 제어
from gpiozero import Button, Servo
from time import sleep
from signal import pause

button = Button(4)
servo = Servo(12)

is_open = False

def toggle_door():
    global is_open
    if is_open:
        print("문 닫는 중...")
        servo.min()
        sleep(0.5)
        print("문 닫힘")
        is_open = False
    else:
        print("문 여는 중...")
        servo.max()
        sleep(0.5)
        print("문 열림")
        is_open = True

servo.min()
button.when_pressed = toggle_door

print("버튼으로 문을 열고 닫습니다 (Ctrl+C로 종료)")
pause()