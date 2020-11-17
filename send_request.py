#!usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
from  time import sleep
from tkinter import messagebox
from tkinter import Tk


"""
http://wellssm.com/newapi.html
"""


class SendRequest():

    def __init__(self):
        self.s = requests.session()
        self.login()
        sleep(5)
    def login(self):
        url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=signIn&uPhoneNo=15060359470&uPassword=linjianyu55'
        s4 = self.s.get(url=url)
        response = s4.text.strip('"')
        print(response)
        return response


    def get_phone(self):
        """
        获取手机号
        :param token:
        :return:
        """
        url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=getPhoneNo&projName=amazon&uPhoneNo=15060359470&uPassword=linjianyu55'
        s4 = self.s.get(url=url)
        response = s4.text.strip('"')
        return response

    def search(self):
        """
        获取手机号
        :param token:
        :return:
        """
        url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=getLeftNum&uPhoneNo=15060359470&uPassword=linjianyu55'
        s4 = self.s.get(url=url)
        response = s4.text.strip('"')
        return response

    def get_phone_msg(self,phone_num):
        """
        获取手机号验证码
        :param token:
        :return:
        """
        print('开始获取{}短信'.format(phone_num))
        url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=getMsg&uPhoneNo=15060359470&uPassword=linjianyu55&projName=amazon&phoneNo={phone}'.format(phone=phone_num)
        sleep(8)
        for i in range(20):
            s4 = requests.get(url=url)
            response = s4.text.strip()  # 响应正文
            print(response)
            if 'ERROR' not in response:
                code =  response.split('is')[1].strip()[:6]
                return code
            sleep(5)
        #一直没有收到短信就加黑名单
        print('超时没有收到短信，拉黑手机号，重新获取手机号')
        self.appde_Blacklist(phone_num)
        return False

    def appde_Blacklist(self,phone):
        """
        手机号假如黑名单
        :param token:
        :return:
        """
        url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=block&uPhoneNo=15060359470&uPassword=linjianyu55&uPhoneNo={phone}'.format(phone=phone)
        s4 = requests.get(url=url)
        response = s4.text.strip('"')
        print(response)
        return
    def login_out(self):
        """
        退出登录
        :param phone:
        :return:
        """
        url = 'http://api.xunyaosoft.com/zc/zhicode/api.php?code=signOut&uPhoneNo=15060359470&uPassword=linjianyu55'
        s4 = self.s.get(url=url)
        response = s4.text.strip('"')
        return response

    # def __del__(self):
    #     self.login_out()

if __name__ == '__main__':
    S = SendRequest()
    #phone = S.get_phone()
    phone = S.get_phone_msg('17075616679')
    print(phone)
    #msg = S.get_phone_msg(phone)