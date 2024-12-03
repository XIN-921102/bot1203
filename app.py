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
line_bot_api = LineBotApi('grZNGQ4enesO10xsdNQNRHbKt4P4uYSU4LwSqDBPvR+G1gnnG4DgZE2WFHfLUpoCVE3tP3hLFrmmBTzqmTC5+Wy7P4o6fN825RpAyrHJ+ZKpm1xJ4IgCptwxSSvssovSlwnPe34cpkLYKCc3vd0BOwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('b575b66d21e61d99d781691770236f63')

line_bot_api.push_message('U732b347d73dd0c11d034eb8233a15ef8', TextSendMessage(text='您好,目前時間是 2024/10/10 14:00 ，請問需要什麼服務呢?'))

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
            latitude=25.035774,
            longitude=121.567414
        )
            line_bot_api.reply_message(event.reply_token, location_message)

    elif message == '找景點':
            location_message = LocationSendMessage(
            title='熱門景點',
            address='台北市大安區羅斯福路四段1號',
            latitude=25.017341,
            longitude=121.539752
        )
            line_bot_api.reply_message(event.reply_token, location_message)

    elif message == '熱門音樂':
            audio_message = AudioSendMessage(
            original_content_url='https://youtu.be/oxWz_j2JDuA?si=WDWEZInKoLN2pFsk',  # 替換為實際的音樂檔案網址
            duration=240000  # 音樂長度（毫秒）
        )
            line_bot_api.reply_message(event.reply_token, audio_message)

    elif message == '放鬆音樂':
            audio_message = AudioSendMessage(
            original_content_url='https://youtu.be/wlSvIL-H1GQ?si=qj3IrsAJ1TkZ8msr',  # 替換為實際的音樂檔案網址
            duration=300000  # 音樂長度（毫秒）
        )
            line_bot_api.reply_message(event.reply_token, audio_message)

    elif message == '今天是我的生日':
            image_message = ImageSendMessage(
            original_content_url='https://www.yesonlineeng.com/wp-content/uploads/2024/06/%E7%94%9F%E6%97%A5%E5%BF%AB%E6%A8%82%E8%8B%B1%E6%96%87.jpg',  # 替換為實際的圖片網址
            preview_image_url='https://img.lovepik.com/png/20230929/happy-birthday-birthday-banner-birthday-invitation-birthday-font_26482_wh1200.png'  # 替換為實際的預覽圖片網址
        )
            text_message = TextSendMessage(text='生日快樂！')
            line_bot_api.reply_message(event.reply_token, [image_message, text_message])

    elif message in ['動作片', '動畫', '紀錄片']:
        # 根據類型傳送影片
        video_urls = {
            '動作片': 'https://youtu.be/tYgxCJWD_5Y?si=WWENRbz2UZC4yLJe',
            '動畫': 'https://youtu.be/Y3roUIXa2Fg?si=nD8o6RADdZM7JWVO',
            '紀錄片': 'https://youtu.be/vmnuj5SoG-o?si=W20CtpegkCQ4LQdR'
        }
        video_url = video_urls.get(message)
        if video_url:
            reply_text = f'這是您要的{message}：\n{video_url}'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
        else:
            reply_text = '抱歉，沒有這類型的影片'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))

    elif message in ['科幻']:
            reply_text = '抱歉，沒有這類型的影片'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))

    else:
            reply_text = '很抱歉，我目前無法理解這個內容。'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
