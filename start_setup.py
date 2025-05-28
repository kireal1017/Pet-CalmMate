# 시작 프로그램은 /etc/systemd/system/petcalmmate_script.service 로 등록되어있음.
import RPi.GPIO as GPIO
import time, subprocess


def is_network_connected():
    try:
        result = subprocess.check_output(['nmcli', '-t', '-f', 'CONNECTIVITY', 'general'])  # nmcli 명령어로 네트워크 연결 상태 확인
        return result.strip() == b'full'                                                    # 'full' 상태면 연결됨
    except subprocess.CalledProcessError:
        return False

def wait_for_network(timeout=60):
    print("네트워크 연결 대기 중")
    start = time.time()
    while time.time() - start < timeout:
        if is_network_connected():
            print("네트워크 연결 확인됨 (nmcli)")
            return True
        time.sleep(1)
    print("네트워크 연결 실패 (timeout)")
    return False


# ----------------------------------------------------------------- 시작 -----------------------------------------------------------------

# 핀 설정
BUTTON_PIN = 17                     # 버튼 입력 핀
LED_STATE_ALLREADY = 23             # 대기 중 LED 출력 핀
LED_STATE_NET_ERROR = 22            # 네트워크 오류 LED 출력 핀
LED_STATE_POWER_ON = 27             # 전원 ON 상태 LED 출력 핀

# GPIO 설정 
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup([LED_STATE_ALLREADY, LED_STATE_NET_ERROR, LED_STATE_POWER_ON], GPIO.OUT, initial=GPIO.LOW) #처음에는모두 끔끔


is_power_on = False
mainprocess = None  # aws_project.py 프로세스 변수


while not wait_for_network(timeout=60):
    GPIO.output(LED_STATE_NET_ERROR, GPIO.HIGH)  # 네트워크 오류 LED 켜기
    print("네트워크 미연결 상태, 1초 후 재시도")
    time.sleep(1)
    

    
# if not wait_for_network(timeout=60):
#     print("네트워크 미연결 상태, 프로그램 종료")
#     exit(1)


print("버튼 제어 시작")
GPIO.output(LED_STATE_NET_ERROR, GPIO.LOW)  # 네트워크 오류 LED 끄기
GPIO.output(LED_STATE_ALLREADY, GPIO.HIGH)  # 대기 상태 LED 켜기

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            press_start = time.time()

            # 버튼이 눌린 동안 시간 측정
            while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                duration = time.time() - press_start

                # 3초 이상이면 즉시 전원 OFF
                if duration >= 3:
                    if is_power_on:
                        is_power_on = False
                        GPIO.output(LED_STATE_POWER_ON, GPIO.LOW)   # 전원 ON 상태 LED 끄기
                        GPIO.output(LED_STATE_ALLREADY, GPIO.HIGH)  # 대기 상태로 전환
                        print("전원 OFF")  
                        if mainprocess is not None:
                            mainprocess.terminate()
                            print(f"aws_project.py 프로세스 종료, 대기 상태 전환 (PID: {mainprocess.pid})")
                            mainprocess = None
                    else:
                        print("전원이 꺼져있음")

                    # 버튼이 떨어질 때까지 대기
                    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                        time.sleep(0.01)
                    break  # 바깥 루프로 돌아가기

                time.sleep(0.01)

            else:
                # 3초 미만 → 짧게 누른 것
                if duration >= 0.05:
                    if not is_power_on:
                        is_power_on = True
                        GPIO.output(LED_STATE_ALLREADY, GPIO.LOW)   # 대기 상태 LED 끄기
                        GPIO.output(LED_STATE_POWER_ON, GPIO.HIGH)  # 전원 ON 상태 LED 켜기
                        print("전원 ON")
                        mainprocess = subprocess.Popen(["python3", "aws_project.py"])  # aws_project.py 실행
                        print(f"aws_project.py 실행 중 (PID: {mainprocess.pid})")
                    else:
                        print("전원 켜짐")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n프로그램 종료")
finally:
    GPIO.cleanup()
