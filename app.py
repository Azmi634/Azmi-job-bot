import os
import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=TOKEN)
keywords = [
    "Mechatronics Yemen",
    "PLC Yemen",
    "Maintenance Engineer Yemen",
    "Internship Yemen",
    "Automation Yemen",
    "Electrical Engineer Yemen"
]

sent_jobs = set()

def search_jobs():
    headers = {"User-Agent": "Mozilla/5.0"}
    for keyword in keywords:
        url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for g in soup.find_all('a'):
            link = g.get('href')
            if link and "http" in link and link not in sent_jobs:
                sent_jobs.add(link)
                message = f"🚀 وظيفة جديدة\n\n🔎 البحث: {keyword}\n🔗 الرابط:\n{link}"
                bot.send_message(chat_id=CHAT_ID, text=message)
                time.sleep(2)

# ======= Flask Web Server بسيط ليجعل Render يقبل الخدمة =========
app = Flask(__name__)

@app.route("/")
def home():
    return "Yemen Job Bot is running!"

# ======= Background Loop =========
import threading

def job_loop():
    while True:
        try:
            search_jobs()
        except Exception as e:
            print("Error:", e)
        time.sleep(300)  # يفحص كل 5 دقائق

threading.Thread(target=job_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
