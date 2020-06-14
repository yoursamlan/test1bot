import requests
import json
import configparser as cfg
import urllib
import json, random
#import StringIO
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


class telegram_chatbot():

    def __init__(self):
        self.token = '1186846195:AAHjOEd8UG6-4Wq8U1fTzOSZ0fVlFl-_oHE'
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

def text(msg):
    msg = msg.lower()
    if msg == "hi":
        rply = "Hey beautiful \U0001F609"
        #rply = "Hey beautiful"
    elif msg == "i love you":
        rply = "Bhaluu koi?????? \U0001F612"
        #rply = "Bhaluu koi??????"
    elif "i love you bhaluu" in msg:
        rply = "I love you tooooooo buchii.... maaaaahhhh"
    else:
        #rply = "sorry"
        rply = "\U0001F612"
    return rply



bot = telegram_chatbot()


def make_reply(msg):
    reply = None
    if msg is not None:
        reply = text(msg)
    return reply

def send_photo(msg):
    #869895108
    if msg is not None:
        r1 = random.randint(0, 4)
        piclist = ['/elLr4DW','BpyNTKj','4DfoHvt','7kgfjGA','74RlZJb']
        pic = 'https://i.imgur.com/'+str(piclist[r1])+'.jpg'
    return pic

update_id = 509976542
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])

            except:
                message = ""
            from_ = item["message"]["from"]["id"]
            print(from_)
            print(message.translate(non_bmp_map))

            if(from_ == 869895108 or from_ == 863693239):
                if ("memory" in message) or ("feel me lucky" in message):
                    pic = send_photo(message)
                    bot.send_message(pic, from_)
                else:
                    reply = make_reply(message)
                    #print(reply)
                    bot.send_message(reply, from_)
            else:
                    reply = make_reply(message)
                    #print(reply)
                    bot.send_message(reply, from_)
                    
