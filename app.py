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
line_bot_api = LineBotApi('RmscZ3tXPFTa3C+xKp9zU2zcapRysd2Lp/tRNkQT3a6FxxKY6XoTexhaMoarJVpf9X5PkvNRpFYLJJCpYJSlQfuPQ4VjgkuX46HOeXIv+fHJuqhaUGhSLXaWVsAqgVkY+zXzx40QYJL+d0GVK6BRQQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('dde3f81dc0ffc12b0b826d473d1c7fa3')

line_bot_api.push_message('Ue67e135a8e71bb7f0a94eb6947e0dc32', TextSendMessage(text='您好,目前時間是 2024/10/10 14:00 ，請問需要什麼服務呢?'))

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
    if message == '天氣':
        reply_text = '請稍等，我幫您查詢天氣資訊！'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))

    elif message == '心情好':
        sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002735'  # 開心的貼圖
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)

    elif message == '心情不好':
        sticker_message = StickerSendMessage(
            package_id='11538',
            sticker_id='51626518'  # 傷心的貼圖
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)

    elif message == '找美食':
        location_message = LocationSendMessage(
            title='著名餐廳',
            address='台北市信義區松壽路12號',
            latitude=25.035774,  # 餐廳的緯度
            longitude=121.567414  # 餐廳的經度
        )
        line_bot_api.reply_message(event.reply_token, location_message)

    elif message == '找景點':
        location_message = LocationSendMessage(
            title='熱門景點',
            address='台北市大安區羅斯福路四段1號',
            latitude=25.017341,  # 景點的緯度
            longitude=121.539752  # 景點的經度
        )
        line_bot_api.reply_message(event.reply_token, location_message)

    else:
        reply_text = '很抱歉，我目前無法理解這個內容。'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
