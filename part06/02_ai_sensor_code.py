# 출처: PART 06. AI와 함께하는 바이브코딩/02장. AI로 IoT 구현하기/01. 센서 코드 자동 생성.md
# 교재: 소설처럼 읽는 홈네트워크

# filename: env_monitor.py
from gpiozero import LED, OutputDevice, DigitalInputDevice  # GPIO 제어
import adafruit_dht                                          # DHT11 센서
import board                                                  # 핀 상수
from time import sleep                                        # 시간 지연
from datetime import datetime                                 # 현재 시각

# 각 장치 객체 초기화
led = LED(27)                           # GPIO 27번 핀의 LED
fan = OutputDevice(18)                  # GPIO 18번 핀의 팬 릴레이
light_sensor = DigitalInputDevice(17)   # GPIO 17번 핀의 조도 센서 (디지털)
dht = adafruit_dht.DHT11(board.D4)     # GPIO 4번 핀의 DHT11 센서

print("=" * 50)
print("   환경 모니터링 시스템 시작")
print("=" * 50)
print("종료: Ctrl+C\n")

try:
    while True:
        # 현재 시각 저장
        timestamp = datetime.now().strftime("%H:%M:%S")

        # DHT11에서 온습도 읽기
        try:
            temp = dht.temperature   # 섭씨 온도
            hum = dht.humidity       # 습도 (%)
        except RuntimeError:
            # DHT11은 간헐적으로 읽기 오류 발생
            temp = None
            hum = None

        # 조도 읽기 (1이면 어두움, 0이면 밝음)
        is_dark = (light_sensor.value == 1)

        # 온도 기반 팬 제어
        if temp is not None and temp >= 28:
            fan.on()          # 28도 이상이면 팬 켜기
            fan_status = "ON (고온)"
        else:
            fan.off()         # 28도 미만이면 팬 끄기
            fan_status = "OFF"

        # 조도 기반 LED 제어
        if is_dark:
            led.on()          # 어두우면 LED 켜기
            led_status = "ON (어두움)"
        else:
            led.off()         # 밝으면 LED 끄기
            led_status = "OFF"

        # 현재 상태 출력
        print(f"[{timestamp}] "
              f"온도: {temp}°C | "
              f"습도: {hum}% | "
              f"조도: {'어두움' if is_dark else '밝음'} | "
              f"팬: {fan_status} | "
              f"LED: {led_status}")

        sleep(5)   # 5초 대기

except KeyboardInterrupt:
    # Ctrl+C 입력 시 정상 종료
    print("\n시스템 종료")
    fan.off()    # 팬 끄기
    led.off()    # LED 끄기
    dht.exit()   # DHT11 센서 자원 해제