import requests
import hashlib
import hmac
import time
import os

SYMBOL = "ETHUSDT"
QUANTITY = 0.01  # Definir como um número em vez de uma string
PERIOD = 14

API_URL = "https://api.binance.com"  # "https://testnet.binance.vision"
API_KEY = "XXXXX"
SECRET_KEY = "XXXXXX"

CARTEIRA = 0
flag = 0
isOpened = False

def averages(prices, period, start_index):
    gains = 0
    losses = 0

    for i in range(period):
        if i + start_index >= len(prices):
            break
        diff = prices[i + start_index] - prices[i + start_index - 1]
        if diff >= 0:
            gains += diff
        else:
            losses += abs(diff)

    avg_gains = gains / period
    avg_losses = losses / period
    return avg_gains, avg_losses

def RSI(prices, period):
    avg_gains = 0
    avg_losses = 0

    for i in range(1, len(prices)):
        new_averages = averages(prices, period, i)

        if i == 1:
            avg_gains = new_averages[0]
            avg_losses = new_averages[1]
            continue

        avg_gains = (avg_gains * (period - 1) + new_averages[0]) / period
        avg_losses = (avg_losses * (period - 1) + new_averages[1]) / period

    rs = avg_gains / avg_losses
    return 100 - (100 / (1 + rs))

def new_order(symbol, quantity, side):
    order = {
        "symbol": symbol,
        "quantity": quantity,
        "side": side,
        "type": "MARKET",
        "timestamp": int(time.time() * 1000)
    }

    query_string = "&".join([f"{key}={value}" for key, value in order.items()])
    signature = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    order["signature"] = signature

    headers = {
        "X-MBX-APIKEY": API_KEY
    }

    try:
        response = requests.post(f"{API_URL}/api/v3/order", params=order, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print(e.response.json())

# Função para obter a cotação atual do dólar em relação ao real
def get_dollar_to_real_exchange_rate():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    rate = response.json()['rates']['BRL']
    return rate

# Função para converter um valor em dólar para real
def convert_dollar_to_real(dollar_amount):
    rate = get_dollar_to_real_exchange_rate()
    real_amount = dollar_amount * rate
    return round(real_amount, 2)  # Retorna o valor formatado com 2 casas decimais

def start():
    global CARTEIRA, flag, isOpened
    response = requests.get(f"{API_URL}/api/v3/klines?limit=100&interval=15m&symbol={SYMBOL}")
    data = response.json()
    candle = data[-1]
    last_price = float(candle[4])
    os.system('cls')

    print(f"Price ETH: {last_price}")

    # Converter para Reais
    try:
        real_amount = convert_dollar_to_real(last_price)
        print(f"REAIS: {real_amount}")
    except Exception as e:
        print(f"Erro ao converter o valor: {e}")

    prices = [float(k[4]) for k in data]
    rsi = RSI(prices, PERIOD)
    print(f"RSI: {rsi}")
    print(f"Já comprei? {isOpened}")

    if flag == 0:
        CARTEIRA = QUANTITY * last_price

    if rsi < 40 and not isOpened:
        print("sobrevendido, hora de comprar")
        isOpened = True
        # new_order(SYMBOL, QUANTITY, "BUY")
        CARTEIRA = CARTEIRA - (QUANTITY * last_price)
        flag = 1
    elif rsi > 60 and isOpened:
        print("sobrecomprado, hora de vender")
        # new_order(SYMBOL, QUANTITY, "SELL")
        isOpened = False
        CARTEIRA = CARTEIRA + (QUANTITY * last_price)
    else:
        print("aguardar")
        print(f"Valor na carteira: {CARTEIRA}")

if __name__ == "__main__":
    while True:
        start()
        time.sleep(3)
