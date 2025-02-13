import requests

def get_btc_prices():
    try:
        # URL da API da Binance para o endpoint de klines (candlesticks)
        url = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h'
        
        # Fazer a requisição para obter os dados de preço
        response = requests.get(url)
        response.raise_for_status()  # Verificar se houve algum erro na requisição
        
        # Array com os dados de preço
        prices = response.json()
        
        # Inicializar os valores máximo e mínimo
        max_price = 0
        min_price = float('inf')
        
        # Iterar sobre os dados para encontrar os valores máximo e mínimo
        for price in prices:
            high = float(price[2])
            low = float(price[3])
            
            if high > max_price:
                max_price = high
            if low < min_price:
                min_price = low
        
        print(f'Valor Máximo: {max_price}')
        print(f'Valor Mínimo: {min_price}')
    
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Chamar a função
get_btc_prices()


//--------------------------------------------------------------
import requests

def get_btc_prices():
    try:
        # URL da API da Binance para o endpoint de klines (candlesticks)
        url = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h'
        
        # Fazer a requisição para obter os dados de preço
        response = requests.get(url)
        response.raise_for_status()  # Verificar se houve algum erro na requisição
        
        # Array com os dados de preço
        prices = response.json()
        
        # Inicializar os valores máximo, mínimo e o preço de fechamento
        max_price = 0
        min_price = float('inf')
        close_prices = []

        # Iterar sobre os dados para encontrar os valores máximo, mínimo e os preços de fechamento
        for price in prices:
            high = float(price[2])
            low = float(price[3])
            close = float(price[4])
            
            if high > max_price:
                max_price = high
            if low < min_price:
                min_price = low
            
            close_prices.append(close)
        
        print(f'Valor Máximo: {max_price}')
        print(f'Valor Mínimo: {min_price}')
        print(f'Preços de Fechamento: {close_prices}')
    
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Chamar a função
get_btc_prices()


//-----------------------------------------


import requests

def get_last_btc_candle():
    try:
        # URL da API da Binance para o endpoint de klines (candlesticks)
        url = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h'
        
        # Fazer a requisição para obter os dados de preço
        response = requests.get(url)
        response.raise_for_status()  # Verificar se houve algum erro na requisição
        
        # Array com os dados de preço
        prices = response.json()
        
        # Obter a última vela
        last_candle = prices[-1]
        
        # Extrair os valores desejados da última vela
        high = float(last_candle[2])
        low = float(last_candle[3])
        close = float(last_candle[4])
        
        print(f'Última Vela - Valor Máximo: {high}')
        print(f'Última Vela - Valor Mínimo: {low}')
        print(f'Última Vela - Preço de Fechamento: {close}')
    
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Chamar a função
get_last_btc_candle()
