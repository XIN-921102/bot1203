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
line_bot_api = LineBotApi('grZNGQ4enesO10xsdNQNRHbKt4P4uYSU4LwSqDBPvR+G1gnnG4DgZE2WFHfLUpoCVE3tP3hLFrmmBTzqmTC5+Wy7P4o6fN825RpAyrHJ+ZKpm1xJ4IgCptwxSSvssovSlwnPe34cpkLYKCc3vd0BOwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b575b66d21e61d99d781691770236f63')

line_bot_api.push_message('U732b347d73dd0c11d034eb8233a15ef8', TextSendMessage(text='你可以開始了'))

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
    if re.match('電影推薦', message):
        carousel_template_message = TemplateSendMessage(
            alt_text='旅遊景點推薦',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://webcms.asset.catchplay.com/l/assets/img/article/article-988-iqrmyyxl/keyvisual.jpg',
                        title='玩命關頭',
                        text='位於北大西洋，風景如畫的島嶼。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://youtu.be/5gcuGLJN2uU?si=OsLTHiejZRYUQxxi'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvICT01Rkyp92NikjHTfCi7E2IiJ_4w1IDWQ&s',
                        title='海洋奇緣',
                        text='冰與火之國，擁有壯觀的極光與瀑布。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://youtu.be/0PjI4AyCEkw?si=fk5XR340ygEn4j6p'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://image-cdn.hypb.st/https%3A%2F%2Fhk.hypebeast.com%2Ffiles%2F2022%2F08%2Fjoker-2-sequel-joaquin-phoenix-2024-premiere-date-1.jpg?q=75&w=800&cbr=1&fit=max',
                        title='小丑',
                        text='希臘著名的藍白建築，適合觀賞日落。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://youtu.be/Eoook2Ee6q0?si=0wJAEgKCGiMBh3Bf'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://image.agentm.tw/images/movie/a142013b564a2f20929f3bdd09cf979baee7a4667734dcea850d9ecc42e0b695/poster/image/px_0004.jpg',
                        title='猛毒',
                        text='冰與火之國，擁有壯觀的極光與瀑布。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://youtu.be/fGErm6zGbGI?si=rWEXongA2f6p6vYX'
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
