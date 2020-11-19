from helium import *
import configparser
import chardet
from selenium.webdriver.chrome.options import Options
from  selenium import webdriver
from kill_prot import *
from send_request import SendRequest
from selenium.webdriver.support.ui import Select
from url_2_png import get_src_img
from img_2_text import png_2_text
from  time import sleep
from helium import *
from get_template import *
from time import  sleep
import configparser
from itertools import zip_longest
import chardet
from kill_prot import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from locale import atof,setlocale,LC_NUMERIC
from email_oper import *
from get_template import get_temp_dict
from send_request import SendRequest
from selenium.webdriver.support.ui import Select
from yanzhengqi_oper import get_make_code
import sys
from chick_proxy import servers_chick_ip
from del_txt_line import del_line#用一行删除一行
from selenium.webdriver import ActionChains #动作操作
import datetime
from xpath_to_png import GetPng
from chaojiying_Python.chaojiying import get_coordinate
from picture_recognition import PictureRecognition
from selenium.webdriver.common.keys import Keys
from random_str import get_ranrom_str
"""
滑动图片验证
"""

def get_file_code(filename):
    f3 = open(filename, 'rb')
    data = f3.read()
    encode = chardet.detect(data).get('encoding')
    f3.close()
    return encode

#path1 = os.path.dirname(os.path.abspath(__file__))  # 获取当前目录
path2 ='config.ini'
encode = get_file_code(path2)
config = configparser.RawConfigParser()
config.read(path2, encoding=encode)
chrome_path = config.get('userinfo', "chrome_path")  # 0-12 如果是0 就表示不指定月份

port =9022
#关闭浏览器
# kill_pid(port)
# # 关闭进程
# cmd = r'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="C:\selenum\AutomationProfile{port}" --window-size=1080,800 '.format(chrome_path=chrome_path,port=port)  # --headless
# os.popen(cmd)
#接管浏览器
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{port}".format(port=port))
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options =chrome_options)
script = '''
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})
'''
set_driver(driver)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
# driver.get('https://applications.labor.ny.gov/IndividualReg/xhtml/individual/emailVerification.faces')
# write('854639',into=S('//*[@name="verifyOTPButton"]'))
# write('+86 18040377309',into=S('//*[@id="country-phone-input"]'))
# click(S('//*[@id="go"]'))
print(driver.title)


# def check_img_exist( img_name):
#     driver.save_screenshot('./img/screen_all.png')
#     sleep(0.2)
#     try:
#         x, y = PictureRecognition.matchImg(img_name, './img/screen_all.png')
#         return True
#     except:
#         return False
#
personal_information_filename = get_filename('.txt', '个人信息')
personal_information_dict = get_temp_dict(personal_information_filename)  # 个人信息
phone_filename = get_filename('.txt', '个人电话')
phone_dict = get_phone_dict(phone_filename)  # 个人电话
email_filename = get_filename('.txt', '个人邮箱')
email_dict = get_email_dict(email_filename)  # 邮箱
# driver.get('https://applications.labor.ny.gov/IndividualReg/xhtml/individual/emailVerification.faces')
# write(personal_information_dict.get('First 名字'), into=S('//*[@id="userNameFirst"]'))  # firse name
# write(personal_information_dict.get('last 姓'), into=S('//*[@id="userNameLast"]'))  # last name
# write(email_dict.get('邮箱地址'), into=S('//*[@id="userEmail"]'))  # E-mail Address
# write(email_dict.get('邮箱地址'), into=S('//*[@id="userEmailConfirm"]'))  # Confirm E-mail Address
# click(S('//div[contains(@id,"j_id_jsp_")]/div/div/iframe')) #点击弹出验证码
# print('请输出验证码')
# for i in range(100):
#     sleep(1)
#     img_exist = check_img_exist('./img/ok.png')
#     if img_exist:#ok图片存在表示成功
#         break
#     else:
#         print('循环检测验证码是否验证成功种...')
#     if i == 99:
#         print('超时，程序退出')
#         sys.exit()
#
# print("生成随机用户名:",username)
# pwd = get_ranrom_str(16)
# print("生成随机密码:",username)
# write(username, into=S('//*[@id="userID"]'))  #  用户名
# write(pwd, into=S('//*[@id="userPassword"]'))  # 密码
# write(pwd, into=S('//*[@id="userPassword2"]'))  # 确认密码
#
# write('123', into=S('//*[@id="userEmailConfirm"] '))  # Confirm E-mail Address
# wait_until(S('//*[@id="auth-captcha-refresh-link" and @style="display: inline;"]').exists, timeout_secs=2, interval_secs=0.4)  ## 是否没货
print(datetime.datetime.now())
#if not CheckBox("is a beneficial owner of the business").is_checked():  # 复选框没有被选中
# click(CheckBox("is a beneficial owner of the business"))
# print(datetime.datetime.now())
# if not CheckBox("Don't require OTP on this browser").is_checked():
#     click(CheckBox("Don't require OTP on this browser"))
# write(temp_dict.get('银行卡号'), into=S('//*[@name="addCreditCardNumber"]'))
Select(S('//*[@id="userSecret1Question"]').web_element).select_by_visible_text('What was the name of my first pet?')#有效期 日
# Select(S('//*[@name="ccExpirationYear" and not(@disabled)]').web_element).select_by_visible_text(temp_dict.get('到期年'))#有效期 日
userSecret1Answer = get_ranrom_str(12)
write(userSecret1Answer, into=S('//*[@id="userSecret1Answer"]'))

#click(S('//*[@id="cancelOTPLink"]/span'))  # 点击提交，但是提交后可能没货
# txt = S('//*[@id="container"]//img').web_element.get_attribute('src')

# click(S('//*[@name="Submit"]'))  # 点击保存并继续

#liucheng4()
#wait_until(Text('验证码输入有误，请重新输入').exists, timeout_secs=2, interval_secs=0.4)  # 需要安全验证