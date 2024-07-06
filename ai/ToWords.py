import requests
import base64


def in_it(words_xy, Excel_xy):  #   判断矩形rectangle是否完全被矩形container包含。
    words_xmin_ymax = {'x': min(p['x'] for p in words_xy), 'y': min(p['y'] for p in words_xy)}  # 提取矩形的左上角和右下角坐标
    words_xmax_ymin = {'x': max(p['x'] for p in words_xy), 'y': max(p['y'] for p in words_xy)}
    Excel_xmin_ymax = {'x': min(p['x'] for p in Excel_xy), 'y': min(p['y'] for p in Excel_xy)}
    Excel_xmax_ymin = {'x': max(p['x'] for p in Excel_xy), 'y': max(p['y'] for p in Excel_xy)}
    return not (words_xmin_ymax['x'] >= Excel_xmin_ymax['x'] and
                words_xmin_ymax['y'] >= Excel_xmin_ymax['y'] and
                words_xmax_ymin['x'] <= Excel_xmax_ymin['x'] and
                words_xmax_ymin['y'] <= Excel_xmax_ymin['y'])  # 判断是否包含


def Words(boundaries):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
    f = open('data/excel1.jpg', 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img, "recognize_granularity": "true", "vertexes_location": "true"}
    access_token = '24.03ee6d125539f1c34170b1a3703462f9.2592000.1722478007.282335-89934956'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        data = response.json()
        with open('output.txt', 'w') as txt_file:
            for item in data['words_result']:
                if in_it(item['min_finegrained_vertexes_location'], boundaries):
                    txt_file.write(item.get('words', '') + '\n')
