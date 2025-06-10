# 시작 프로그램은 /etc/systemd/system/petcalmmate_script.service 로 등록되어있음. 
# 이 파일 수정할거면 sudo systemctl stop petcalmmate_script.service로 꺼둔 다음에 수정할것

import RPi.GPIO as GPIO
import time, subprocess, board, neopixel, threading, os

# 버튼 핀
BUTTON_PIN = 17

# 네오픽셀 설정
PIXEL_PIN = board.D18
NUM_PIXELS = 1
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.3, auto_write=True, pixel_order=neopixel.GRB)

# state 색상
COLOR_OFF = (0, 0, 0)
COLOR_YELLOW = (255, 150, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

# 상태 변수
is_power_on = False
mainprocess = None
last_network_check = 0
NETWORK_CHECK_INTERVAL = 10  # 초 단위로 체크함

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# 네트워크 연결 확인 함수
def is_network_connected():
    try:
        result = subprocess.check_output(['nmcli', '-t', '-f', 'CONNECTIVITY', 'general'])
        return result.strip() == b'full'
    except subprocess.CalledProcessError: # 네트워크 연결 실패시 false 반환
        return False

# 네트워크 연결 대기 + 점멸 애니메이션
def wait_for_network(timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        if is_network_connected():
            return True
        pixels[0] = COLOR_YELLOW
        time.sleep(0.3)
        pixels[0] = COLOR_OFF
        time.sleep(0.3)
    return False

def stream_stdout(pipe):
    for line in iter(pipe.readline, ''):
        print(f"[aws_project.py] {line.strip()}")

def start_mainprocess():
    global is_power_on, mainprocess
    if not is_power_on:
        try:
            # 명시적으로 nohup 사용하여 완전 분리
            command = (
                "sudo -u kireal1017 env HOME=/home/kireal1017 "
                "setsid nohup python3 /home/kireal1017/petcalmmate_project/aws_project.py "
                "> /tmp/aws_log.txt 2>&1 < /dev/null &"
            )
            
            subprocess.Popen(
                ["bash", "-c", command]
            )
            
            is_power_on = True
            pixels[0] = COLOR_GREEN
            print("전원 ON, aws_project.py 백그라운드로 실행")
        except Exception as e:
            print(f"메인 프로세스 실행 실패: {e}")
            is_power_on = False
    else:
        print("이미 실행 중")
        
    
def stop_mainprocess():
    global is_power_on, mainprocess
    if is_power_on:
        is_power_on = False
        if mainprocess:
            try:
                mainprocess.terminate()
                mainprocess.wait()
                mainprocess = None
            except Exception as e:
                print(f"프로세스 종료 실패: {e}")
        pixels[0] = COLOR_RED
        print("전원 OFF")
    else:
        print("이미 꺼져 있음")


# 시작 시 네트워크 연결 대기
while not wait_for_network(timeout=60):
    print("네트워크 연결 대기 중...")

pixels[0] = COLOR_RED  # 네트워크 연결 완료, 초기 대기 상태

time.sleep(5)   # 초기 대기 시간

# 메인 프로세스 시작
try:
    
    was_button_pressed = False
    press_start = 0
    long_press_handled = False

    while True:
        current_time = time.time()

        # 네트워크 상태 주기적 확인
        if current_time - last_network_check >= NETWORK_CHECK_INTERVAL:
            last_network_check = current_time
            if not is_network_connected():
                print("네트워크 끊김!")
                pixels[0] = COLOR_YELLOW
                stop_mainprocess()
            # else:
            #     print("네트워크 연결 유지 중")

        # 버튼 처리
        button_state = GPIO.input(BUTTON_PIN)

        if button_state == GPIO.LOW:
            if not was_button_pressed:
                press_start = time.time()
                was_button_pressed = True
                long_press_handled = False
                print("버튼 눌림 시작")

            duration = time.time() - press_start

            # if duration >= 3 and not long_press_handled:
            #     stop_mainprocess()
            #     print("메인 프로세스 종료")
            #     long_press_handled = True

        elif button_state == GPIO.HIGH and was_button_pressed:
            was_button_pressed = False
            duration = time.time() - press_start
            # print(f"버튼 뗀 시점: {time.time():.2f}")
            # print(f"총 누른 시간: {duration:.2f}초")

            if duration < 3 and duration >= 0.05 and not long_press_handled:
                start_mainprocess()
                print("메인 프로세스")
        

        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("\n종료 중...")

finally:
    if mainprocess:
        mainprocess.terminate()
    pixels.fill(COLOR_OFF)
    
    # 이 파일 수정할거면 sudo systemctl stop petcalmmate_script.service로 꺼둔 다음에 수정할것
