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
import random
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
    stickers = [
        {"package_id": "446", "sticker_id": "1988"},
        {"package_id": "789", "sticker_id": "10855"},
        {"package_id": "1070", "sticker_id": "17839"},
        {"package_id": "6136", "sticker_id": "10551376"},
        {"package_id": "6325", "sticker_id": "10979904"},
    ]

    if event.message.text:
        # 隨機選擇一個貼圖
        sticker = random.choice(stickers)
        sticker_message = StickerSendMessage(
            package_id=sticker["package_id"],
            sticker_id=sticker["sticker_id"]
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    else:
        reply_text = '很抱歉，我目前無法理解這個內容。'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))

    if message == '天氣':
            reply_text = '請稍等，我幫您查詢天氣資訊！'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(reply_text))

    elif message == '心情好':
            sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002734'  # 開心的貼圖
        )
            line_bot_api.reply_message(event.reply_token, sticker_message)

    elif message == '心情不好':
            sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002750'  # 傷心的貼圖
        )
            line_bot_api.reply_message(event.reply_token, sticker_message)

    elif message == '找美食':
            location_message = LocationSendMessage(
            title='著名餐廳',
            address='Gordon Ramsay Pub & Grill',
            latitude=22.14726876398457,
            longitude=113.56505331030235
        )
            line_bot_api.reply_message(event.reply_token, location_message)

    elif message == '找景點':
            location_message = LocationSendMessage(
            title='熱門景點',
            address='Hylton Castle',
            latitude=54.92642132251696,
            longitude=-1.4441933898550596
        )
            line_bot_api.reply_message(event.reply_token, location_message)

    elif message == '熱門音樂':
            audio_message = AudioSendMessage(
            original_content_url='https://www.youtube.com/watch?v=mUhJUNJCcQ0',  # 替換為實際的音樂檔案網址
            duration=240000  # 音樂長度（毫秒）
        )
            line_bot_api.reply_message(event.reply_token, audio_message)

    elif message == '放鬆音樂':
            audio_message = AudioSendMessage(
            original_content_url='https://www.youtube.com/watch?v=ekr2nIex040',  # 替換為實際的音樂檔案網址
            duration=300000  # 音樂長度（毫秒）
        )
            line_bot_api.reply_message(event.reply_token, audio_message)

    elif message == '今天是我的生日':
            image_message = ImageSendMessage(
            original_content_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTev_tjnQuGPY3SXZ4nznPgJqd9juRuBRoOw&s',  # 替換為實際的圖片網址
            preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTev_tjnQuGPY3SXZ4nznPgJqd9juRuBRoOw&s'  # 替換為實際的預覽圖片網址
        )
            text_message = TextSendMessage(text='生日快樂！')
            line_bot_api.reply_message(event.reply_token, [image_message, text_message])

    elif message in ['動作片', '動畫', '紀錄片']:
        # 根據類型傳送影片
        video_urls = {
            '動作片': 'https://youtu.be/J4e68cK4FY0?si=LoDixR5kbjuLp9PH',
            '動畫': 'https://youtu.be/Io9X8Clv3Xk?si=BFCVLv3JpwUiDXmD',
            '紀錄片': 'https://youtu.be/IbaJ1hYYFH8?si=pC6A9DMzgzwECvh3'
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
