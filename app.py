# -*- coding: utf-8 -*-

# 載入 LineBot 所需要的套件
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
import os

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
    if re.match('電影推薦', message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='電影推薦',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/gMkJXKV.jpeg',
                        action=URIAction(
                            label='查看詳情',
                            uri='https://www.imdb.com/title/tt0111161/'  # 《刺激1995》
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/8pC5rSp.png',
                        action=URIAction(
                            label='查看詳情',
                            uri='https://www.imdb.com/title/tt0133093/'  # 《駭客任務》
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/mraKT3t.jpeg',
                        action=URIAction(
                            label='查看詳情',
                            uri='https://www.imdb.com/title/tt0110413/'  # 《阿甘正傳》
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/2mIVMLV.png',
                        action=URIAction(
                            label='查看詳情',
                            uri='https://www.imdb.com/title/tt1375666/'  # 《全面啟動》
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入「電影推薦」以獲取推薦電影列表。"))

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
