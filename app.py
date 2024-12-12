# -*- coding: utf-8 -*-

# 載入LineBot所需要的套件
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

line_bot_api.push_message('Ue67e135a8e71bb7f0a94eb6947e0dc32', TextSendMessage(text='你可以開始了'))

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

# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text

    # 當使用者輸入「推薦餐廳」時回傳 Imagemap
    if re.match('推薦餐廳', message):
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/your_restaurant_image.jpg', # 請替換為您的背景圖 URL
            alt_text='餐廳推薦',
            base_size=BaseSize(height=2000, width=2000),
            actions=[
                # 日式料理
                URIImagemapAction(
                    link_uri='https://www.google.com/maps/search/?api=1&query=Japanese+restaurant',
                    area=ImagemapArea(
                        x=0, y=0, width=1000, height=1000
                    )
                ),
                # 西式料理
                URIImagemapAction(
                    link_uri='https://www.google.com/maps/search/?api=1&query=Western+restaurant',
                    area=ImagemapArea(
                        x=1000, y=0, width=1000, height=1000
                    )
                ),
                # 中式料理
                URIImagemapAction(
                    link_uri='https://www.google.com/maps/search/?api=1&query=Chinese+restaurant',
                    area=ImagemapArea(
                        x=0, y=1000, width=1000, height=1000
                    )
                ),
                # 法式料理
                URIImagemapAction(
                    link_uri='https://www.google.com/maps/search/?api=1&query=French+restaurant',
                    area=ImagemapArea(
                        x=1000, y=1000, width=1000, height=1000
                    )
                ),
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)

    elif re.match('告訴我秘密', message):
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/xMUKNtn.jpg',
            alt_text='組圖訊息',
            base_size=BaseSize(height=2000, width=2000),
            actions=[
                URIImagemapAction(
                    link_uri='https://en.wikipedia.org/wiki/Cebu',
                    area=ImagemapArea(
                        x=0, y=0, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://en.wikipedia.org/wiki/Taipei',
                    area=ImagemapArea(
                        x=1000, y=0, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://en.wikipedia.org/wiki/Osaka',
                    area=ImagemapArea(
                        x=0, y=1000, width=1000, height=1000
                    )
                ),
                URIImagemapAction(
                    link_uri='https://en.wikipedia.org/wiki/Shanghai',
                    area=ImagemapArea(
                        x=1000, y=1000, width=1000, height=1000
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
