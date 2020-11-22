#! /usr/bin/python
# -*- coding: utf-8 -*-
from helium import *
from itertools import zip_longest
from kill_prot import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from locale import atof,setlocale,LC_NUMERIC
from email_oper import *
from get_template import *
from send_request import SendRequest
from selenium.webdriver.support.ui import Select
from yanzhengqi_oper import get_make_code
from base64_to_img import to_png
from chick_proxy import servers_chick_ip
from del_txt_line import del_line#用一行删除一行
from url_2_png import get_src_img
from email_oper import get_url
from xpath_to_png import GetPng
from chaojiying_Python.chaojiying import get_coordinate
from selenium.webdriver import ActionChains #动作操作
from picture_recognition import PictureRecognition
from random_str import get_ranrom_str
import sys

email_filename = get_filename('.txt', '个人邮箱')
email_dict = get_email_dict(email_filename)  # 邮箱
email_pwd = email_dict.get('邮箱密码')


str1 = ['January','February','March','April','May','June','July','August','September']
import random
print(random.choice(str1))