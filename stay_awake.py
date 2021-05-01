from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')

def home():
  return "Ayo I'm up"  # lets change this heh

def run():
  app.run(host='0.0.0.0', port=800)

def stay_awake():
  t = Thread(target=run)
  t.start()