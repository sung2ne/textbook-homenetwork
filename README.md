# 소설처럼 읽는 홈네트워크 - 실습 코드

**Raspberry Pi 5**로 배우는 IoT 홈네트워크 실습 코드 저장소입니다.
Docker + MQTT + Node-RED + Gemini CLI 바이브코딩을 활용한 스마트홈 프로토타입을 만들어봅니다.

📚 **교재**: [소설처럼 읽는 홈네트워크](https://text.ibetter.kr/home-network)

---

## 브랜치 구조

각 브랜치에는 해당 PART까지의 코드가 누적 포함됩니다.

| 브랜치 | 내용 |
|--------|------|
| `main` | 전체 코드 (PART 02~06) |
| `part02` | PART 02: Python과 GPIO 제어 |
| `part03` | PART 03: 다양한 센서 연동 (PART 02 포함) |
| `part04` | PART 04: MQTT와 IoT 통신 (PART 02~03 포함) |
| `part06` | PART 06: AI와 함께하는 바이브코딩 (PART 02~04 포함) |

## 실습 환경

- **보드**: Raspberry Pi 5 (Raspberry Pi OS 기반)
- **언어**: Python 3
- **소프트웨어 스택**:
  - `gpiozero` — GPIO 핀 제어
  - `adafruit-circuitpython-dht` — DHT11 온습도 센서
  - `paho-mqtt >= 2.0` — MQTT 클라이언트
  - `flask` — 웹 대시보드 (PART 06)
  - Mosquitto MQTT 브로커 (Docker)
  - Node-RED (Docker)

## 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/sung2ne/textbook-homenetwork.git
cd textbook-homenetwork

# 특정 PART 코드 확인
git checkout part04

# 의존성 설치 (Raspberry Pi에서)
pip install -r requirements.txt
```

## 파트별 코드 구조

```
part02/
├── 01_python_hello.py    # Python 개발 환경 확인
├── 02_datatypes.py       # 자료형과 제어문
├── 03_functions.py       # 함수와 모듈
├── 04_gpio_intro.py      # GPIO 핀 구조
├── 05_led_buzzer.py      # LED & 부저 제어
└── 06_button_pwm.py      # 버튼과 PWM

part03/
├── 01_dht11.py           # DHT11 온습도 센서
├── 02_light_sensor.py    # 조도 센서
├── 03_ultrasonic.py      # HC-SR04 초음파 센서
└── 04_pir_motion.py      # PIR 모션 센서

part04/
├── 01_mqtt_publish.py    # 센서 데이터 Publish
└── 02_mqtt_subscribe.py  # 원격 제어 Subscribe

part06/
├── 01_vibe_coding_example.py  # 첫 번째 바이브코딩 예제
├── 02_ai_sensor_code.py       # AI로 생성한 센서 코드
└── 03_web_dashboard.py        # Flask 웹 대시보드
```

## 주의사항

- 모든 Python 코드는 **Raspberry Pi 하드웨어에서 실행**해야 합니다.
- PC/Mac에서는 GPIO 관련 코드가 실행되지 않습니다.
- paho-mqtt 2.0 이상을 사용합니다. `CallbackAPIVersion.VERSION1` 명시가 필요합니다.

## 라이선스

MIT License — 교육 목적으로 자유롭게 사용 가능합니다.
