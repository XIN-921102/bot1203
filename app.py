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
    if re.match('推薦景點',message):
        carousel_template_message = TemplateSendMessage(
            alt_text='熱門旅行景點',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.todaiji.or.jp/wp-content/uploads/2022/02/daibutsuden00.jpg',
                        title='東大寺',
                        text='Todaiji Temple',
                        actions=[
                            URIAction(
                                label='導覽',
                                uri='https://www.todaiji.or.jp/zh/information/daibutsuden/'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://www.todaiji.or.jp/zh/information/daibutsuden/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/c/c2/01_khafre_north.jpg',
                        title='埃及金字塔',
                        text='egyptian pyramidsd',
                        actions=[
                            URIAction(
                                label='導覽',
                                uri='https://ninetyroadtravel.com/egypt/khufu/'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://zh.wikipedia.org/zh-tw/%E5%9F%83%E5%8F%8A%E9%87%91%E5%AD%97%E5%A1%94'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo3PtF0hSIGEHu43UDbwtPQNyoCLQSN0n4sA&s',
                        title='漁人碼頭',
                        text='fisherman',
                        actions=[
                            URIAction(
                                label='導覽',
                                uri='https://www.travelking.com.tw/tourguide/taipei/scenery1105.html'
                            ),
                            URIAction(
                                label='詳細資訊',
                                uri='https://zh.wikipedia.org/zh-tw/%E6%B7%A1%E6%B0%B4%E6%BC%81%E4%BA%BA%E7%A2%BC%E9%A0%AD'
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
