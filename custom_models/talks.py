from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage

import configparser

import random

# 我們的函數
from custom_models import utils, calldata

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

# 請 LINE 幫我們存入資料
def insert_record(event):
    
    if '咖啡紀錄' in event.message.text:
        
        try:
            record_list = utils.prepare_record(event.message.text)
            reply = calldata.line_insert_record(record_list)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )

        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='失敗了')
            )

        return True
    else:
        return False



# 請 pixabay 幫我們找圖
def img_search(event):
    
    try:
        try:
            img_source = event.message.text.split(' ')[0].lower()
            target = event.message.text.split(' ')[1]
            random_img_url = utils.get_img_url(img_source=img_source, target=target)
            
        except:
            random_img_url = utils.get_img_url(img_source='pixabay', target=event.message.text)

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=random_img_url,
                preview_image_url=random_img_url
            )
        )
        
        return True
    
    except:
        return False
