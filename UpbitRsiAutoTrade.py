import datetime
import math
import os
import time
import requests
import pyupbit
import datetime

RSI_PERIOD = 14
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70
FIRST_BUY_RATE = 0.5
ADDITIONAL_BUY_THRESHOLD = -5.0
STOP_LOSS_THRESHOLD = -7.0
TICKER = "KRW-BTC"


access = os.environ["access"]  # Upbit API access 키
secret = os.environ["secret"]   # Upbit API secret 키
myToken = os.environ["Slack_Token"]  # Access Token
myChannel = "비트코인-자동매매-1"  # 채널 이름 OR 채널 ID

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b["currency"] == ticker:  # 통화
            if b["balance"] is not None:
                return float(b["balance"])
            else:
                return 0

def get_rsi(df, period=RSI_PERIOD):

    df['change'] = df['close'].diff()

    df['up'] = df['change'].apply(lambda x: x if x > 0 else 0)
    df['down'] = df['change'].apply(lambda x: -x if x < 0 else 0)

    df['avg_up'] = df['up'].ewm(alpha=1/period).mean()
    df['avg_down'] = df['down'].ewm(alpha=1/period).mean()

    df['rs'] = df['avg_up'] / df['avg_down']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    rsi = df['rsi']

    return rsi

# 이미 매수한 코인인지 확인하는 함수
def has_coin(ticker, balances):
    result = False
    
    for coin in balances:
        coin_ticker = coin['unit_currency'] + "-" + coin['currency']
        
        if ticker == coin_ticker:
            result = True
            
    return result

# 종목 현재 가격조회_시작
def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0][
        "ask_price"
    ]  

# 수익률 확인 함수
def get_revenue_rate(balances, ticker):
    revenue_rate = 0.0

    for coin in balances:
        # 티커 형태로 전환
        coin_ticker = coin['unit_currency'] + "-" + coin['currency']

        if ticker == coin_ticker:
            # 현재 시세
            now_price = pyupbit.get_current_price(coin_ticker)

            revenue_rate = (now_price - float(coin['avg_buy_price'])) / float(coin['avg_buy_price']) * 100.0

    return revenue_rate

def evaluate_fluctuation(balances, ticker, money, ticker_rate):
    # 실제로 매도하다 보면, 단위와 주문 시간의 오차로 인해 금액간에 오차가 발생하는 경우가 있다.
    # 주문한 금액과 실제 주문된 금액의 오차를 감안하기 위해 모수 매수된 상태는 0.99를,
    # 최초 50% 매수된 상태는 0.49를 곱하는 것으로 확인하였다.
    # 만약 코인에 할당된 금액이 모두 매수 되었을 때는 수익률이 -7% 이하일 때 매도를 진행하고, 
    # 최초로 매수한 코인만 존재할 때는 수익률이 -5% 이하일 때 물을 타주도록 하였다.
    # 이 부분은 이해가 어렵다면 지워도 될 듯
    have_coin = 0.0
    for coin in balances:
        coin_ticker = coin['unit_currency'] + "-" + coin['currency']
        coin_avg_buy_price = float(coin['avg_buy_price'])
        coin_balance = float(coin['balance'])
        
        have_coin = coin_avg_buy_price * coin_balance
        if ticker == coin_ticker:
                ticker_rate = get_revenue_rate(balances, ticker)
                
                # 실제 매도된 금액의 오차 감안
                if (money * 0.99) < have_coin:
                    if ticker_rate <= STOP_LOSS_THRESHOLD:
                        amount = upbit.get_balance(ticker)    
                        upbit.sell_market_order(ticker, amount)   # 시장가에 매도
                
                # 실제 매수된 금액의 오차 감안
                elif (money * 0.49) < have_coin and (money * 0.51) > have_coin:
                    if ticker_rate <= ADDITIONAL_BUY_THRESHOLD:
                        upbit.buy_market_order(ticker, money * FIRST_BUY_RATE)   # 시장가에 코인 매수
                
                break      
    
# 슬랙 메세지 전송 함수
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
    my_Balance = get_balance("KRW")  # 잔고 확인
    print("Login OK")
    print("==========Autotrade start==========")
except:
    print("!!Login ERROR!!")
# 로그인_끝
else:
    print("내 잔고 : " + str(format(int(my_Balance), ",")) + " 원")
    print("date:" + str(datetime.datetime.now()))
    # 무한 루프를 돌되, sleep()을 통해 루프 사이의 간격을 조절합니다.
    while 1:
        try:
            balances = upbit.get_balances()
            my_money = float(balances[0]['balance'])
            money = math.floor(my_money)
            df_day = pyupbit.get_ohlcv(TICKER, interval="day")   
            rsi14 = get_rsi(df_day, RSI_PERIOD).iloc[-1]                          # 당일 RSI
            current_price = round(get_current_price(TICKER), 0)
            
            if rsi14 < 30:
                upbit.buy_market_order(TICKER, money) 
                balances = upbit.get_balances()        
                post_message(myToken, myChannel, " ")
                post_message(
                    myToken,
                    myChannel,    
                    str(current_price) + "원으로" + str(now) + "에 매수 성공!"
                )
                time.sleep(1000)
                

        # 매도 조건 충족 시
            elif rsi14 > 70:
                amount = upbit.get_balance(TICKER)     
                upbit.sell_market_order(TICKER, amount)  
                balances = upbit.get_balances()   
                now = datetime.datetime.today().strftime("%y-%m-%d %H:%M:%S") 
                post_message(myToken, myChannel, " ")
                post_message(
                    myToken,
                    myChannel,    
                    str(current_price) + "원으로" + str(now) + "에 매도 성공!"
                )
                time.sleep(1000)
            
            balances = upbit.get_balances()
            ticker_rate = get_revenue_rate(balances, TICKER)
            
            evaluate_fluctuation(balances, TICKER, money, ticker_rate)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            time.sleep(1)

