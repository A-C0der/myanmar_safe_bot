import requests
import time
import json as js
class BotMyanmar:
    def __init__(self):
        self.token = "7586848193:AAEFsTAZwvua5YQdziZuSF174EMEQzyzkrc"
        self.url = f"https://api.telegram.org/bot{self.token}"
        self.last_update_id = None  # Track last processed update

    def get_updates(self):
        """Fetch new updates from Telegram API"""
        params = {"timeout": 10, "offset": self.last_update_id + 1 if self.last_update_id else None}
        response = requests.get(f"{self.url}/getUpdates", params=params)
        return response.json()

    def send_message(self, chat_id):
        """Send a message with inline buttons"""
        url = f"{self.url}/sendMessage"
        buttons = {
            "inline_keyboard": [
                [{"text": "မန္တလေး", "callback_data": "mandalay"}],
                [{"text": "စစ်ကိုင်း", "callback_data": "sagaing"}],
                [{"text": "နေပြည်တော်", "callback_data": "naypyitaw"}],
                [{"text": "ရှမ်း", "callback_data": "shan"}]
            ]
        }
        data = {
            "chat_id": chat_id,
            "text": "Choose a location:",
            "reply_markup": buttons
        }
        requests.post(url, json=data)

    def mandalay(self, chat_id):
        """Handle Mandalay button click"""
        url = f"{self.url}/sendMessage"
        buttons = {
            "inline_keyboard": [
                [{"text": "ကယ်ဆယ်ရေး", "callback_data": "mdy_rescue"}],
                [{"text": "အစားအသောက်ဆေး၀ါးအလှူ", "callback_data": "food_donation"}]
            ]
        }
        data = {
            "chat_id": chat_id,
            "text": "Mandalay options:",
            "reply_markup": buttons
        }
        requests.post(url, json=data)

    def handle_callback(self, callback_query):
        """Process button clicks"""
        query_id = callback_query["id"]
        chat_id = callback_query["message"]["chat"]["id"]
        data = callback_query["data"]
        text=''
        if data == "mandalay":
            self.mandalay(chat_id,)
        elif data == "mdy_rescue":
                return "MDY RESCUE"
        elif data == "rescue":
            text = "You selected: 'ကယ်ဆယ်ရေး'"
        elif data == "food_donation":
            text = "You selected: 'အစားအသောက်ဆေး၀ါးအလှူ'"
        else:
            text = "Unknown option."
        
        # Answer callback to remove the "loading" state in Telegram
        requests.post(f"{self.url}/answerCallbackQuery", json={"callback_query_id": query_id})

        # Edit message with selected option
        
        requests.post(f"{self.url}/editMessageText", json={
            "chat_id": chat_id,
            "message_id": callback_query["message"]["message_id"],
            "text": text
        })
        
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
                            self.send_message(chat_id)

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
