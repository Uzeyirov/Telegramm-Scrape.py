import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time
from telegram import Bot
import os


#Define URL (Book)

url="https://emlak.az/"
time.sleep(5)

# Request page
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")



# Prepare excel
wb = Workbook()
ws = wb.active
ws.title = "Emlak Scrape"
ws.append(["Price", "Attributes"])


# Scrape listing
emlak=soup.find_all("div", class_="ticket-item")


for product in emlak:
    
    price_tag = product.find("div", class_="price-ticket")
    attribute_tag = product.find("div", class_="description-ticket")


    price=price_tag.get_text(strip=True) if price_tag else ""
    attribute=attribute_tag.get_text(strip=True) if attribute_tag else ""
    

    if price and attribute:
        ws.append([price, attribute])

    # Save Excel
wb.save("Emlak.xlsx")
print("Done: emlak-scrape.xlsx")

#Telegram-Bot
BOT_TOKEN = "7961154905:AAE39dcHN3GqA-la8WSJlboHTJLSHTtaH_4"
CHAT_ID = "5882097855"

bot = Bot(token=BOT_TOKEN)


file_path = "Emlak.xlsx"

with open(file_path, "rb") as f:
    bot.send_document(chat_id=CHAT_ID, document=f, filename=os.path.basename(file_path))