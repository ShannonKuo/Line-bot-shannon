from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
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
line_bot_api = LineBotApi('Cl3jVd/y4GpkqurC/63xKqWYGWx9vtYMLArtyALsRUquhUyUS/jHaXif1Ua2XbfOJG197JBfdx3VesvwjCpQQeEsqTSfNmZOZPmnkViegy8zVxN6O9FSKrcNXqyrqsvTKlgTvZzoQkHd08pLyBs1QAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f787f1305680c20fc61c962950fcfefd')

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
    if text == '天蠍':
        buttons_template = ButtonsTemplate(
            title='您今天的運勢', text='以下是您的運勢', actions=[
                MessageTemplateAction(label='整體運勢', text='我想看整體運勢'),
                MessageTemplateAction(label='愛情運勢', text='我想看愛情運勢'),
                MessageTemplateAction(label='事業學業運勢', text='我想看事業學業運勢'),
                MessageTemplateAction(label='財運運勢', text='我想看財運運勢'),
            ])
        template_message = TemplateSendMessage(
            alt_text='您今天的運勢', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text.find('整體運勢') != -1:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='您今天的整體運勢是 五顆星'
                ),
                TextSendMessage(
                    text='內容'
                )
            ]
        )
    elif text.find('愛情運勢') != -1:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='您今天的愛情運勢是 五顆星'
                ),
                TextSendMessage(
                    text='內容'
                )
            ]
        )
    elif text.find('事業學業運勢') != -1:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='您今天的事業學業運勢是 五顆星'
                ),
                TextSendMessage(
                    text='內容'
                )
            ]
        )
    elif text.find('財運運勢') != -1:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='您今天的財運運勢是 五顆星'
                ),
                TextSendMessage(
                    text='內容'
                )
            ]
        )
    elif text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text='Status message: ' + profile.status_message
                    )
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))
    elif text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't leave from 1:1 chat"))
    elif text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://images.pexels.com/photos/370799/pexels-photo-370799.jpeg?auto=compress&cs=tinysrgb&h=350',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'image':
        image_message = ImageSendMessage(
            original_content_url='https://images.pexels.com/photos/370799/pexels-photo-370799.jpeg?auto=compress&cs=tinysrgb&h=350',
            preview_image_url='https://images.pexels.com/photos/370799/pexels-photo-370799.jpeg?auto=compress&cs=tinysrgb&h=350'
        )   
        line_bot_api.reply_message(event.reply_token, image_message)
    elif text == 'imagemap':
        pass

    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(
                    text='不好意思，我聽不太懂耶'
                )
            ]
        )

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id='4',
            sticker_id='632')
    )
def handle_ask_zodiac_sign(event):
    if text == '好':
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="那你可以給我你的星座嗎？"
                )
        )
    elif text == '不好':
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="嗚嗚好吧～那我們明天見囉"
                )
        )
    else:
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="對不起，我聽不太懂耶\n 如果想看運勢的話請回 好 "
                )
        )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


