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
        if location=='dontmiss':
         if location=='dontmiss':
            cursor.execute(f"SELECT name,location,status,donation,required FROM dontmiss")
            rowd = cursor.fetchall()
            dtt=[]
            for dae in rowd:
                dtt.append(f'နေရာ/မြို့ရွာ: {dae[0]}\n လိပ်စာ: {dae[1]}\n လက်ရှိအခြေအနေ: {dae[2]}\n အလျှူရှင်များရောက်ရှိမှု: {dae[3]}\n အဓိကလိုအပ်နေသောအရာများ: {dae[4]}\n')
            return dtt
        elif type(location)==list:
          try:
            if len(location)==2:
                cursor.execute(
    "SELECT name, phone, location, township, type, link, division, remark, date FROM donation WHERE township = ? AND type = ?",
    (location[0], location[1]))

                rows = cursor.fetchall()
                dt =[]
                for data in rows:
                    dt.append(f' အလျှူရှင်အမည်: {data[0]}\n ဖုန်းနံပါတ်: {data[1]}\n လိပ်စာ: {data[2]}, မြို့အမည်: {data[3]}\n တိုင်းအမည်: {data[6]}\n အလျှူအမျိုးအစား: {data[4]}\n အခြားအချက်အလက်: {data[7]}\n အချိန်:{data[8]} \n Link:{data[5]}\n \n')
                return dt
          
            elif len(location)==3:
                cursor.execute(
    "SELECT name, phone, location, township, type, link, division, remark, date FROM donation WHERE township = ? AND type = ? AND division = ?",
    (location[0], location[1], location[2]) 
)

                rows = cursor.fetchall()
                dt =[]
                for data in rows:
                 dt.append(f' အလျှူရှင်အမည်: {data[0]}\n ဖုန်းနံပါတ်: {data[1]}\n လိပ်စာ: {data[2]}, မြို့အမည်: {data[3]}\n တိုင်းအမည်: {data[6]}\n အလျှူအမျိုးအစား: {data[4]}\n အခြားအချက်အလက်: {data[7]}\n အချိန်:{data[8]} \n Link:{data[5]}\n \n')
                return dt
            else:
              return "အချက်အလက်မရှိပါ။"
          except sql.OperationalError:
            return "အချက်အလက်မရှိပါ။"
   
        
           
    def handle_callback(self, callback_query):
        """Process button clicks"""
        query_id = callback_query["id"]
        chat_id = callback_query["message"]["chat"]["id"]
        data = callback_query["data"]

        if data == "mandalay":
            self.mandalay(chat_id)

        elif data == 'dontmiss':
            self.send_message(chat_id,self.data_return('dontmiss'))

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
        remind=["miss","missed",'remind location','လျှူရန်ကျန်ရှိနေသောနေရာများ','လူရောက်နည်းသောနေရာများ','လျှူကြပါ','လိုအပ်ချက်များသောနေရာ','လိုအပ်နေသောနေရာများ']
        while True:
            updates = self.get_updates()
            if "result" in updates and len(updates["result"]) > 0:
                for update in updates["result"]:
                    self.last_update_id = update["update_id"]

                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        if update["message"]["text"] == "/start":
                            self.send_message(chat_id, """
လိုအပ်သည့်များကိုစာတိုပိုဖြင့် ရှာဖွေနိုင်ပါသည်။
အစားအသောက် စာဖွေသည့်ပုံစံ
ချမ်းမြသာစည် အစားအစာ 
ဆေး၀ါး
စစ်ကိုင်း  ဆေး  
ကယ်ဆယ်ရေး

တိုင်းဒေသကြီးနဲ့ အတိကျရှာဖွေလိုပါက
ချမ်းအေးသာစည်  အစားအစာ မန္တာလေးတိုင်း
""")

                        elif update["message"]["text"] == "dontmiss" or update["message"]["text"] in remind:
                                 self.send_message(chat_id,self.data_return('dontmiss'))
                        elif update["message"]["text"]:
                            sa = update["message"]["text"].split()
                            if len(sa) == 2:
                                self.send_message(chat_id,self.data_return(sa[:2]))
                            if len(sa) == 3:
                                 self.send_message(chat_id,self.data_return(sa[:3]))
                            else:
                                continue

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
