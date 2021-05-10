# -*- coding: utf-8 -*-

import urllib
import urllib.parse
import urllib.request
import urllib.error
import requests as rq

from bs4 import BeautifulSoup

#引数取得
import sys
args = sys.argv
file_import = args[1]

#レッスンファイルを読み込む
from importlib import import_module
resson = import_module("resson.r" + file_import)

#日時を計算する
import time
import datetime
from dateutil.parser import parse
#import pandas as pd


#sys.exit()

#検索文字列
login_id = "work@kuttu.net"
password = "kutu0427"
reserve_string = "reserve-form"

string = resson.string
s_date = resson.s_date
e_date = resson.e_date
pos = resson.pos

#Session接続
ses = rq.Session()

#ログイン
url = "https://i.tipness.co.jp/i/auth/login"
params = {"login_id":login_id, "login_pass" : password,"auto_login":1 }
#sessionでPOST
st = ses.post(url,params=params)
print('login_status:'+str(st.status_code))
with open('file.txt', 'w') as f:
  print(st.text, file=f)

##### 予約・確認画面 #####
url2 = "https://i.tipness.co.jp/i/reservation/"
st2 = ses.get(url2)
print('login_status:'+str(st2.status_code))
with open('file2.txt', 'w') as f:
  print(st2.text, file=f)

##### レッスン予約サービス予約画面 #####
url3 = "https://i.tipness.co.jp/i/rsv3/?type=4"
st3 = ses.get(url3)
print('login_status:'+str(st3.status_code))
with open('file3.txt', 'w') as f:
  print(st3.text, file=f)

##### レッスン予約サービス予約画面 #####
url4 = "https://i.tipness.co.jp/i/rsv3/form"
st4 = ses.get(url4)
print('login_status:'+str(st4.status_code))
with open('file4.txt', 'w') as f:
  print(st4.text, file=f)

##### 検索画面(検索前に時間までsleep) #####
#現在時刻のUNIXタイムスタンプ
ut_now = int(time.time())
dt_now = datetime.datetime.now()
dt_today = dt_now.strftime('%Y-%m-%d')
dt_s_reserve = dt_today + ' ' + resson.time_s_reserve
ut_s_reserve = int(parse(dt_s_reserve).timestamp())
print(dt_s_reserve)
print(ut_s_reserve)
#待ち時間(秒)
wait_seconds = ut_s_reserve - ut_now + 1
print(wait_seconds)

time.sleep(wait_seconds)

url5 = "https://i.tipness.co.jp/i/rsv3/search"
params5 = {
  "p":0,
  "v" : 10,
  "cond[shop_id]":resson.shop_id,
  "cond[s_date]":s_date,
  "cond[e_date]":e_date,
}
st5 = ses.post(url5,params5)
print('login_status:'+str(st5.status_code))
with open('file5.txt', 'w') as f:
  print(st5.text, file=f)

##### 検索結果画面 #####
SOUP = BeautifulSoup(st5.text, "html.parser")
RES = SOUP.find(text=string)
next_link = (RES.parent.parent.parent.find("p", recursive=False).find("a", recursive=False).get("href"))

url6 = "https://i.tipness.co.jp/i/rsv3/" + next_link
st6 = ses.get(url6)
print('login_status:'+str(st6.status_code))
with open('file6.txt', 'w') as f:
  print(st6.text, file=f)

##### レッスン予約サービス予約 #####
SOUP = BeautifulSoup(st6.text, "html.parser")
RES = SOUP.find(id=reserve_string)
input_array = RES.find_all("input")
hash_string = input_array[1].get("value")

url7 = "https://i.tipness.co.jp/i/rsv3/confirm"
params7 = {
  "ticket":0,
  "hash" : hash_string,
}
st7 = ses.post(url7,params7)
print('login_status:'+str(st7.status_code))
with open('file7.txt', 'w') as f:
  print(st7.text, file=f)

##### 席選ぶ画面 #####
url8 = "https://i.tipness.co.jp/i/rsv3/confirm"
params8 = {
  "pos":pos,
}
st8 = ses.post(url8,params8)
print('login_status:'+str(st8.status_code))
with open('file8.txt', 'w') as f:
  print(st8.text, file=f)


##### 確認画面 #####
SOUP = BeautifulSoup(st8.text, "html.parser")
RES = SOUP.find(id="reserve-form")
input_array = RES.find_all("input")
hash_string = input_array[0].get("value")

url9 = "https://i.tipness.co.jp/i/rsv3/reserve"
params9 = {
  "hash":hash_string,
  "email":1,
  "password":password,
}
st9 = ses.post(url9,params9)
print('login_status:'+str(st9.status_code))
with open('file9.txt', 'w') as f:
  print(st9.text, file=f)

