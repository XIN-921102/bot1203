# -*- coding: utf-8 -*-

# 載入 LineBot 所需要的套件
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import re

app = Flask(__name__)

# 必須放上自己的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('RmscZ3tXPFTa3C+xKp9zU2zcapRysd2Lp/tRNkQT3a6FxxKY6XoTexhaMoarJVpf9X5PkvNRpFYLJJCpYJSlQfuPQ4VjgkuX46HOeXIv+fHJuqhaUGhSLXaWVsAqgVkY+zXzx40QYJL+d0GVK6BRQQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dde3f81dc0ffc12b0b826d473d1c7fa3')

line_bot_api.push_message('Ue67e135a8e71bb7f0a94eb6947e0dc32', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 POST 請求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息處理邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('旅遊推薦', message):
        carousel_template_message = TemplateSendMessage(
            alt_text='旅遊景點推薦',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/5IfWEYi.jpeg',
                        title='法羅群島',
                        text='位於北大西洋，風景如畫的島嶼。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://maps.app.goo.gl/x5GCp2GM1N7yA5XG7'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/Zv687p8.jpeg',
                        title='冰島',
                        text='冰與火之國，擁有壯觀的極光與瀑布。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://maps.app.goo.gl/drBLg8SpYMUHHPZ56'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/m9ENy4Q.jpeg',
                        title='聖托里尼',
                        text='希臘著名的藍白建築，適合觀賞日落。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://maps.app.goo.gl/pnEmq3S39bSXG8nS8'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入「旅遊推薦」以獲取推薦景點列表。"))


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
