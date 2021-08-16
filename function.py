##### ステータスがenableのポジション配列を取得 #####
def get_position_enable(html_text):
  import json
  html_lines = html_text.split("\n")
  html_data = ""

  # 各行をチェック
  for html_line in html_lines:
    # html_dataにまだ何も入っていない
    if html_data == "":
      # 「RsvApp.mapData」というテキストが入っていたら
      if "RsvApp.mapData" in html_line:
        # html_dataに改行と半角空白を除いたhtml_lineを入れる
        html_data = html_line.strip()
    #      continue

    else:
      # html_dataに改行と半角空白を除いたhtml_lineを付ける
      html_data += html_line.strip()
    # 「};」という文字列が入っていたらJSONデータ終わり
    if '};' in html_data:
      break;
  #  sys.exit()
  # "RsvApp.mapData"と"="と";"と半角スペースを削除
  html_data = html_data.replace("RsvApp.mapData = ", "")
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
  #      break
  return position_enables


##### 指定したポジションが空いているかチェック #####
def check_enable(position, position_enables):
  position_dict = position.split(':')
  # 指定したポジションが"enable"ならそのポジションを返す
  if (position_enables[int(position_dict[0])][int(position_dict[1])] == 'enable'):
    return position
  else:
    #ポジション配列が空の場合はキャンセル待ちを登録して終了
    if(len(position_enables)==0):
      sys.exit
    # ポジション配列を全てチェックして"enable"であったポジションを返す
    for y in range(0, len(position_enables)):
      for x in range(0, len(position_enables[y])):
        if (position_enables[y][x] == "enable"):
          position_new = str(y) + ':' + str(x)
          return (position_new)

  return position

##### キャンセル待ちを登録 #####
