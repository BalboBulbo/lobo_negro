import os
import random as rnd
import smtplib as smtp
import configparser as cfg

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

config = cfg.ConfigParser()
config.read("setup.cfg")

email_info = config['EMAIL-SETUP']
dirs_info = config['SETUP']
players_info = {p for p in config['PLAYERS'].values()}
game_info = config['GAME']

print("Connecting To:"+email_info['server'])

s = smtp.SMTP(email_info['server'], email_info['port'])
s.ehlo()

if email_info['tls'] == 'Yes':
    s.starttls()
    s.ehlo()

s.login(email_info['user_name'], email_info['password'])


def send_email(to: str, img: str, text: str, subj=email_info['subject']):
    img_data = open(img, "rb").read()

    msg = MIMEMultipart()

    msg['subject'] = subj
    msg['From']  = email_info['user_name']
    msg['To'] = to


    txt = MIMEText(text)
    msg.attach(txt)

    image = MIMEImage(img_data, name=os.path.basename(img))
    msg.attach(image)


    s.sendmail(email_info['user_name'], to, msg.as_string())
    print("is:\t"+to)

def random_email(card: str):
    player = rnd.choice(list(players_info))
    players_info.remove(player)
    print("Next card to be send:\t"+card)
    img = dirs_info['img'] + config[card]['image']
    txt = open(dirs_info['txt'] + config[card]['text'], "r").read()
    
    send_email(player, img, txt)



for key in game_info.keys(): 
    [random_email(key.upper()) for _ in range(int(game_info[key]))]

s.quit()
