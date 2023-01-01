import schedule
import requests
from flask import Flask
from flask import request
from flask import Response
from bs4 import BeautifulSoup  #del módulo bs4, necesitamos BeautifulSoup

app = Flask(__name__)

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def bot_send_text(bot_message):

    bot_token = "5920449308:AAFMoryS9bN6E_lWJvuQPdjjZxisDb8G1JM"
    bot_chatID = "1714790512"
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

@app.post("/")
def index():
    msg = request.get_json()
    inputText = msg["message"]["text"]
    if inputText == "/start":
        bot_send_text("Ya, I am Online. Send me a Prompt")
        schedule.every().day.at("10:00").do(get_cantv)
        schedule.every().day.at("10:00").do(get_corpoelec)
        while True:
            schedule.run_pending()
    return Response("ok", status=200)



# https://api.telegram.org/bot5920449308:AAFMoryS9bN6E_lWJvuQPdjjZxisDb8G1JM/setWebhook?url=https://python-telegram-services.vercel.app