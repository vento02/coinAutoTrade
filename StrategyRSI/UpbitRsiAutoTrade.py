import datetime
import math
import os
import time
import pyupbit

RSI_PERIOD = 14
RSI_BUY_THRESHOLD = 30
RSI_SELL_THRESHOLD = 70
FIRST_BUY_RATE = 0.5
ADDITIONAL_BUY_THRESHOLD = -5.0
STOP_LOSS_THRESHOLD = -7.0
TICKER = "KRW-BTC"


access = os.environ["access"]  # Upbit API access 키
secret = os.environ["secret"]  # Upbit API secret 키
upbit = pyupbit.Upbit(access, secret)
# 수수료 아직 설정안해놓음

def get_rsi(df, period=RSI_PERIOD):

    # 전일 대비 변동 평균
    df['change'] = df['close'].diff()

    # 상승한 가격과 하락한 가격
    df['up'] = df['change'].apply(lambda x: x if x > 0 else 0)
    df['down'] = df['change'].apply(lambda x: -x if x < 0 else 0)

    # 상승 평균과 하락 평균
    df['avg_up'] = df['up'].ewm(alpha=1/period).mean()
    df['avg_down'] = df['down'].ewm(alpha=1/period).mean()

    # 상대강도지수(RSI) 계산
    df['rs'] = df['avg_up'] / df['avg_down']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    rsi = df['rsi']

    return rsi

# 이미 매수한 코인인지 확인
def has_coin(ticker, balances):
    result = False
    
    for coin in balances:
        coin_ticker = coin['unit_currency'] + "-" + coin['currency']
        
        if ticker == coin_ticker:
            result = True
            
    return result

# 수익률 확인 함수
# 티커(비트코인)의 현재 시세에서 평균 매입단가를 뺀 후, 이를 평균 매입단가로 나누어 수익률을 구한다
def get_revenue_rate(balances, ticker):
    revenue_rate = 0.0

    for coin in balances:
        # 티커 형태로 전환
        coin_ticker = coin['unit_currency'] + "-" + coin['currency']

        if ticker == coin_ticker:
            # 현재 시세
            now_price = pyupbit.get_current_price(coin_ticker)
             
            # 수익률 계산을 위한 형 변환
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
        have_coin = float(ticker['avg_buy_price']) * float(coin_ticker['balance'])
        if ticker == coin_ticker:
                have_coin = float(coin_ticker['avg_buy_price']) * float(coin_ticker['balance'])
                ticker_rate = get_revenue_rate(balances, ticker)
                
                # 실제 매도된 금액의 오차 감안
                if (money * 0.99) < have_coin:
                    if ticker_rate <= STOP_LOSS_THRESHOLD:
                        amount = upbit.get_balance(ticker)       # 현재 코인 보유 수량	  
                        upbit.sell_market_order(ticker, amount)   # 시장가에 매도
                
                # 실제 매수된 금액의 오차 감안
                elif (money * 0.49) < have_coin and (money * 0.51) > have_coin:
                    if ticker_rate <= ADDITIONAL_BUY_THRESHOLD:
                        upbit.buy_market_order(ticker, money * FIRST_BUY_RATE)   # 시장가에 코인 매수
                
                break      
    

def main():
    # 로그인_시작
    try:
        upbit = pyupbit.Upbit(access, secret)
        my_Balance = upbit.get_balances("KRW")  # 내 잔고
        print("Login OK")
        print("==========Autotrade start==========")
    except:
        print("!!Login ERROR!!", e)
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
                df_day = pyupbit.get_ohlcv(TICKER, interval="day")     # 일봉 정보
                rsi14 = get_rsi(df_day, RSI_PERIOD).iloc[-1]                          # 당일 RSI
                before_rsi14 = get_rsi(df_day, RSI_PERIOD).iloc[-2]                   # 전날 RSI
                
                if has_coin(TICKER, balances):
                # 매도 조건 충족
                    if rsi14 < RSI_SELL_THRESHOLD and before_rsi14 > RSI_SELL_THRESHOLD:
                            amount = upbit.get_balance(TICKER)       # 현재 코인 보유 수량	  
                            upbit.sell_market_order(TICKER, amount)  # 시장가에 매도 

                else:
                # 매수 조건 충족
                    if rsi14 > RSI_BUY_THRESHOLD and before_rsi14 < RSI_BUY_THRESHOLD:
                        upbit.buy_market_order(TICKER, money * FIRST_BUY_RATE)    # 시장가에 코인 매수
                
                balances = upbit.get_balances()
                ticker_rate = get_revenue_rate(balances, TICKER)
                
                evaluate_fluctuation(balances, TICKER, money, ticker_rate)
                
            except pyupbit.exceptions.UpbitError as e:
                print(f"Upbit API error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                time.sleep(1)
    

if __name__ == "__main__":
    main()