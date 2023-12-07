import logging
import json
from datetime import datetime
from flask import Flask, request, make_response
from slack_sdk import WebClient
import subprocess
 
token = "xoxb-6144145428068-6320182512017-Lhd2kbJvJkKoHfuL5pRofka9"
app = Flask(__name__)
client = WebClient(token)
strategy = 1
#strategy 1이 돌파매매법임
absolutePath = "/home/ubuntu/autoTrade-1/"
 
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
        '시작': '매매프로그램을 시작합니다.[기본은 돌파매매법입니다.]',
        '정지': '실행중인 매매프로그램을 중지합니다.',
        '잔고확인': '현재 잔고입니다.',
        '작동확인': '프로그램이 작동중인지 확인합니다.',
        '가격': '현재 매수목표가와 현재가를 확인합니다.',
        '돌파매매법': '돌파매매법으로 매매법을 교체합니다.',
        'RSI매매법': 'RSI매매법으로 매매법을 교체합니다',
        '매매기법': "현재 매매기법으로는 '돌파매매법'과 'RSI매매법'이 있습니다. 매매법을 변경하고 싶으시다면, 매매법의 이름을 명령어로 입력해주세요."
    }

    global strategy

    if "시작" in trim_text:
        start_program()
    elif "정지" in trim_text:
        stop_program()
    elif "작동확인" in trim_text:
        check_program()
    elif "잔고확인" in trim_text:
        check_balance()
    elif "가격" in trim_text:
        show_target_price()
    elif "돌파매매법" in trim_text:
        strategy = 1
        change_trading_strategy(strategy)
    elif "RSI매매법" in trim_text:
        strategy = 2
        change_trading_strategy(strategy)
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


def start_program():
    if strategy == 1:
        subprocess.Popen(["bash", absolutePath+"start.sh"])
    elif strategy == 2:
        subprocess.Popen(["bash", absolutePath+"startRsi.sh"])

def stop_program():
    if strategy == 1:
        subprocess.Popen(["bash", absolutePath+"stop.sh"])
    elif strategy == 2:
        subprocess.Popen(["bash", absolutePath+"stopRsi.sh"])

def check_program():
    if strategy == 1:
        subprocess.Popen(["bash", absolutePath+"ProcessCheck.sh"])
    elif strategy == 2:
        subprocess.Popen(["bash", absolutePath+"RsiProcessCheck.sh"])
    

    
def check_balance():
    process = subprocess.Popen(["python", absolutePath+"balance.py"])

def show_target_price():
    if strategy == 1:
        subprocess.Popen(["bash", absolutePath+"Tprice_alertBot.sh"])
    elif strategy == 2:
        subprocess.Popen(["bash", absolutePath+"RsiPrice_alertBot.sh"])
    

def change_trading_strategy(strategy):
    if strategy == 1:
        subprocess.Popen(["bash", absolutePath+"stop.sh"])
        start_program()
    elif strategy == 2:
        subprocess.Popen(["bash", absolutePath+"stopRsi.sh"])
        start_program()
    else:
        print("Invalid strategy selected")

@app.route('/', methods=['GET'])
def index():
    return "Flask 서버가 실행 중입니다."

 
@app.route('/', methods=['POST'])
def hello_there():
    slack_event = json.loads(request.data)
    channel_id = "C064ULBGDC0"  # 메시지를 보낼 채널의 ID

    try:
        # Slack 채널에 요청 수신 알림을 보냄
        client.chat_postMessage(channel=channel_id, text="요청을 성공적으로 받았습니다.")

        # 나머지 이벤트 처리 로직...
        # ...

    except SlackApiError as e:
        # Slack API 에러 처리
        print(f"Error posting message: {e}")
    
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
 
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})
 
 
if __name__ == '__main__':
    app.run(debug=True, port=5002)