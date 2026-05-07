from flask import Flask
import threading
import os
import requests
import time
from bs4 import BeautifulSoup
#fix bot
TOKEN = "8679506052:AAGSx0N3zOrajN70WyXcVqHvkzHFGaChvQE"
CHAT_ID = "8203943962"
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot radi!"
WATCHLIST = ["JDRN", "ATPL", "CKML"]

seen = set()

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def fetch_eho():
    url = "https://eho.zse.hr/obavijesti-izdavatelja/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for a in soup.find_all("a"):
        text = a.get_text(strip=True)
        link = a.get("href")
        if text and len(text) > 20:
            results.append((text, link))

    return results
while   True:
    try:
        posts = fetch_eho()

        for title, link in posts:
            if title in seen:
                continue

            seen.add(title)

            for ticker in WATCHLIST:
                if ticker in title:
                    msg = f"🚨 {ticker}\n{title}\n{link}"
                    send(msg)

        time.sleep(60)

    except Exception as e:
        print(e)
        time.sleep(60)
    def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()    
        
