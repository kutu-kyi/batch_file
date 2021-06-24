##### ステータスがenableのポジション配列を取得 #####
def get_position_enable(html_text):
  import json
  html_lines = html_text.split("\n")

  #各行をチェック
  for html_line in html_lines:
    #「RsvApp.mapData」というテキストが入っていたら
    if "RsvApp.mapData" in html_line:
      #"RsvApp.mapData"と"="と";"と半角スペースを削除
      html_data = html_line.replace("RsvApp.mapData = ","")
      html_data = html_data.replace("=","")
      html_data = html_data.replace(";","")
      html_json = html_data.replace(" ","")

      html_dict = json.loads(html_json)
      position_datas = html_dict['data']

      #ポジションデータを全チェック
      position_enables = {}
      for position_data in position_datas:
        #enabelのポジションを取得
        if position_data['status']=="enable":
          #position_enables[position_data['y']]がdictになっていなかったらdict宣言
          if position_data['y'] not in position_enables:
            if type(position_data['y']) != 'dict':
              position_enables[position_data['y']] = {}

          position_enables[position_data['y']][position_data['x']] = position_data['status']

      # 「RsvApp.mapData」というテキストを見つけて処理が終わればbreak
      break
  return position_enables

##### 指定したポジションが空いているかチェック #####
def check_enable(position):
  return position