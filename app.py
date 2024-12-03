# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('h5osWA+HQKmjLSZ41tAc8z6KqHuqcj+68xPLvK80DENwG5JyUx3JDK7N7Q+BjtMn+9lUddWgOK1p6jVr3OOWOVx7f65YjpcaSz7/RvVD1p6jVr3OOWOVx7f65YjpcaS tsmIbwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('69d23835422ab468be99efec4a39b6cd')

line_bot_api.push_message('ud5e99dd7cbc1adb2020217e98bfcbab5', TextSendMessage(text='您好,目前時間是 2024/10/10 14:00 ，請問需要什麼服務呢?'))

# 監聽所有來自 /callback 的 Post Request
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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        # 貼圖查詢：https://developers.line.biz/en/docs/messaging-api/sticker-list/#specify-sticker-in-message-object
        sticker_message = StickerSendMessage(
            package_id='789',
            sticker_id='10857'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
