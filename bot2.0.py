import requests
import json
#import alphabet
import urllib
import random
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

p_beta = [0,0]
cl = []

class telegram_chatbot():

    def __init__(self):
        self.token = ''
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

bot = telegram_chatbot()


#=======================
#   CUSTOM FUNCTIONS
#=======================

def text(msg):
    msg = msg.lower()
    
    # greetings
    
    if "hi" in msg or "hello" in msg:
        rply = "Hey beautiful \U0001F609"

    elif "good morning" in msg or "suprovat" in msg or "gd mrng" in msg or "gd mrn9" in msg or "gd mr9" in msg or "morning" in msg:
        rply = "Have a very good morning dear.... \U0001F60D"
    elif "good noon" in msg or "gd nn" in msg or "gd noon" in msg or "gd nun" in msg or "noon" in msg:
        rply = "What's so good about this noon .... \U0001F60D"
        
    else:
        #rply = "sorry"
        rply = "\U0001F612"
    return rply

def make_reply(msg):
    reply = None
    if msg is not None:
        reply = text(msg)
    return reply

def textmsg(msg,uid):
    reply = make_reply(msg)
    #print(reply)
    bot.send_message(reply, uid)
    
def send_photo(msg):
    #869895108
    if msg is not None:
        r1 = random.randint(0, 4)
        piclist = ['/elLr4DW','BpyNTKj','4DfoHvt','7kgfjGA','74RlZJb']
        pic = 'https://i.imgur.com/'+str(piclist[r1])+'.jpg'
    return pic

def sendphotoinit(message,uid):
    pic = send_photo(message)
    bot.send_message(pic, uid)
    cl.append("xx")

def initplaythirty(msg,uid,p_beta):
    from_ = uid
    rply = "Welcome to Play 30. The main aim of this game is pushing your opponent to say 30. But there is a twist. One can't exceed 3 numbers at the same time.\n For example, if player-A starts with 1, 2 then player B is allowed to say (3) OR (3, 4) OR (3, 4, 5). But NOT more than 5.\n The player, who will say '29', will win the game. "
    bot.send_message(rply, from_)
    rply = "To play, please enter the last number, followed by p.\nFor Example, if you want to say 3,4,5; then send 5p as your move.\n Do not cheat; else you will be forfeited."
    bot.send_message(rply, from_)
    rply = "Let's have a toss"
    bot.send_message(rply, from_)
    t1 = random.randint(0,100)
    #print(t1)
    if t1%2 == 0:
        rply = "I won the toss. It's my turn now. \nI will start with 1\n\nIf you want to say... \n 2       -> Type 2p\n 2,3    -> Type 3p\n 2,3,4 -> Type 4p "
        bot.send_message(rply, from_)
        p_beta.append(1)
    else:
        rply = "You won the toss. It's your turn. Good Luck.\n\nIf you want to say... \n 1       -> Type 1p\n 1,2    -> Type 2p\n 1,2,3 -> Type 3p"
        bot.send_message(rply, from_)
        
    #game = playthirty(message)
    #bot.send_message(game, from_)
    

def playthirty(msg,p_beta):
    x = msg
    print("x: ",x)
    d = p_beta[-2]
    print("d: ",d)
    print(p_beta)
    if (abs(int(d) - int(x)) <=3) and x < 30:
        if x == 29:
            m = "I am resigning. Well played dear....\U0001F60D"
            cl.append("xx")
        elif x%4==1:
            n = x//4
            m = 4*(n+1)
            p_beta.append(m)
        elif x%4==0:
            m = x+1
            p_beta.append(m)
        else:
            n = x//4
            m = (4*(n+1)+1)
            p_beta.append(m)
    else:
        m = "Sorry you have crossed your limit.\nThe Game is forfeited.\nI have WON."
        cl.append("xx")
    return m

def ptgameplay(message,uid,p_beta):
    from_ = uid
    try:
        v = int(message[:-1])
        print(v)
        px = str(playthirty(v,p_beta))
        if px == "29":
            p_beta = [0,0]
            rply = "29 \nHurray... I have won. Well played...\U0001F60E"
            cl.append("xx")
            bot.send_message(rply, from_)
        else:  
            p_beta.append(v)
            bot.send_message(px, from_)
            
    except ValueError:
        rply = "Sorry please input (last number + p), eg., 1p/9p/24p etc. to continue playing the game '30'"
        bot.send_message(rply, from_)

#========================
#   SYSTEM ADMIN
#========================

def indexer(message,userid):
    msg = message
    uid = str(userid)
    if "alphabet" in msg:
        cl.append("alpha")
    elif "play 30" in msg or "play30" in msg:
        cl.append("play30-init")
        p_beta.append(0)
    elif (len(msg)==2 or len(msg)==3) and msg.endswith("p"):
        cl.append("play30-game")
    elif(uid == "869895108" or uid == "863693239") and (("memory" in msg) or ("feel me lucky" in msg)):
        cl.append("memory-init")
    else:
        cl.append("xx")
    return msg   



def operator(msg,uid,p_beta):
    umsg = msg
    if cl[-1] == "alpha":
        cl.append("alpha-welcome")
        #txt = alphabet.welcome()
        txt = "Test 1"
        bot.send_message(txt,uid)
        
    elif cl[-1] == "play30-init":
        initplaythirty(umsg,uid,p_beta)
        #cl.append()
    elif cl[-1] == "play30-game":
        ptgameplay(umsg,uid,p_beta)
    elif cl[-1] == "memory-init":
        sendphotoinit(umsg,uid)
    elif cl[-1] == "xx":
        textmsg(umsg,uid)
        

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
            fname = item["message"]["from"]["first_name"]
            lname = item["message"]["from"]["last_name"]
            name = fname + " " + lname
            uname = item["message"]["from"]["username"]
            
            print(from_)
            print(name)
            print(uname)
            print(message.translate(non_bmp_map))
            print("\n")

            imessage = indexer(message,from_)
            operator(imessage,from_,p_beta)

                
