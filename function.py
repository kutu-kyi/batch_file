##### ステータスがenableのポジション配列を取得 #####
def get_position_enable(html_text):
  import json
  html_lines = html_text.split("\n")

  # 各行をチェック
  for html_line in html_lines:
    # 「RsvApp.mapData」というテキストが入っていたら
    if "RsvApp.mapData" in html_line:
      # "RsvApp.mapData"と"="と";"と半角スペースを削除
      html_data = html_line.replace("RsvApp.mapData = ", "")
      html_data = html_data.replace("=", "")
      html_data = html_data.replace(";", "")
      html_json = html_data.replace(" ", "")

      html_dict = json.loads(html_json)
      position_datas = html_dict['data']

      # ポジションデータを全チェック
      position_enables = {}
      for position_data in position_datas:
        # enabelのポジションを取得
        #        if position_data['status']=="enable":
        # position_enables[position_data['y']]がdictになっていなかったらdict宣言
        if position_data['y'] not in position_enables:
          if type(position_data['y']) != 'dict':
            position_enables[position_data['y']] = {}

        position_enables[position_data['y']][position_data['x']] = position_data['status']

      # 「RsvApp.mapData」というテキストを見つけて処理が終わればbreak
      break
  return position_enables


##### 指定したポジションが空いているかチェック #####
def check_enable(position,position_enables):
    position_dict = position.split(':')
#    print(position_enables[int(position_dict[0])][int(position_dict[1])])
    #指定したポジションが"enable"ならそのポジションを返す
    if(position_enables[int(position_dict[0])][int(position_dict[1])]=='enable'):
        return position
    else:
        #ポジション配列を全てチェックして"enable"であったポジションを返す
        for y in range(0, len(position_enables)):
            for x in range(0,len(position_enables[y])):
                if(position_enables[y][x]=="enable"):
                    position_new = str(y)+':'+str(x)
                    return (position_new)

    return position
