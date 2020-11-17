# -*- coding: UTF-8 -*-
from aip import AipOcr
"""
准备工作

1.安装aip：pip install baidu-aip

2.到
https://ai.baidu.com/docs#/OCR-Python-SDK/top 使用说明
https://console.bce.baidu.com/?fromai=1#/aip/overview 控制台
https://console.bce.baidu.com/ai/#/ai/ocr/app 文字识别总览
https://console.bce.baidu.com/ai/创建文字识别应用，获取APP_ID、API_KEY、SECRET_KEY

参考文档
https://ai.baidu.com/docs#/OCR-Python-SDK/273a7560
"""
# 定义常量
APP_ID = '17490452'
API_KEY = 'ExSQLgk21aRx0857Kq3sbSGK'
SECRET_KEY = 'I2jpYzTBmHKXpHbYIwbsx9lcx1PzaGEt'

# 初始化AipFace对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def png_2_text(file):
    # 读取图片

    """ 读取图片 """
    def get_file_content(file):
        with open(file, 'rb') as fp:
            return fp.read()

    image = get_file_content(file)

    """ 调用通用文字识别, 图片参数为本地图片 """
    client.basicGeneral(image)

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    # 调用通用文字识别接口
    result = client.basicGeneral(get_file_content(file), options)
    #print(result)
    words_result = result['words_result']
    for i in range(len(words_result)):
        #print(words_result[i]['words'])
        return words_result[i]['words']
if __name__ == '__main__':
    png_2_text('login_code.png')