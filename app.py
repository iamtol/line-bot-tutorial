import requests
import re
import random
import configparser
import urllib
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']
API_Get_Image = config['other_api']['API_Get_Image']


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def pattern_mega(text):
    patterns = [
        'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
        'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
        
def technews():
    target_url = 'https://www.blognone.com/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('div h2 a')):
        if index == 5:
            return content
        title = data.text
        link = "https://www.blognone.com" + data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content

def checkstatus():
    target_url = 'https://s3-ap-southeast-1.amazonaws.com/mdstatus/md_status/example_j.json'
    print('Start parsing web ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    content = res.text
    return content


def checknode():
    target_url = 'https://s3-ap-southeast-1.amazonaws.com/mdstatus/md_status/example_j.json'
    print('Start parsing web ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    data = res.json()
    json_str = json.dumps(data)
    content = json.loads(json_str)
    return content

#def checkstatus():
#    data=urllib2.urlopen("https://s3-ap-southeast-1.amazonaws.com/mdstatus/md_status/example_j.json")
#    for content in data:
#        print (content)
#    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == "tech":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "server":
        content = checkstatus()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "main_cdr":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Voice\nPatcharaporn Uadglar <patchaud@ais.co.th> : 6586\nAnucha Santana <anuchasa@ais.co.th> : 6707\n\nData\nPachara Towattanakit <somphont@ais.co.th> : 6586\nPatcharaporn Uadglar <patchaud@ais.co.th> : 6586'))
        return 0
    
    if event.message.text == "online_bill":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='BOS\nAnucha Santana <anuchasa@ais.co.th> : 6707\nThanawan Katecha <thanawkt@ais.co.th> : 6027\n\nAvatar ans INS\nWarat Thintapthai <warat307@kston.postbox.in.th> : 8533\nPiya Wongharichao <piyawong@ais.co.th>'))
        return 0    
    
    if event.message.text == "hcs_cdr":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='HCS\nThanawan Katecha <thanawkt@ais.co.th> : 6027\n\nCDR Search\nPatcharaporn Uadglar <patchaud@ais.co.th> : 6586'))
        return 0     
    
    if event.message.text == "another":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Leader\nOngsakorn Treesinchai <ongsakot@ais.co.th> : 6686\n\nMember:\nPachara Towattanakit <somphont@ais.co.th> : 6586\nPatcharaporn Uadglar <patchaud@ais.co.th> : 6586\nAnucha Santana <anuchasa@ais.co.th> : 6707\nThanawan Katecha <thanawkt@ais.co.th> : 6027\nPiya Wongharichao <piyawong@ais.co.th>'))
        return 0     
    
    if event.message.text == "mdcdr801":
        status = checknode()
        content = status['mdcdr801']
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "เช็คสถานะเซิฟเวอร์":
        buttons_template = TemplateSendMessage(
            alt_text='menu template',
            template=ButtonsTemplate(
                title='เลือกบริการ',
                text='โปรดเลือก',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='MDCDR801',
                        text='mdcdr801'
                    ),
                    MessageTemplateAction(
                        label='MDCDR802',
                        text='mdcdr802'
                    ),
                    MessageTemplateAction(
                        label='MDCDR803',
                        text='mdcdr803'
                    ),
                    MessageTemplateAction(
                        label='MDCDR804',
                        text='mdcdr804'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    
    if event.message.text == "contacts":
        buttons_template = TemplateSendMessage(
            alt_text='contacts template',
            template=ButtonsTemplate(
                title='เลือกประเภทของเรื่องที่ต้องการติดต่อ',
                text='โปรดเลือก',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='Voice/Data/Rated-CDR',
                        text='main_cdr'
                    ),
                    MessageTemplateAction(
                        label='BOS/INS/AVATAR',
                        text='online_bill'
                    ),
                    MessageTemplateAction(
                        label='HCS/CDR Search',
                        text='hcs_cdr'
                    ),
                    MessageTemplateAction(
                        label='อื่นๆ',
                        text='another'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0 
    
if __name__ == '__main__':
    app.run()
