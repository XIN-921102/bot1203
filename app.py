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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('000',message):
        carousel_template_message = TemplateSendMessage(
            alt_text='熱門旅行景點',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/xRBnJwk.png',
                        title='法羅群島',
                        text='Faroe Islands',
                        actions=[
                            URIAction(
                                label='導覽',
                                uri='https://maps.app.goo.gl/zTxbpMz9aTyEfAU77'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.canon.com.hk/tc/club/article/itemDetail.do?itemId=10496'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/ES4f9oQ.jpeg',
                        title='冰島',
                        text='Iceland',
                        actions=[
                            URIAction(
                                label='導覽',
                                uri='https://maps.app.goo.gl/NntWXAXjVxzsFuK49'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://zh.wikipedia.org/zh-tw/%E5%86%B0%E5%B2%9B'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/aRJXCWh.jpeg',
                        title='北海道',
                        text='Japan',
                        actions=[
                            URIAction(
                                label='導覽',
                                uri='https://maps.app.goo.gl/itU2dK1ccTTKaBENA'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://zh.wikipedia.org/zh-tw/%E5%8C%97%E6%B5%B7%E9%81%93'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
