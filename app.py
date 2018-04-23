from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
import random
from parse_zodiac_sign import parse_zodiac

from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, ImageSendMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('9q7lPr4h4i/ypQ90Hy6DuH0jkdp5u6i94aQdyefwiS/fDsK9XCXBk25BJbLIs3hOzvij49V64FIHczNEGGBQn4LfZ8a2Rt3lDUOvjwKuZbSLZJlwqHfxkOWCj+vxb3uPUhxgNg55h14HEpaF+274FAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4b2fec6cc9da5c50b603bcfcd1039e52')
zodiac_signs = ['牡羊', '金牛', '雙子', '巨蟹', '獅子', '處女', '天秤', '天蠍', '射手', '羯', '水瓶', '雙魚']
zodiac_results = {'整體運勢': 'overview', '愛情運勢': 'love','事業學業運勢': 'work','財運運勢': 'wealth'}

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    
    for i, sign in enumerate(zodiac_signs):
        if text.find(sign) != -1:
            parse_result = zodiac.constellation(i) 
            buttons_template = ButtonsTemplate(
                title='您今天的運勢:', text='點選按鈕就可以看了喔<3', actions=[
                    MessageTemplateAction(label='整體運勢', text='我想看整體運勢'),
                    MessageTemplateAction(label='愛情運勢', text='我想看愛情運勢'),
                    MessageTemplateAction(label='事業學業運勢', text='我想看事業學業運勢'),
                    MessageTemplateAction(label='財運運勢', text='我想看財運運勢'),
                ])
            template_message = TemplateSendMessage(
                alt_text='您今天的運勢', template=buttons_template)
            line_bot_api.reply_message(event.reply_token, template_message)
            
            return

    for key, value in zodiac_results.items():
        if text.find(key) != -1:
            feedback = get_feedback(zodiac.result[value])
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text = zodiac.result[value]
                    ),
                    TextSendMessage(
                        text=zodiac.result[value + '_cont']
                    ),
                    feedback[0],
                    feedback[1],
                ]
            )
            return
    
    if text.find('不想') != -1:
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text = '嗚嗚好吧～那我們明天見Q'
                    ),
                    ImageSendMessage(
                        original_content_url='https://image.ibb.co/jhADSS/13132732.jpg',
                        preview_image_url='https://image.ibb.co/jhADSS/13132732.jpg'
                    )  
                ]
                
            )
    elif text.find('想') != -1:
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text = '想看的話只要輸入星座就可以查看了喔！ \n ex: 天蠍座'
                    )
                ]
            )
    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='不好意思，我聽不太懂耶! 想查詢今日運勢的話，請輸入您的星座'
                )
            ]
        )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    random_num = random.randint(180, 259)
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id='3',
            sticker_id=str(random_num))
    )

def get_feedback(stars):
    if stars.find('★★★★★') != -1:
        message = TextSendMessage(text="太棒了～祝你一整天順利呦")
        image_message = ImageSendMessage(
            original_content_url='https://image.ibb.co/nioggn/13132728.jpg',
            preview_image_url='https://image.ibb.co/nioggn/13132728.jpg'
        )  
    elif stars.find('★★★★☆') != -1:
        message = TextSendMessage(text="很不錯喔～今天一定能過得很棒")
        image_message = ImageSendMessage(
            original_content_url='https://image.ibb.co/cRmOu7/23620976.jpg',
            preview_image_url='https://image.ibb.co/cRmOu7/23620976.jpg'
        )  
    elif stars.find('★★★☆☆') != -1:
        message = TextSendMessage(text="只要努力一下，就會很好的！加油")
        image_message = ImageSendMessage(
            original_content_url='https://image.ibb.co/n3rOu7/13132763.jpg',
            preview_image_url='https://image.ibb.co/n3rOu7/13132763.jpg'
        )  
    elif stars.find('★★☆☆☆') != -1:
        message = TextSendMessage(text="不要難過，明天一定會更好的")
        image_message = ImageSendMessage(
            original_content_url='https://image.ibb.co/bvQ57S/13132735.jpg',
            preview_image_url='https://image.ibb.co/bvQ57S/13132735.jpg'
        )  
    elif stars.find('★☆☆☆☆') != -1:
        message = TextSendMessage(text="上面都是騙人的，不要難過")
        image_message = ImageSendMessage(
            original_content_url='https://image.ibb.co/fFkGE7/23620974.jpg',
            preview_image_url='https://image.ibb.co/fFkGE7/23620974.jpg'
        ) 
    else:
        message = TextSendMessage(text="還想看下一個嗎～可以繼續點上面的按鈕喔")
        image_message = ImageSendMessage(
            original_content_url='https://image.ibb.co/hsuySS/13132741.jpg',
            preview_image_url='https://image.ibb.co/hsuySS/13132741.jpg'
        ) 
    return [message, image_message]

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    zodiac = parse_zodiac()
    app.run(host='0.0.0.0', port=port)
    


