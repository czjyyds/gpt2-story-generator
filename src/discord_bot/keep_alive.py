from threading import Thread

from flask import Flask
from waitress import serve

app = Flask('')


def run():
    serve(app, host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
