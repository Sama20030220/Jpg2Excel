import cv2
import requests
import base64


def save_excel(base64_str, filename='output.xlsx'):   # 将Base64编码的Excel内容解码并保存为Excel文件。
    decoded_data = base64.b64decode(base64_str)  # 解码Base64字符串为二进制数据
    with open(filename, 'wb') as f:
        f.write(decoded_data)
    # wb.save(filename) 由于出现了警告，大致意思是没有使用默认的格式，使用了这样的改正方法，但是出现无法写入数据的情况
    print(f"Excel文件已保存为：{filename}")


def cv_image_to_base64(cv_image):
    """将OpenCV图像转换为Base64编码"""
    is_success, buffer = cv2.imencode(".jpg", cv_image)
    if not is_success:
        raise ValueError("Failed to encode image.")
    return base64.b64encode(buffer).decode('utf-8')


def excel(img):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/table"
    # f = open('data/excel1.jpg', 'rb')
    # img = base64.b64encode(f.read())
    img = cv_image_to_base64(img)  # 使用新函数转换图像为Base64
    params = {"image": img, "return_excel": "true"}
    access_token = '24.03ee6d125539f1c34170b1a3703462f9.2592000.1722478007.282335-89934956'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        data = response.json()
        if data.get('tables_result') and isinstance(data['tables_result'], list) and data['tables_result']:  # 确保'tables_result'存在且为非空列表
            first_table = data['tables_result'][0]      # 定位到数据中的第一个表格信息
            if 'table_location' in first_table:
                boundaries = first_table['table_location']
            else:
                print("在第一个表格数据中未找到'table_location'。")
        else:
            print("未在响应中找到'tables_result'或其不是非空列表。")
        if 'excel_file' in data:
            base64_ima = data['excel_file']
            save_excel(base64_ima)
        else:
            print("Json中既没找到 'cell_location' 也未找到 'excel_file'。")
    else:
        print("服务器没响应")
    return boundaries
