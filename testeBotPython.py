import requests
import time
import os

SYMBOL = "BTCUSDT"
BUY_PRICE = 97500
SELL_PRICE = 97600

CARTEIRA = BUY_PRICE

API_URL = "https://testnet.binance.vision"  # https://api.binance.com

isOpened = False

def start():
    global CARTEIRA, isOpened
    
    try:
        # Fazer a requisição para obter os dados de preço
        url = f"{API_URL}/api/v3/klines?limit=21&interval=15m&symbol={SYMBOL}"
        response = requests.get(url)
        response.raise_for_status()  # Verificar se houve algum erro na requisição
        
        # Array com os dados de preço
        data = response.json()
        # Acessa a última vela
        candle = data[-1]
        # Posição 4 do vetor armazena o preço de fechamento
        price = float(candle[4])
        os.system('cls')
        print("Price: " + str(price))

        if price <= BUY_PRICE and not isOpened:
            print("comprar")
            CARTEIRA = CARTEIRA - BUY_PRICE
            isOpened = True
        elif price >= SELL_PRICE and isOpened:
            print("vender")
            CARTEIRA = CARTEIRA + SELL_PRICE
            isOpened = False
        else:
            
            print("aguardar")
            print("Valor na carteira: " + str(CARTEIRA))
            print("Valor de compra: " + str(BUY_PRICE))
            print("Valor de venda: " + str(SELL_PRICE))
            print("-------------------")
    
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

while True:
    start()
    time.sleep(3)
