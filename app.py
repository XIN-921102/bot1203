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
    if re.match('查看菜單', message):
        flex_message = FlexSendMessage(
            alt_text='餐廳菜單推薦',
            contents={
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Tokyo_Chikuyotei_Unadon01s2100.jpg/800px-Tokyo_Chikuyotei_Unadon01s2100.jpg",  # 替換為餐點圖片
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "鰻魚飯",
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                {
                                    "type": "text",
                                    "text": "密制醬汁，搭配特製烤鰻魚。",
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "價格: NT 350",
                                    "color": "#333333",
                                    "size": "md"
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "訂購",
                                        "data": "action=order&item=鰻魚飯"
                                    },
                                    "style": "primary",
                                    "color": "#905c44"
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://www.gomaji.com/blog/wp-content/uploads/2024/02/Snapinsta.app_307301802_1234327370470820_7001915545910360195_n_1080.jpg",  # 替換為餐點圖片
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "生魚片",
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                {
                                    "type": "text",
                                    "text": "新鮮光亮，口感滑順。",
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "價格: NT 300",
                                    "color": "#333333",
                                    "size": "md"
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "訂購",
                                        "data": "action=order&item=生魚片"
                                    },
                                    "style": "primary",
                                    "color": "#905c44"
                                }
                            ]
                        }
                    },
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://d3l76hx23vw40a.cloudfront.net/recipe/bk145-016.jpg",  # 替換為餐點圖片
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "雞排",
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                {
                                    "type": "text",
                                    "text": "口感酥脆。",
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "價格: NT 80",
                                    "color": "#333333",
                                    "size": "md"
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "postback",
                                        "label": "訂購",
                                        "data": "action=order&item=雞排"
                                    },
                                    "style": "primary",
                                    "color": "#905c44"
                                }
                            ]
                        }
                    }
                ]
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入有效的指令"))

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if "action=order" in data:
        item = data.split("&item=")[1]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"已成功將「{item}」加入購物車！")
        )

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
