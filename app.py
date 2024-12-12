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

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('告訴我秘密', message):
        buttons_template_message = TemplateSendMessage(
            alt_text='這是樣板傳送訊息',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/frXs2nV.jpeg',
                title='中華民國',
                text='選單功能－TemplateSendMessage',
                actions=[
                    PostbackAction(
                        label='這是PostbackAction',
                        display_text='顯示文字',
                        data='實際資料'
                    ),
                    MessageAction(
                        label='這是MessageAction',
                        text='實際資料'
                    ),
                    URIAction(
                        label='這是URIAction',
                        uri='https://en.wikipedia.org/wiki/Taiwan'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

    elif re.match('推薦景點', message):
        carousel_template_message = TemplateSendMessage(
            alt_text='旅遊景點推薦',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/3UK5bhI.jpeg', # 台北101示意圖
                        title='台北101',
                        text='世界著名地標與購物中心',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://zh.wikipedia.org/wiki/台北101'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/frXs2nV.jpeg', # 故宮博物院示意圖
                        title='故宮博物院',
                        text='收藏中華文化藝術珍品',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://www.npm.gov.tw/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qadTNYk.jpeg', # 九份老街示意圖
                        title='九份老街',
                        text='懷舊山城、茶館與特產',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://zh.wikipedia.org/wiki/九份'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
