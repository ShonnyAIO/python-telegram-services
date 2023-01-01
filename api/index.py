from bs4 import BeautifulSoup  #del módulo bs4, necesitamos BeautifulSoup
from http.server import BaseHTTPRequestHandler
from decouple import config
import requests
import schedule
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(str('Hello World!!').encode())
        return

def bot_send_text(bot_message):

    bot_token = config("TELEGRAM_TOKEN")
    bot_chatID = config("CHAT_ID")
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response

def get_cantv():
    url = requests.get('https://cati.cantv.com.ve/chat_cantv_java/Servlet_Consulta_Saldo?consulta_codigo_area=212&consulta_numero_telefonico=5772359')
    response = url.json()
    fecha_aux = response[0]["fechaVencimiento"]
    fecha_pago = fecha_aux[6:8] + "/" + fecha_aux[4:6] + "/" + fecha_aux[0:4]
    bot_send_text(f'Su estado de cuenta de CANTV es: {response[0]["saldoActual"]} Bolivares tienes hasta la fecha de: {fecha_pago}')

def get_corpoelec():
    url = requests.get('https://ov-capital.corpoelec.gob.ve/index.php/Login/popup/ncc/1000020696048', verify=False)
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('nobr', {'id': 'l0013051'})
    format_result = result.text.replace(' ', '')
    bot_send_text(f'Su estado de cuenta de CORPOELEC es: {format_result} Bolivares')

def btc_scraping():
    url = requests.get('https://awebanalysis.com/es/coin-details/bitcoin/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('td', {'class' : 'text-larger text-price'})
    format_result = result.text

    return format_result

def report():
    btc_price = f'El precio de Bitcon es de {btc_scraping()}'
    bot_send_text(btc_price)


get_corpoelec()
get_cantv()
schedule.every().day.at("10:00").do(get_cantv)
schedule.every().day.at("10:00").do(get_corpoelec)

while True:
    schedule.run_pending()
