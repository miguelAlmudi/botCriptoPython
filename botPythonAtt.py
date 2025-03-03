import requests
import hashlib
import hmac
import time
import os

SYMBOL = "BTCUSDT"
QUANTITY = "0.001"
PERIOD = 14

API_URL = "https://api.binance.com"  # "https://testnet.binance.vision"
API_KEY = "XXXXX"
SECRET_KEY = "XXXXXX"

CARTEIRA = 0
flag = 0

def averages(prices, period, startIndex):
    gains = 0
    losses = 0

    for i in range(period):
        if (i + startIndex) >= len(prices):
            break
        diff = prices[i + startIndex] - prices[i + startIndex - 1]
        if diff >= 0:
            gains += diff
        else:
            losses += abs(diff)

    avgGains = gains / period
    avgLosses = losses / period
    return avgGains, avgLosses

def RSI(prices, period):
    avgGains = 0
    avgLosses = 0

    for i in range(1, len(prices)):
        newAverages = averages(prices, period, i)

        if i == 1:
            avgGains = newAverages[0]
            avgLosses = newAverages[1]
            continue

        avgGains = (avgGains * (period - 1) + newAverages[0]) / period
        avgLosses = (avgLosses * (period - 1) + newAverages[1]) / period

    rs = avgGains / avgLosses
    return 100 - (100 / (1 + rs))

def newOrder(symbol, quantity, side):
    order = {
        "symbol": symbol,
        "quantity": quantity,
        "side": side,
        "type": "MARKET",
        "timestamp": int(time.time() * 1000)
    }

    query_string = "&".join([f"{k}={v}" for k, v in order.items()])
    signature = hmac.new(SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    order["signature"] = signature

    headers = {
        "X-MBX-APIKEY": API_KEY
    }

    try:
        response = requests.post(
            API_URL + "/api/v3/order",
            headers=headers,
            data=query_string
        )
        print(response.json())
    except requests.exceptions.RequestException as err:
        print(err.response.json())

isOpened = False

def start():
    global CARTEIRA, flag, isOpened

    response = requests.get(API_URL + "/api/v3/klines", params={
        "symbol": SYMBOL,
        "interval": "15m",
        "limit": 100
    })
    data = response.json()
    candle = data[-1]
    lastPrice = float(candle[4])
    os.system('cls')
    print(f"Price: {lastPrice}")

    prices = [float(k[4]) for k in data]
    rsi = RSI(prices, PERIOD)
    print(f"RSI: {rsi}")
    print(f"Já comprei? {isOpened}")

    if flag == 0:
        CARTEIRA = float(QUANTITY) * lastPrice

    if rsi < 40 and not isOpened:
        print("sobrevendido, hora de comprar")
        isOpened = True
        # newOrder(SYMBOL, QUANTITY, "BUY")
        CARTEIRA -= float(QUANTITY) * lastPrice
        flag = 1
    elif rsi > 60 and isOpened:
        print("sobrecomprado, hora de vender")
        # newOrder(SYMBOL, QUANTITY, "SELL")
        isOpened = False
        CARTEIRA += float(QUANTITY) * lastPrice
    else:
        print("aguardar")
        print(f"Valor na carteira: {CARTEIRA}")

if __name__ == "__main__":
    while True:
        start()
        time.sleep(3)
