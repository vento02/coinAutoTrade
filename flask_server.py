import logging
import json
from datetime import datetime
from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import subprocess
import requests
import os
 
token = os.environ["Slack_Token"]
app = Flask(__name__)
client = WebClient(token)
absolutePath = "/home/ubuntu/autoTrade/"
myChannel = "비트코인-자동매매-1"
 
def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)
 
def get_day_of_week():
    weekday_list = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
 
    weekday = weekday_list[datetime.today().weekday()]
    date = datetime.today().strftime("%Y년 %m월 %d일")
    result = '{}({})'.format(date, weekday)
    return result
 
def get_time():
    return datetime.today().strftime("%H시 %M분 %S초")
 
 
def get_answer(text):
    trim_text = text.replace(" ", "")
 
    answer_dict = {
        '시작1': '돌파매매법 매매프로그램을 시작합니다.',
        '시작2': 'RSI매매법 매매프로그램을 시작합니다.',
        '정지1': '실행중인 돌파매매법 매매프로그램을 중지합니다.',
        '정지2': '실행중인 RSI매매법 매매프로그램을 중지합니다.',
        '잔고확인': '현재 잔고입니다.',
        '작동확인1': '돌파매매법 프로그램이 작동중인지 확인합니다.',
        '작동확인2': 'RSI매매법 프로그램이 작동중인지 확인합니다.',
        '가격1': '현재 매수목표가와 현재가를 확인합니다.',
        '가격2': '현재 RSI지수와 현재가를 확인합니다.',
        '돌파매매법': '돌파매매법으로 매매법을 교체합니다.',
        'RSI매매법': 'RSI매매법으로 매매법을 교체합니다',
        '매매기법': "현재 매매기법으로는 '돌파매매법'과 'RSI매매법'이 있습니다. 매매법을 변경하고 싶으시다면, 매매법의 이름을 명령어로 입력해주세요."
    }



    if "시작1" in trim_text:
        start_program1()
    elif "시작2" in trim_text:
        start_program2()
    elif "정지1" in trim_text:
        stop_program1()
    elif "정지2" in trim_text:
        stop_program2()
    elif "작동확인1" in trim_text:
        check_program1()
    elif "작동확인2" in trim_text:
        check_program2()
    elif "잔고확인" in trim_text:
        check_balance()
    elif "가격1" in trim_text:
        show_target_price1()
    elif "가격2" in trim_text:
        show_target_price2()
    elif "돌파매매법" in trim_text:
        change_trading_strategy1()
    elif "RSI매매법" in trim_text:
        change_trading_strategy2()
    else:
        print("Invalid input")

 
    if trim_text == '' or None:
        return "알 수 없는 질의입니다. 답변을 드릴 수 없습니다."
    elif trim_text in answer_dict.keys():
        return answer_dict[trim_text]
    else:
        for key in answer_dict.keys():
            if key.find(trim_text) != -1:
                return "연관 단어 [" + key + "]에 대한 답변입니다.\n" + answer_dict[key]
 
        for key in answer_dict.keys():
            if answer_dict[key].find(text[1:]) != -1:
                return "질문과 가장 유사한 질문 [" + key + "]에 대한 답변이에요.\n"+ answer_dict[key]
    

    return text + "은(는) 없는 질문입니다."
 
 
def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    string_slack_event = str(slack_event)
 
    print(string_slack_event)
 
    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:
        try:
            if event_type == 'app_mention':
                user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
                answer = get_answer(user_query)
                result = client.chat_postMessage(channel=channel,
                                                 text=answer)
            return make_response("ok", 200, )
        except IndexError:
            pass
    # Direct Call 추가
    
    message = "[%s] cannot find event handler" % event_type
 
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


def start_program1():
    subprocess.Popen(["bash", absolutePath+"start.sh"])

def start_program2():
    subprocess.Popen(["bash", absolutePath+"startRsi.sh"])

def stop_program1():
    subprocess.Popen(["bash", absolutePath+"stop.sh"])

def stop_program2():
    subprocess.Popen(["bash", absolutePath+"stopRsi.sh"])

def check_program1():
    subprocess.Popen(["bash", absolutePath+"ProcessCheck.sh"])
    
    
def check_program2():
    subprocess.Popen(["bash", absolutePath+"RsiProcessCheck.sh"])
    
def check_balance():
    process = subprocess.Popen(["bash", absolutePath+"balance.sh"])

def show_target_price1():
        subprocess.Popen(["bash", absolutePath+"Tprice_alertBot.sh"])
    
def show_target_price2():
    subprocess.Popen(["bash", absolutePath+"RsiPrice_alertBot.sh"])

def change_trading_strategy1():
    subprocess.Popen(["bash", absolutePath+"stopRsi.sh"])
    start_program1()
    
def change_trading_strategy2():
    subprocess.Popen(["bash", absolutePath+"stop.sh"])
    start_program2()

@app.route('/', methods=['GET'])
def index():
    return "Flask 서버가 실행 중입니다."

 
@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    channel_id = "C069C8Z7QAG"  # 메시지를 보낼 채널의 ID

    try:
        # Slack 채널에 요청 수신 알림을 보냄
        client.chat_postMessage(channel=channel_id, text="요청을 성공적으로 받았습니다." )

        # 나머지 이벤트 처리 로직...
        # ...

    except SlackApiError as e:
        # Slack API 에러 처리
        print(f"Error posting message: {e}")
    
    if "challenge" in slack_event:
        return make_response({"challenge" : slack_event["challenge"]}, 200, {"content_type": "application/json"})
 
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True, port=5002)