import requests
import re
import random
import configparser
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
        content += '{}\n{}\n'.format(title, link)
    return content

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
    
    if event.message.text == "เริ่มเล่น":
        buttons_template = TemplateSendMessage(
            alt_text='เริ่มเล่น template',
            template=ButtonsTemplate(
                title='เลือกบริการ',
                text='โปรดเลือก',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='เทค',
                        text='เทค'
                    ),
                    MessageTemplateAction(
                        label='หนัง',
                        text='หนัง'
                    ),
                    MessageTemplateAction(
                        label='อื่นๆ',
                        text='อื่นๆ'
                    ),
                    MessageTemplateAction(
                        label='ข่าวดัง',
                        text='ข่าวดัง'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "ข่าว":
        buttons_template = TemplateSendMessage(
            alt_text='ข่าว template',
            template=ButtonsTemplate(
                title='ประเภทข่าว',
                text='โปรดเลือก',
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                actions=[
                    MessageTemplateAction(
                        label='ข่าวด่วนของ Apple',
                        text='ข่าวด่วนของ Apple'
                    ),
                    MessageTemplateAction(
                        label='เทค',
                        text='เทค'
                    ),
                    MessageTemplateAction(
                        label='PanX Pan เทคโนโลยี',
                        text='PanX Pan เทคโนโลยี'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
if __name__ == '__main__':
    app.run()
