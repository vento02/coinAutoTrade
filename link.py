import subprocess
import os
import requests

def start_program():
    subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/start.sh"])

def stop_program():
    subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/stop.sh"])

def check_program():
    subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/ProcessCheck.sh"])

def check_balance():
    process = subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/test.py"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    post_message(slack_token, slack_channel, output.decode())

def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)

myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-자동매매"  # 채널 이름 OR 채널 ID

def calculate_profit():
    # 미구현
    pass

def show_target_price():
    subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/Tprice_alertBot.sh"])

def change_trading_strategy(strategy):
    if strategy == 1:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/strategy1.py"])
    elif strategy == 2:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/strategy2.py"])
    elif strategy == 3:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/strategy3.py"])
    else:
        print("Invalid strategy selected")

def respond_to_slack(input_text):
    if "프로그램 시작" in input_text:
        start_program()
    elif "프로그램 중단" in input_text:
        stop_program()
    elif "프로그램 확인" in input_text:
        check_program()
    elif "잔고 확인" in input_text:
        check_balance()
    elif "수익률" in input_text:
        calculate_profit()
    elif "매수목표가" in input_text:
        show_target_price()
    elif "매매 기법" in input_text:
        strategy = int(input_text.split()[-1])
        change_trading_strategy(strategy)
    else:
        print("Invalid input")

