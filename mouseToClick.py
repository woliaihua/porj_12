# coding=utf-8
__author__ = 'pinsengjiujiezhong'
__date__ = '2019/8/31 11:38'
import aircv as ac
from pymouse import *
from PIL import ImageGrab
import win32api, win32con
from  time import sleep
import os

"""
需要安装的库
aircv 
opencv-python ：此库安装方法见lib下的opencv安装方法
pyscreenshot ：暂时未看懂为何要装此库
pymouse ：安装此库运行会提示缺少pyhook， 下载安装对应版本就行
pywin32 
Pillow 
"""

class CustomError(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo



class MouseToClick(object):
    # 截取整个屏幕
    @classmethod
    def screenshot(cls):
        filename = 'screen.png'
        im = ImageGrab.grab()
        im.save(filename)

    # 获取对应的图片的坐标点
    @classmethod
    def matchImg(cls,imgobj, imgsrc='screen.png', confidence=0.5):
        imsrc = ac.imread(imgsrc)
        imobj = ac.imread(imgobj)
        match_result = ac.find_template(imsrc,imobj,confidence)
        #print(match_result)
        os.remove(imgsrc)
        #match_result为None或不为None时满足自定义条件
        if not match_result or match_result and match_result['confidence']<0.8:
            raise CustomError(imgobj+'图片识别失败')
        else:
            x = match_result['result'][0]
            y = match_result['result'][1]
            #当前 x y 为识别图片的中心点，可以进行直接点击
            return x,y

    # 点击对应的鼠标
    @classmethod
    def click_img(cls, imgobj):
        sleep(0.3)
        MouseToClick.screenshot()
        sleep(0.15)
        x, y = MouseToClick.matchImg(imgobj)
        mouse = PyMouse()
        #print(int(x), int(y))
        mouse.click(int(x), int(y))

    # 输入单个键盘   enter等等
    @classmethod
    def oneKey(cls, key):
        keyboard = {'*': '106', '+': '107', '-': '109', '.': '110', '/': '111', 'F1': '112', 'F2': '113', 'F3': '114',
                    'F4': '115', 'F5': '116', 'F6': '117', 'F7': '118', 'F8': '119', 'F9': '120', 'F10': '121',
                    'F11': '122', 'F12': '123', 'A': '65', 'B': '66', 'C': '67', 'D': '68', 'E': '69', 'F': '70',
                    'G': '71', 'H': '72', 'I': '73', 'J': '74', 'K': '75', 'L': '76', 'M': '77', 'N': '78', 'O': '79',
                    'P': '80', 'Q': '81', 'R': '82', 'S': '83', 'T': '84', 'U': '85', 'V': '86', 'W': '87', 'X': '88',
                    'Y': '89', 'Z': '90', '0': '48', '1': '49', '2': '50', '3': '51', '4': '52', '5': '53', '6': '54',
                    '7': '55', '8': '56', '9': '57', 'BACKSPACE': '8', 'TAB': '9', 'CLEAR': '12', 'ENTER': '13',
                    'SHIFT': '16', 'CTRL': '17', 'ALT': '18', 'CAPSLOCK': '20', 'ESC': '27', 'SPACEBAR': '32',
                    'PAGEUP': '33', 'PAGEDOWN': '34', 'END': '35', 'LEFT': '37', 'UP': '38', 'HOME': '36',
                    'RIGHT': '39', 'DOWN': '40', 'INSERT': '45', 'DELETE': '46', 'HELP': '47', 'NUMLOCK': '144'}
        key = key.upper()
        win32api.keybd_event(int(keyboard[key]), 0, 0, 0)
        win32api.keybd_event(int(keyboard[key]), 0, win32con.KEYEVENTF_KEYUP, 0)

    # 输入两个键盘  ctrl+a等等
    @classmethod
    def twoKey(cls, keyone, keytwo):
        keyboard = {'*': '106', '+': '107', '-': '109', '.': '110', '/': '111', 'F1': '112', 'F2': '113', 'F3': '114',
                    'F4': '115', 'F5': '116', 'F6': '117', 'F7': '118', 'F8': '119', 'F9': '120', 'F10': '121',
                    'F11': '122', 'F12': '123', 'A': '65', 'B': '66', 'C': '67', 'D': '68', 'E': '69', 'F': '70',
                    'G': '71', 'H': '72', 'I': '73', 'J': '74', 'K': '75', 'L': '76', 'M': '77', 'N': '78', 'O': '79',
                    'P': '80', 'Q': '81', 'R': '82', 'S': '83', 'T': '84', 'U': '85', 'V': '86', 'W': '87', 'X': '88',
                    'Y': '89', 'Z': '90', '0': '48', '1': '49', '2': '50', '3': '51', '4': '52', '5': '53', '6': '54',
                    '7': '55', '8': '56', '9': '57', 'BACKSPACE': '8', 'TAB': '9', 'CLEAR': '12', 'ENTER': '13',
                    'SHIFT': '16', 'CTRL': '17', 'ALT': '18', 'CAPSLOCK': '20', 'ESC': '27',
                    'SPACEBAR': '32', 'PAGEUP': '33', 'PAGEDOWN': '34', 'END': '35', 'LEFT': '37', 'UP': '38',
                    'HOME': '36', 'RIGHT': '39', 'DOWN': '40', 'INSERT': '45', 'DELETE': '46', 'HELP': '47',
                    'NUMLOCK': '144'}
        keyone = keyone.upper()
        keytwo = keytwo.upper()
        win32api.keybd_event(int(keyboard[keyone]), 0, 0, 0)
        win32api.keybd_event(int(keyboard[keytwo]), 0, 0, 0)
        win32api.keybd_event(int(keyboard[keytwo]), 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(int(keyboard[keyone]), 0, win32con.KEYEVENTF_KEYUP, 0)
if __name__ == '__main__':
    MouseToClick.click_img('./img/email_setting.png')  # 点击邮箱设置