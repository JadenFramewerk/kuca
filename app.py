from flask import Flask, render_template
from flask_socketio import SocketIO
import os
from threading import Thread
import time

app = Flask(__name__)
socketio = SocketIO(app)

def read_rub_price_from_file():
    file_path = 'rub_price_binance.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return None

def update_rub_price():
    previous_price = None

    while True:
        rub_price = read_rub_price_from_file()
        if rub_price and rub_price != previous_price:
            previous_price = rub_price
            socketio.send(rub_price, broadcast=True)  # Corrected the argument position

        time.sleep(1)  # Ожидаем 1 секунду перед следующей проверкой

# Запускаем фоновую задачу для обновления содержимого файла
thread = Thread(target=update_rub_price)
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app, debug=True)
