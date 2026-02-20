import os
import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot

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
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for keyword in keywords:
        url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for g in soup.find_all('a'):
            link = g.get('href')
            if link and "http" in link:
                if link not in sent_jobs:
                    sent_jobs.add(link)
                    message = f"🚀 وظيفة جديدة\n\n🔎 البحث: {keyword}\n🔗 الرابط:\n{link}"
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    time.sleep(2)

while True:
    search_jobs()
    time.sleep(300)
