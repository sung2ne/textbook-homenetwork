# 출처: PART 02. Python과 GPIO 제어/02장. GPIO 기초/01. GPIO 핀 구조.md
# 교재: 소설처럼 읽는 홈네트워크

# RPi.GPIO 방식 (복잡)
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)

# gpiozero 방식 (간단)
from gpiozero import LED
led = LED(17)
led.on()