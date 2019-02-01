# -*- encoding: utf-8 -*-

from django.shortcuts import render
import json
import requests
from django.http import HttpResponse
from linebot import LineBotApi, WebhookHandler
import cv2
import numpy as np
import math
import io
from PIL import Image


class img2moon():
    # moon matrix for '🌕'
    moon0000 = np.array([[0,0,0,0],
                         [0,0,0,0],
                         [0,0,0,0],
                         [0,0,0,0]])

    # moon matrix for '🌖'
    moon0001 = np.array([[0,0,0,1],
                         [0,0,0,1],
                         [0,0,0,1],
                         [0,0,0,1]])
    # moon matrix for '🌗'
    moon0011 = np.array([[0,0,1,1],
                         [0,0,1,1],
                         [0,0,1,1],
                         [0,0,1,1]])

    # moon matrix for '🌘'
    moon0111 = np.array([[0,1,1,1],
                         [0,1,1,1],
                         [0,1,1,1],
                         [0,1,1,1]])

    # moon matrix for '🌑'
    moon1111 = np.array([[1,1,1,1],
                         [1,1,1,1],
                         [1,1,1,1],
                         [1,1,1,1]])


    # moon matrix for '🌒'
    moon1110 = np.array([[1,1,1,0],
                         [1,1,1,0],
                         [1,1,1,0],
                         [1,1,1,0]])

    # moon matrix for '🌓'
    moon1100 = np.array([[1,1,0,0],
                         [1,1,0,0],
                         [1,1,0,0],
                         [1,1,0,0]])


    # moon matrix for '🌔'
    moon1000 = np.array([[1,0,0,0],
                         [1,0,0,0],
                         [1,0,0,0],
                         [1,0,0,0]])

    moon_mats = (moon0000,moon0001,moon0011,moon0111,moon1111,moon1110,moon1100,moon1000)

    moon_index_list = []

    moon_list = ["🌕","🌖","🌗","🌘","🌑","🌒","🌓","🌔"]

    def __init__(self,binary_img):
        self.binary = binary_img
        self.hz_px = len(binary_img[0])
        self.vt_px = len(binary_img)
        self.hz_4x4box_num = int(math.floor(self.hz_px/4))
        self.vt_4x4box_num = int(math.floor(self.vt_px/4))

    def creat_moon_index_list(self):
        for row in range(self.vt_4x4box_num):
            moon_index_row = []
            for col in range(self.hz_4x4box_num):
                devide_mat4x4 = np.array([[self.binary[4*row][4*col],self.binary[4*row][4*col+1],self.binary[4*row][4*col+2],self.binary[4*row][4*col+3]],
                                          [self.binary[4*row+1][4*col],self.binary[4*row+1][4*col+1],self.binary[4*row+1][4*col+2],self.binary[4*row+1][4*col+3]],
                                          [self.binary[4*row+2][4*col],self.binary[4*row+2][4*col+1],self.binary[4*row+2][4*col+2],self.binary[4*row+2][4*col+3]],
                                          [self.binary[4*row+3][4*col],self.binary[4*row+3][4*col+1],self.binary[4*row+3][4*col+2],self.binary[4*row+3][4*col+3]]])
                index4small_distance = 0
                for index in range(len(self.moon_mats)):
                    if(np.linalg.norm(devide_mat4x4-self.moon_mats[index])<np.linalg.norm(devide_mat4x4-self.moon_mats[index4small_distance])):
                        index4small_distance = index

                moon_index_row.append(index4small_distance)

            self.moon_index_list.append(moon_index_row)

    def get_text(self):
        text = ""
        for indexes int self.moon_index_list:
            for index in indexes:
                text += self.moon_list[index]
            text += '\n'
        
        return text

    def print_moon_img(self):
        for indexs in self.moon_index_list:
            for index in indexs:
                sys.stdout.write(self.moon_list[index])
            print("")

    def output_txt(self,file_name):
        file = open(file_name,'w')
        for indexs in self.moon_index_list:
            for index in indexs:
                file.write(self.moon_list[index])
            file.write('\n')


# Create your views here.
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'g/GBZoNw/tTm8OWTln/4jN/yrgN6UNB+lIGwiWLxTgYnjiAOIp0exZGk8yVICB3X8Jl6ei4ikO7gikR9/HItoB3kO5YEYw5rZIUKfd2a/ciAft1WJP7+OmnBdFLLglFDYS4T6KZIocSNduy34il2NwdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " +  ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is bot api.")

def reply_text(reply_token, text):
    reply = text
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

# def get_and_save_content()

def disp_moon(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8'))  # to get json

    for e in request_json['events']:
        reply_token = e['replyToken']  # to get reply_token
        message_type = e['message']['type']  # to get type

        # reply for test
        if message_type == 'text':
            text = e['message']['text']  # to get message
            # rep_meg = client.talk(text)["results"][0]["reply"]  # to get reply message by recuitTalk
            reply += reply_text(reply_token, text)

            # reply for image
        if message_type == 'image':
            line_bot_api = LineBotApi(ACCESS_TOKEN)

            message_id = e['message']['id']  # to get messageID
            message_content = line_bot_api.get_message_content(message_id)
            img_pil = Image.open(BytesIO(message_content.content)) # バイナリストリーム -> PILイメージ
            img_np = np.asarray(img_pil) # PIL -> numpy配列(RGBA)
            img_np_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR) # RGBA -> BGR
            img_np_gray = cv2.cvtColor(img_np_bgr, cv2.COLOR_BGR2GRAY) # BGR -> GRAY

            ret, thresh_img = cv2.threshold(img_np_gray, 0, 255, cv2.THRESH_OTSU)

            moon_img = img2moon(thresh_img)
            moon_img.creat_moon_index_list()
            reply += reply_text(reply_token, text=moon_img.get_text())

    return HttpResponse(reply)  # for test



# @csrf_exempt
# def webhook(request):
#     if request.method != 'POST':
#         return HttpResponse('ん？なんやようか？', status=405)

#     signature = request.META['HTTP_X_LINE_SIGNATURE']
#     body = request.body.decode('utf-8')
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         return HttpResponseForbidden()
#     except LineBotApiError:
#         return HttpResponseBadRequest()

#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue

#         text_send_message = TextSendMessage(text=event.message.text)
#         line_bot_api.reply_message(
#             event.reply_token,
#             text_send_message
#         )

#     return HttpResponse(status=200)