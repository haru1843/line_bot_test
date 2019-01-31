# -*- encoding: utf-8 -*-

# from django.shortcuts import render
# import json
# import requests
# from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
# Create your views here.

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'K1OkmS/ONGZyfiSxAfcyo6lwUPwLQexJQ1NRZqveFlyIg9u7/xCYSSMh9OGxTRU58Jl6ei4ikO7gikR9/HItoB3kO5YEYw5rZIUKfd2a/cgFrqz9BHl36dZrIPGUENxrIgZ1/0E3ILFuzRo7QtDn/AdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " +  ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is bot api.")

def reply_text(reply_token, text):
    reply = "hello"
    payload = {
        "replyToken": reply_token,
        "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }
    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # lineにデータを送信
    return reply

def callback(request):
    reply=""
    request_json = json.loads(request.body.decode('utf-8'))

    for event in request_json['events']:
        reply_token = event['replyToken'] # 返信先のトークンの取得
        message_type = event['message']['type']

        if message_type == 'text':
            text = event['message']['text'] # 受信メッセージの取得
            reply += reply_text(reply_token, text)
    
    return HttpResponse(reply)

line_bot_api = LineBotApi('K1OkmS/ONGZyfiSxAfcyo6lwUPwLQexJQ1NRZqveFlyIg9u7/xCYSSMh9OGxTRU58Jl6ei4ikO7gikR9/HItoB3kO5YEYw5rZIUKfd2a/cgFrqz9BHl36dZrIPGUENxrIgZ1/0E3ILFuzRo7QtDn/AdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('c15e393c696f8ffa024eaad30a42a2db')


@csrf_exempt
def webhook(request):
    if request.method != 'POST':
        return HttpResponse('ん？なんやようか？', status=405)

    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        text_send_message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            text_send_message
        )

    return HttpResponse(status=200)