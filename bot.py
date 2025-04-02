import requests
import time
import json as js
import pandas as pd
import sqlite3 as sql
class BotMyanmar:
    def __init__(self):
        self.token = "7586848193:AAEFsTAZwvua5YQdziZuSF174EMEQzyzkrc"  # Replace with your bot token
        self.url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = None  # Track last processed update

    def get_updates(self):
        """Fetch new updates from Telegram API"""
        params = {"timeout": 10, "offset": self.last_update_id + 1 if self.last_update_id else None}
        response = requests.get(f"{self.url}/getUpdates", params=params)
        return response.json()

    def send_message(self, chat_id, text, buttons=None):
        """Send a message with optional inline buttons"""
        url = f"{self.url}/sendMessage"
        
        # data={
        #         'chat_id':chat_id,
        #         'text':'hello'
        #     }  
       
       
        data = {"chat_id": chat_id}
        
        if type(text)==str:
            data = {"chat_id": chat_id, "text":text}
            if buttons:
                data["reply_markup"] = buttons
            
            requests.post(url,json=data)
        if type(text)==list:
            for i in text:
                data["text"] = i
                if buttons:
                    data["reply_markup"] = buttons
                requests.post(url, json=data)

        
        
    def mandalay(self, chat_id):
        """Handle Mandalay button click"""
        buttons = {
            "inline_keyboard": [
                [{"text": "ကယ်ဆယ်ရေး", "callback_data": "mdy_rescue"}],
                [{"text": "အစားအသောက်ဆေး၀ါးအလှူ", "callback_data": "mdy_donation"}]
            ]
        }
        self.send_message(chat_id, "Mandalay options:", buttons)

    def data_return(self,location):
        conn = sql.connect("/project/myanmar_safe_bot/earthdb.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT name,phone,location,date FROM {location}")
        rows = cursor.fetchall()
        dt =[]
        for data in rows:
            dt.append(f' Name: {data[0]}, Phone: {data[1]},Location: {data[2]}, Date: {data[3]}\n\n')
        return dt
            
           
    def handle_callback(self, callback_query):
        """Process button clicks"""
        query_id = callback_query["id"]
        chat_id = callback_query["message"]["chat"]["id"]
        data = callback_query["data"]

        if data == "mandalay":
            self.mandalay(chat_id)
        elif data == "mdy_rescue":
            self.send_message(chat_id,self.data_return('mdysafe'))  # Send "MDY RESCUE" when clicked
        elif data == "mdy_donation":
            self.send_message(chat_id,self.data_return('mdydonate'))
        else:
            self.send_message(chat_id, "Unknown option.")

        # Answer callback to remove the "loading" state in Telegram
        requests.post(f"{self.url}/answerCallbackQuery", json={"callback_query_id": query_id})

    def process_updates(self):
        """Continuously check for new messages"""
        while True:
            updates = self.get_updates()
            if "result" in updates and len(updates["result"]) > 0:
                for update in updates["result"]:
                    self.last_update_id = update["update_id"]

                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        if update["message"]["text"] == "/start":
                            self.send_message(chat_id, "Select Location:", {
                                "inline_keyboard": [
                                    [{"text": "မန္တလေး", "callback_data": "mandalay"}],
                                    [{"text": "စစ်ကိုင်း", "callback_data": "sagaing"}],
                                    [{"text": "နေပြည်တော်", "callback_data": "naypyitaw"}],
                                    [{"text": "ရှမ်း", "callback_data": "shan"}]
                                ]
                            })
                        
                        elif update["message"]["text"] == "MDY FOOD" or update["message"]["text"] == "mdy food" or update["message"]["text"]=="MDY DONATE" or update["message"]["text"]=="mdy donate":
                             self.send_message(chat_id,self.data_return('mdydonate'))

                        elif update["message"]["text"] == "mdy rescue" or update["message"]["text"] == "MDY RESCUE" or update["message"]["text"]=="MDY SAFE" or update["message"]["text"]=="mdy safe":
                             self.send_message(chat_id,self.data_return('mdysafe'))
                    elif "callback_query" in update:
                        self.handle_callback(update["callback_query"])

            time.sleep(1)  # Prevent API spam

    def run(self):
        """Run the bot indefinitely"""
        self.process_updates()

# Run the bot
if __name__ == "__main__":
    bot = BotMyanmar()
    bot.run()
