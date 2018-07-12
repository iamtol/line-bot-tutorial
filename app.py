from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('JMrtslHAQGeBbpL/TZL8kuBtbkF3SYQYHeNFr/Mw+9eAATNEnSV3+6dr7u7N77VQN+BkC175m7TpAKeGVyjp/wRWfUYXN3L91KHVE1zH0ogdGEjSxxbJxhmjl3yqQyWWtI8uUGXEd45Eny8q39SVaAdB04t89/1O/w1cDnyilFU=')   #I put my TOKEN
handler = WebhookHandler('0ec2d401699e8d20e25f2db75131fc4b')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
