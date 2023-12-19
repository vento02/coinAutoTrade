
import pyupbit
import datetime
import numpy as np
import os
import requests

access = os.environ['access']                           # Upbit API access 키
secret = os.environ['secret']                           # Upbit API secret 키
myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-자동매매-1"  # 채널 이름 OR 채널 ID
# 내 잔고 조회_시작
def get_balance(ticker):
      balances = upbit.get_balances()
      for b in balances:
          if b['currency'] == ticker:
              if b['balance'] is not None:
                  return float(b['balance'])
              else:
                  return 0
# 내 잔고 조회_끝

def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)


# 로그인_시작
try:
  upbit = pyupbit.Upbit(access, secret)
  my_Balance = get_balance("KRW")             # 내 잔고
  print("Login OK")
  print("==========Autotrade start==========")
except:
  print("!!Login ERROR!!")
# 로그인_끝
else:
  print("내 잔고 : "+str(format(int(my_Balance),','))+" 원")
  print("date:"+str(datetime.datetime.now()))

post_message(myToken, myChannel, " ")
post_message(
    myToken,
    myChannel,
    "내 잔고 : "+str(format(int(my_Balance),','))+" 원" + "\n" + "date:"+str(datetime.datetime.now()),
    )
