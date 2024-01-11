from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def obtener_datos_cacao():
    url = 'https://es.tradingview.com/markets/futures/quotes-agricultural/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        price = soup.find('td', class_='cell-RLhfr_y4 right-RLhfr_y4')
        percent = soup.find('span', class_='positive-p_QIAEOQ')
        change = soup.find('span', class_='positive-YXaj5m4M')

        if percent:
            precio = price.text
            cambio_porcentual = percent.text
            cambio = change.text

            return {
                'Precio': precio,
                'Cambio del cacao': cambio,
                'Porcentaje de cambio del cacao': cambio_porcentual
            }
        else:
            return {'error': 'No se encontró el elemento con la clase específica.'}
    else:
        return {'error': f'La solicitud no fue exitosa. Código de estado: {response.status_code}'}

@app.route('/')
def index():
    return 'API de datos de cacao, por favor agregue "/datos-cacao" al url para que pueda observar los resultados'
    
@app.route('/datos-cacao', methods=['GET'])
def obtener_datos_cacao_api():
    datos_cacao = obtener_datos_cacao()
    return jsonify(datos_cacao)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8040)
