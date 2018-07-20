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
    
    if event.message.text == "menu":
        buttons_template = TemplateSendMessage(
            alt_text='menu template',
            template=ButtonsTemplate(
                title='เลือกบริการ',
                text='โปรดเลือก',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='เทค',
                        text='tech'
                    ),
                    MessageTemplateAction(
                        label='หนัง',
                        text='movies'
                    ),
                    MessageTemplateAction(
                        label='สถานะ server',
                        text='server'
                    ),
                    MessageTemplateAction(
                        label='ข่าวดัง',
                        text='news'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    
if __name__ == '__main__':
    app.run()
