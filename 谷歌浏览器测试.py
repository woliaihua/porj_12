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
from base64_to_img import to_png
from chick_proxy import servers_chick_ip
from del_txt_line import del_line#用一行删除一行
from url_2_png import get_src_img
import datetime
"""
滑动图片验证
"""
from get_template import get_temp_dict,get_filename
temp_filename = get_filename('.txt', 'template')
temp_dict = get_temp_dict(temp_filename)  # 模板
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
# driver.get('https://sellercentral.amazon.co.uk/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fsellercentral.amazon.co.uk%2Fhome&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=sc_uk_amazon_v2&openid.mode=checkid_setup&language=zh_CN&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=sc_uk_amazon_v2&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ssoResponse=eyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.a5mUI1lQr80X3ikb1RfOscCl9fzyVVqmwXRr7HiL8LvGu6_LPzJA3w.T45gQk4uPvjQ7NW0.Na-asGEBLFxeUQFlqMQgwJNXHMC74exdYEpDoxF-LZ9sURBQONC_tTvjCK5Rsr781XOY-SMbZMSmm3q4UhtKJKJVN3tYK-vsOlfm01WkIwsztXXVAtPK50U3GNL1TdWt83BC2gUPzCVvkSVunLWRqUtS3yqesp5rCOyBl4SKfhHTQs2581J8-15xVwQ7LiN1vVYU_tMMJWMimFq2SITB6lvXS9cm8Hs8Rv81scAwDMJUtyHMddsgLnOSZ3wRbY_YmVcS.IwaDHOGL2wtpgIvB_we95A')
# write('854639',into=S('//*[@name="verifyOTPButton"]'))
# write('+86 18040377309',into=S('//*[@id="country-phone-input"]'))
# click(S('//*[@id="go"]'))
print(driver.title)
click(S('//*[@id="ExistingAddress"]/div[1]/div/div/div/div/label/input'))
#wait_until(Text('我们找不到具有该电子邮件地址的账户').exists, timeout_secs=1, interval_secs=0.4)  # 需要安全验证
#write('kejv0059',into=S('//*[@id="ap_password"]'))
#wait_until(S('//*[@id="auth-captcha-refresh-link" and @style="display: inline;"]').exists, timeout_secs=10, interval_secs=0.4)  ## 是否没货
print(datetime.datetime.now())
#if not CheckBox("is a beneficial owner of the business").is_checked():  # 复选框没有被选中
# click(CheckBox("is a beneficial owner of the business"))
# print(datetime.datetime.now())
# if not CheckBox("Don't require OTP on this browser").is_checked():
#     click(CheckBox("Don't require OTP on this browser"))
# write(temp_dict.get('银行卡号'), into=S('//*[@name="addCreditCardNumber"]'))
# Select(S('//*[@name="ccExpirationMonth" and not(@disabled)]').web_element).select_by_visible_text(temp_dict.get('到期日'))#有效期 日
# Select(S('//*[@name="ccExpirationYear" and not(@disabled)]').web_element).select_by_visible_text(temp_dict.get('到期年'))#有效期 日
# write(temp_dict.get('英文姓')+temp_dict.get('英文名'), into=S('//*[@name="ccHolderName"]'))

#click(S('//*[@id="cancelOTPLink"]/span'))  # 点击提交，但是提交后可能没货
# txt = S('//*[@id="container"]//img').web_element.get_attribute('src')
wait_until(S('//input[@name="pincode"]').exists, timeout_secs=20, interval_secs=0.4)  ## 是否有邮编输入框
write(temp_dict.get('邮编'),into=S('//input[@name="pincode"]'))
write(temp_dict.get('街道地址'),into=S('//input[@name="address_line1"]'))
write(temp_dict.get('城市'), into=S('//input[@name="city"]'))
write(temp_dict.get('省'), into=S('//input[@name="state"]'))
#获取电话号码
SR = SendRequest()
phone = SR.get_phone()
print('获取到的手机号是{}'.format(phone))
write('+86 {}'.format(phone), into=S('//*[@name="phoneno"]'))
write(temp_dict.get('英文名'),into=S('//input[@name="firstName"]'))
write(temp_dict.get('英文姓'),into=S('//input[@name="lastName"]'))
write(temp_dict.get('统一社会信用代码'), into=S('//input[@name="businessLicenseNumber"]'))
# click(S('//*[@name="Submit"]'))  # 点击保存并继续

#liucheng4()
#wait_until(Text('验证码输入有误，请重新输入').exists, timeout_secs=2, interval_secs=0.4)  # 需要安全验证