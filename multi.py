from django.views.decorators.csrf import csrf_exempt
import subprocess
import os
import requests

myToken = "xoxb-6162400799312-6162407511152-HCU70Srwok7XMokZmrvdGsxd"  # Access Token
myChannel = "비트코인-자동매매"  # 채널 이름 OR 채널 ID
strategy = 1
#strategy 1이 돌파매매법임


@csrf_exempt
def slack_command(request):
    # POST 요청에서 데이터 추출
    input_text = request.POST.get('text', '')
    # 여기에서 input_text를 처리하는 로직 구현

    if "프로그램시작" in input_text:
        start_program()
    elif "프로그램중단" in input_text:
        stop_program()
    elif "프로그램확인" in input_text:
        check_program()
    elif "잔고확인" in input_text:
        check_balance()
    elif "매수목표가" in input_text:
        show_target_price()
    elif "매매기법" in input_text:
        strategy = int(input_text.split()[-1])
        change_trading_strategy(strategy)
    else:
        print("Invalid input")

def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)


def start_program():
    post_message(myToken, 
                 myChannel, 
                 "시스템 시작",
                 )
    if strategy == 1:
        subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/start.sh"])
    elif strategy == 2:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/start2.sh"])
    elif strategy == 3:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/start3.sh"])
def stop_program():
    post_message(myToken, 
                 myChannel, 
                 "시스템 중지",
                 )
    if strategy == 1:
        subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/stop.sh"])
    elif strategy == 2:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/stop2.sh"])
    elif strategy == 3:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/stop3.sh"])

def check_program():
    post_message(myToken, 
                 myChannel, 
                 "프로그램 작동 체크",
                 )
    subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/ProcessCheck.sh"])
    

def check_balance():
    post_message(myToken, 
                 myChannel, 
                 "잔고 확인",
                 )
    process = subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/test.py"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    post_message(myToken, 
                 myChannel, 
                 output.decode(),
                 )

def show_target_price():
    post_message(myToken, 
                 myChannel, 
                 "매수 목표가 확인",
                 )
    subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/Tprice_alertBot.sh"])

def change_trading_strategy(strategy):
    post_message(myToken, 
                 myChannel, 
                 "매매 기법 변환",
                 )
    if strategy == 1:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/strategy1.py"])
    elif strategy == 2:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/strategy2.py"])
    elif strategy == 3:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/strategy3.py"])
    else:
        print("Invalid strategy selected")