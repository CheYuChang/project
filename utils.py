import os

from linebot import LineBotApi, WebhookParser
from linebot.models import *

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_temp_message(reply_token, title, text, choose, url):
    
    message = TemplateSendMessage(
        alt_text=' templatemessage',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = choose
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)

    return "OK"


def send_carousel_message(reply_token,title,col):
    message=TemplateSendMessage(
        alt_text=title,
        template=ImageCarouselTemplate(
            columns=col
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    
    return "OK"
       
def send_confirm_message(reply_token,text,title,col):
    message  = TemplateSendMessage(
             alt_text=text,
             template=ConfirmTemplate(
                 text=title,
                 actions=col
             )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    
    return "OK"

def send_sure_message(reply_token):
    message = TextSendMessage(
        text='確定要衝動購物嗎!!!',
        quick_reply=QuickReply(items=[
            
            QuickReplyButton(action=MessageAction(label="我就是要敗家", text="購物")),
            QuickReplyButton(action=MessageAction(label="看看而已啦", text="購物")),
            QuickReplyButton(action=MessageAction(label="有意志力這種東西", text="購物")),
            QuickReplyButton(action=MessageAction(label="剛領薪水", text="購物")),
            QuickReplyButton(action=MessageAction(label="還是算了", text="主選單")),
                                ]))
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    
    return "OK"

"""
def send_image_url(id, img_url):
    pass
def send_button_message(id, text, buttons):
    pass
"""