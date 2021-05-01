from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')

def home():
  return "Hey, I'm awake!"  # w

def run():
  app.run(host='0.0.0.0', port=800)

def stay_awake():
  t = Thread(target=run)
  t.start()