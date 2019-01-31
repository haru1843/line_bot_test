# -*- encoding: utf-8 -*-

from django.shortcuts import render
import json
import requests
# Create your views here.

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'K1OkmS/ONGZyfiSxAfcyo6lwUPwLQexJQ1NRZqveFlyIg9u7/xCYSSMh9OGxTRU58Jl6ei4ikO7gikR9/HItoB3kO5YEYw5rZIUKfd2a/cgFrqz9BHl36dZrIPGUENxrIgZ1/0E3ILFuzRo7QtDn/AdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " +  ACCESS_TOKEN
}

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