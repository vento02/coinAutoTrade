from flask import Flask, request, jsonify
import subprocess
import os
import requests

strategy = 1
#strategy 1이 돌파매매법임

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_request():
    data = request.json
    input_text = data.get('text', 'No text provided')

    # 여기에서 input_text를 처리하는 로직 구현

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

    response_text = f"Received text: {input_text}"
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)



def start_program():
    if strategy == 1:
        subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/start.sh"])
    elif strategy == 2:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/start2.sh"])
    elif strategy == 3:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/start3.sh"])
def stop_program():
    if strategy == 1:
        subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/stop.sh"])
    elif strategy == 2:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/stop2.sh"])
    elif strategy == 3:
        subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/stop3.sh"])

def check_program():
    subprocess.Popen(["bash", "/home/ubuntu/autoTrade-1/ProcessCheck.sh"])

def check_balance():
    process = subprocess.Popen(["python", "/home/ubuntu/autoTrade-1/test.py"], stdout=subprocess.PIPE)
    output, error = process.communicate()
    post_message("YOUR_SLACK_TOKEN", "YOUR_CHANNEL_ID", output.decode())

myToken = "xoxb-6162400799312-6162407511152-HCU70Srwok7XMokZmrvdGsxd"  # Access Token
myChannel = "비트코인-자동매매"  # 채널 이름 OR 채널 ID
def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)

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