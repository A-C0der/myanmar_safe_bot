import requests
import time
import json as js
import pandas as pd
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
        data = {"chat_id": chat_id, "text": text}
        if buttons:
            data["reply_markup"] = buttons
        requests.post(url, json=data)

    def mandalay(self, chat_id):
        """Handle Mandalay button click"""
        buttons = {
            "inline_keyboard": [
                [{"text": "ကယ်ဆယ်ရေး", "callback_data": "mdy_rescue"}],
                [{"text": "အစားအသောက်ဆေး၀ါးအလှူ", "callback_data": "food_donation"}]
            ]
        }
        self.send_message(chat_id, "Mandalay options:", buttons)

    def data_return(self,file):
        with open(file,"r") as mdr:
            data = js.load(mdr)
            df = pd.DataFrame(data)
            for index, row in df.iterrows():
                return f"Name: {row.get('rescue_name','Not Show')}\nLocation: {row.get('location')}\n Phone:{row.get('phone')}\n\n"

    def handle_callback(self, callback_query):
        """Process button clicks"""
        query_id = callback_query["id"]
        chat_id = callback_query["message"]["chat"]["id"]
        data = callback_query["data"]

        if data == "mandalay":
            self.mandalay(chat_id)
        elif data == "mdy_rescue":
            self.send_message(chat_id,self.data_return('mdy_resuce_data.json'))  # Send "MDY RESCUE" when clicked
        elif data == "food_donation":
            self.send_message(chat_id, "You selected: 'အစားအသောက်ဆေး၀ါးအလှူ'")
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
                            self.send_message(chat_id, "Choose a location:", {
                                "inline_keyboard": [
                                    [{"text": "မန္တလေး", "callback_data": "mandalay"}],
                                    [{"text": "စစ်ကိုင်း", "callback_data": "sagaing"}],
                                    [{"text": "နေပြည်တော်", "callback_data": "naypyitaw"}],
                                    [{"text": "ရှမ်း", "callback_data": "shan"}]
                                ]
                            })

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
