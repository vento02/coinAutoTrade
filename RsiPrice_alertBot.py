import datetime
import os
import pyupbit
import requests

RSI_PERIOD = 14
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70
TICKER = "KRW-BTC"

access = os.environ["access"]  # Upbit API access 키
secret = os.environ["secret"]  # Upbit API secret 키

def get_rsi(df, period=14):
    df['change'] = df['close'].diff()
    df['up'] = df['change'].apply(lambda x: x if x > 0 else 0)
    df['down'] = df['change'].apply(lambda x: -x if x < 0 else 0)
    df['avg_up'] = df['up'].ewm(alpha=1/period).mean()
    df['avg_down'] = df['down'].ewm(alpha=1/period).mean()
    df['rs'] = df['avg_up'] / df['avg_down']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    
    rsi = df['rsi']
    return rsi

# 메시지 전송 함수_시작
def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)
    
def nowtime():
    now = datetime.datetime.today().strftime("%y-%m-%d %H:%M:%S")  # 현재 DateTime
    return now

myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-돌파매매전략"  # 채널 이름 OR 채널 ID

df_day = pyupbit.get_ohlcv(TICKER, interval="day")
rsi = get_rsi(df_day, RSI_PERIOD).iloc[-1]

post_message(myToken, myChannel, f"{nowtime()} 현재 RSI: {rsi:.2f}")

if rsi < RSI_BUY_THRESHOLD:
    post_message(myToken, myChannel, f"매수 신호! 현재 RSI: {rsi:.2f}")
elif rsi > RSI_SELL_THRESHOLD:
    post_message(myToken, myChannel, f"매도 신호! 현재 RSI: {rsi:.2f}")
