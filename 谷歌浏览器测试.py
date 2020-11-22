from helium import *
import configparser
import chardet
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from kill_prot import *
from send_request import SendRequest
from selenium.webdriver.support.ui import Select
from url_2_png import get_src_img
from img_2_text import png_2_text
from time import sleep
from helium import *
from get_template import *
from time import sleep
import configparser
from itertools import zip_longest
import chardet
from kill_prot import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from locale import atof, setlocale, LC_NUMERIC
from email_oper import *
from get_template import get_temp_dict
from send_request import SendRequest
from selenium.webdriver.support.ui import Select
from yanzhengqi_oper import get_make_code
import sys
from chick_proxy import servers_chick_ip
from del_txt_line import del_line  # 用一行删除一行
from selenium.webdriver import ActionChains  # 动作操作
import datetime
from xpath_to_png import GetPng
from chaojiying_Python.chaojiying import get_coordinate
from picture_recognition import PictureRecognition
from selenium.webdriver.common.keys import Keys
from random_str import *

"""
滑动图片验证
"""
import random


def get_file_code(filename):
    f3 = open(filename, 'rb')
    data = f3.read()
    encode = chardet.detect(data).get('encoding')
    f3.close()
    return encode


# path1 = os.path.dirname(os.path.abspath(__file__))  # 获取当前目录
path2 = 'config.ini'
encode = get_file_code(path2)
config = configparser.RawConfigParser()
config.read(path2, encoding=encode)
chrome_path = config.get('userinfo', "chrome_path")  # 0-12 如果是0 就表示不指定月份

port = 9022
# 关闭浏览器
# kill_pid(port)
# # 关闭进程
# cmd = r'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="C:\selenum\AutomationProfile{port}" --window-size=1080,800 '.format(chrome_path=chrome_path,port=port)  # --headless
# os.popen(cmd)
# 接管浏览器
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{port}".format(port=port))
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
script = '''
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})
'''
set_driver(driver)
Config.implicit_wait_secs =15 #设置隐式等待时间15秒
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
firse_name = personal_information_dict.get('First 名字')
last_name = personal_information_dict.get('last 姓')
email = email_dict.get('邮箱地址')
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


# if not CheckBox("is a beneficial owner of the business").is_checked():  # 复选框没有被选中
# click(CheckBox("is a beneficial owner of the business"))
# print(datetime.datetime.now())
# if not CheckBox("Don't require OTP on this browser").is_checked():
#     click(CheckBox("Don't require OTP on this browser"))
# write(temp_dict.get('银行卡号'), into=S('//*[@name="addCreditCardNumber"]'))
# click(S('//*[@id="formRegister:buttondoReg"]')) #图片7 确认
def check_img_exist(img_name):
    """
    检测当前页面是否有 图片 存在
    :param img_name:
    :return:
    """
    driver.save_screenshot('./img/screen_all.png')
    sleep(0.2)
    try:
        x, y = PictureRecognition.matchImg(img_name, './img/screen_all.png')
        return True
    except:
        return False


def chick_yanzhengma():
    """
    检查验证码是否正常通过
    :return:
    """
    for i in range(200):
        if i == 0:
            sleep(2.5)
        sleep(1)
        img_exist = check_img_exist('./img/ok.png')
        if img_exist:  # ok图片存在表示成功
            print('验证码通过')
            return
        if i == 99:
            print('超时，程序退出')
            sys.exit()


# click(S('//*[@id="cancelOTPLink"]/span'))  # 点击提交，但是提交后可能没货
# txt = S('//*[@id="container"]//img').web_element.get_attribute('src')
def save_txt(txt):
    """
    保存文本，用户名， 手机号，机器码
    :param txt:
    :return:
    """
    filename = './result/' + firse_name + last_name + '.txt'
    encod = 'utf-8'
    with open(filename, 'a', encoding=encod) as f:
        f.write(txt + '\n')

personal_information_filename = get_filename('.txt', '个人信息')
personal_information_dict = get_temp_dict(personal_information_filename)  # 个人信息
phone_filename = get_filename('.txt', '个人电话')
phone_dict = get_phone_dict(phone_filename)  # 个人电话
email_filename = get_filename('.txt', '个人邮箱')
email_dict = get_email_dict(email_filename)  # 邮箱
firse_name = personal_information_dict.get('First 名字')
last_name = personal_information_dict.get('last 姓')
email = email_dict.get('邮箱地址')
# write(personal_information_dict.get('SSN'), into=S('//*[@id="form:uiClaimant_ssn1to9"]'))
# write(personal_information_dict.get('SSN'), into=S('//*[@id="form:uiClaimant_confirmSsn1to9"]'))
# click(S('//*[@id="form:submitClaimantInfo"]'))#
# PIN = get_ranrom_pin(4)
# print("生成随机PIN:",PIN)
# write(PIN, into=S('//*[@id="form:uiClaimant_pin_new"]'))
# write(PIN, into=S('//*[@id="form:uiClaimant_pin_confirm"]'))
# save_txt("PIN:{}".format(PIN))
# mother_name = get_ranrom_name(7)
# print("生成随机Mother's Maiden Name:",mother_name)
# write('2020', into=S('//*[@id="UC1G01_F07_Year"]'))
# Select(S('//*[@id="UC1G01_F07_Day"]').web_element).select_by_visible_text('5')
# Select(S('//*[@id="UC1G01_F07_Month"]').web_element).select_by_visible_text('May')
# Select(S('//*[@id="UC1G01_F05"]').web_element).select_by_visible_text('0')
# write(mother_name, into=S('//*[@id="form:uiClaimant_maidenNameConf"]'))
# save_txt("Mother's Maiden Name:{}".format(mother_name))
# click(Link('Unemployment Services'))  # 点击 sign in
# click(S('//*[@id="form:submitNewPinMmn"]'))#点击登录
# wait_until(Text('File A Claim').exists, timeout_secs=2, interval_secs=0.4)
# click(S('//*[@id="UC1G01_F06"]')) #第二行单选选 no
# click(S('//*[@id="UC1G01_F2001"]')) #第4行单选选 yes
# click(S('//*[@id="UC1G01_F111"]')) #第5行单选选 yes
# click(S('//*[@id="UC1G01_F101"]')) #第6行单选选 yes
# click(S('//*[@id="UC1G01_F12"]')) #倒数第二行选no
def liucheng1():
    """
    第一二张：注册
    :return:
    """
    print('开始图片第1,2张流程')
    firse_name = personal_information_dict.get('First 名字')
    last_name = personal_information_dict.get('last 姓')
    email = email_dict.get('邮箱地址')
    driver.get('https://applications.labor.ny.gov/IndividualReg/xhtml/individual/emailVerification.faces')
    write(firse_name, into=S('//*[@id="userNameFirst"]'))  # firse name
    write(last_name, into=S('//*[@id="userNameLast"]'))  # last name
    write(email, into=S('//*[@id="userEmail"]'))  # E-mail Address
    write(email, into=S('//*[@id="userEmailConfirm"]'))  # Confirm E-mail Address
    click(S('//div[contains(@id,"j_id_jsp_")]/div/div/iframe'))  # 点击弹出验证码
    print('请输出验证码,450秒后超时')
    chick_yanzhengma()  # 开始检查验证码是否通过
    # click(Link('Contact Us'))  # 打开一个新的标签页面
    # switch_to(find_all(Window())[0])  # 切换到第0个窗口
    click(S('//*[@id="buttondoAddReg"]'))  # 点击continue
    save_txt('firse name: {}'.format(firse_name))
    save_txt('last_name: {}'.format(last_name))
    save_txt('email: {}'.format(email))


def liucheng2():
    """
    第三四张：激活邮箱
    :return:
    """
    print('开始图片第3,4张流程，激活邮箱')
    email_pwd = email_dict.get('邮箱密码')
    # switch_to(find_all(Window())[1])  # 打开第0个窗口
    driver.get("https://login.yahoo.com/")
    print('开始退出登录')
    driver.delete_all_cookies()
    driver.refresh()
    print('退出登录成功')
    try:
        print('点击邮箱登录')
        click(Link('Sign in'))
        print('点击邮箱登录完成')
        print('开始检测是否有Use another account字样，最长检测8秒')
        wait_until(Link('Use another account').exists, timeout_secs=8, interval_secs=0.4)
        print('发现Use another account,开始点击Use another account')
        click(Link('Use another account'))
        print('点击完成 ')
    except:
        write(email, into=S('//*[@id="login-username"]'))  # 输入邮箱地址
    write(email, into=S('//*[@id="login-username"]'))  # 输入邮箱地址
    click(S('//*[@id="login-signin"]'))  # 点击下一步
    write(email_pwd, into=S('//*[@id="login-passwd"]'))  # E-mail Address
    click(S('//*[@id="login-signin"]'))  # 点击下一步
    print('邮件登录操作完成')
    print('点击收件箱')
    click(S('//*[@id="ybarMailLink"]/span[1]'))  # 点击收件箱
    print('点击收件箱完成')
    try:
        click(S('//*[@title="Individual Account Creation for Online Services"]'))  # 点击第一封邮件
    except:
        print('暂时没有收到邮件.刷新页面重试')
        driver.refresh()
        click(S('//*[@title="Individual Account Creation for Online Services"]'))  # 点击第一封邮件
    save_txt('邮箱密码：{}'.format(email_pwd))
    try:
        click(Link('Click here to continue with the registration process.'))  # 点击激活链接
    except:
        try:
            print('激活链接点击失败，刷新页面重试')
            click(Text('Individual Account Creation for Online Services'))  # 点击第一封邮件
            click(Link('Click here to continue with the registration process.'))  # 点击激活链接
        except:
            print('没有收到邮件')

def liucheng3():
    """
    第五,5-2张图，激活邮件种输入详细信息
    :return:
    """
    print('开始图片第5,5-2张流程，激活邮件输入详细信息')
    try:
        write(firse_name, into=S('//*[@id="userNameFirst"]'))  # firse name
        write(last_name, into=S('//*[@id="userNameLast"]'))  # last name
        write(email, into=S('//*[@id="userEmail"]'))  # E-mail Address
    except:
        pass
    username = get_ranrom_str(12)
    print("生成随机用户名:", username)
    pwd = get_ranrom_str(16)
    print("生成随机密码:", pwd)
    write(username, into=S('//*[@id="userID"]'))  # 用户名
    write(pwd, into=S('//*[@id="userPassword"]'))  # 密码
    write(pwd, into=S('//*[@id="userPassword2"]'))  # 确认密码
    # 问题1
    Select(S('//*[@id="userSecret1Question"]').web_element).select_by_visible_text(
        'What was the name of my first pet?')  # 有效期 日
    Answer1 = get_ranrom_str(12)
    write(Answer1, into=S('//*[@id="userSecret1Answer"]'))
    write(Answer1, into=S('//*[@id="userSecret1AnswerConf"]'))
    # 问题2
    Select(S('//*[@id="userSecret2Question"]').web_element).select_by_visible_text(
        "What was my first grade teacher's last name?")  # 有效期 日
    Answer2 = get_ranrom_str(12)
    write(Answer2, into=S('//*[@id="userSecret2Answer"]'))
    write(Answer2, into=S('//*[@id="userSecret2AnswerConf"]'))
    # 问题3
    Select(S('//*[@id="userSecret3Question"]').web_element).select_by_visible_text(
        "What is the first name of my childhood best friend?")  # 有效期 日
    Answer3 = get_ranrom_str(12)
    write(Answer3, into=S('//*[@id="userSecret3Answer"]'))
    write(Answer3, into=S('//*[@id="userSecret3AnswerConf"]'))
    click(S('//*[@id="buttondoAddReg"]'))  # 点击继续
    save_txt('用户名：{}'.format(username))
    save_txt('密码：{}'.format(pwd))
    save_txt('问题1：{}'.format('What was the name of my first pet?'))
    save_txt('答案1：{}'.format(Answer1))
    save_txt('确认答案1：{}'.format(Answer1))
    save_txt('问题2：{}'.format("What was my first grade teacher's last name?"))
    save_txt('确认答案2：{}'.format(Answer2))
    save_txt('描述2：{}'.format(Answer2))
    save_txt('问题3：{}'.format('What is the first name of my childhood best friend?'))
    save_txt('确认答案3：{}'.format(Answer3))
    save_txt('描述3：{}'.format(Answer3))
def zhuce():
    liucheng1()
    liucheng2()
    liucheng3()
    liucheng4()

def liucheng4():
    """
    图片6,6-2,7 ,8填写生日 SSN ， 和确认提交
    :return:
    """
    global personal_information_filename
    global personal_information_dict
    global phone_filename
    global phone_dict
    global email_filename
    global email_dict
    global firse_name
    global last_name
    global email

    print('开始图片第6,6-2,7,8张流程，填写生日 SSN信息等')
    birth_date = personal_information_dict.get('生日')  # 1985/5/19
    birth_date = birth_date.split('/')
    if len(birth_date[1]) == 1:
        birth_date[1] = '0' + birth_date[1]
    str2 = birth_date[1] + '/' + birth_date[2] + '/' + birth_date[0]
    write(str2, into=S('//*[@id="formRegister:dob"]'))  # 生日
    save_txt('生日：{}'.format(str2))
    SSN = personal_information_dict.get('SSN')  # 1985/5/19
    write(SSN, into=S('//*[@id="formRegister:UIClaimant_social"]'))  # SSN
    save_txt('SSN：{}'.format(SSN))
    click(S('//*[@id="formRegister:buttondoAddReg"]'))  # 确认
    try:
        wait_until(Text('The SSN you provided is already in our records').exists, timeout_secs=5, interval_secs=0.4)
        print('SSN已被注册，跳过此行数据，从头开始注册')
        del_line(personal_information_dict.get('驾照号'), personal_information_filename)  # 删除个人信息
        sleep(0.15)

        personal_information_filename = get_filename('.txt', '个人信息')
        personal_information_dict = get_temp_dict(personal_information_filename)  # 个人信息
        phone_filename = get_filename('.txt', '个人电话')
        phone_dict = get_phone_dict(phone_filename)  # 个人电话
        email_filename = get_filename('.txt', '个人邮箱')
        email_dict = get_email_dict(email_filename)  # 邮箱
        firse_name = personal_information_dict.get('First 名字')
        last_name = personal_information_dict.get('last 姓')
        email = email_dict.get('邮箱地址')
        zhuce()
    except:
        pass


def liucheng5():
    """
    图片9，10
    :return:
    """
    print('开始图片第9,10张流程')
    driver.get('https://www.labor.ny.gov/signin')
    click(S('//*[@id="signInButton"]'))  # 点击 sign in
    try:
        write('C8GPHmvEx0UT', into=S('//*[@id="loginform:username"]'))  # 用户名
        write('fFu0XhrkcsnMfXIR', into=S('//*[@id="loginform:password"]'))  # 密码
    except:
        print('已被登录，开始退出登录后重新登录')
        click(S('//*[@id="CommonNavSignoutLinktxt2"]'))  # 需要退出登录
        try:
            wait_until(S('//*[@id="CommonNavSignoutLinktxt2"]').exists, timeout_secs=10,
                       interval_secs=0.4)  # 没有退出登录成功
            click(S('//*[@id="CommonNavSignoutLinktxt2"]'))  # 需要退出登录
        except:
            pass
        try:
            wait_until(S('//*[@id="signInButton"]').exists, timeout_secs=30, interval_secs=0.4)  # sign in存在
            click(S('//*[@id="signInButton"]'))  # 点击 sign in
            sleep(1)
        except Exception as e:
            pass
            check_img_exist('/img/login.png')
        print('开始输入用户名密码')
        write('C8GPHmvEx0UT', into=S('//*[@id="loginform:username"]'))  # 用户名
        write('fFu0XhrkcsnMfXIR', into=S('//*[@id="loginform:password"]'))  # 密码
    print("请手动输入验证码,400秒后超时")
    chick_yanzhengma()
    click(S('//*[@id="loginform:signinButton"]'))  # 点击登录


def liucheng6():
    """
    图片12，13
    :return:
    """
    print('开始图片第12,13张流程')
    wait_until(Link('Unemployment Services').exists, timeout_secs=40, interval_secs=0.4)
    click(Link('Unemployment Services'))  # 点击Unemployment Services
    write(personal_information_dict.get('SSN'), into=S('//*[@id="form:uiClaimant_ssn1to9"]'))
    write(personal_information_dict.get('SSN'), into=S('//*[@id="form:uiClaimant_confirmSsn1to9"]'))
    click(S('//*[@id="form:submitClaimantInfo"]'))  # 点击提交


def liucheng7():
    """
    图片14
    :return:
    """
    print('开始图片第14张流程')
    PIN = get_ranrom_pin(4)
    print("生成随机PIN:", PIN)
    write(PIN, into=S('//*[@id="form:uiClaimant_pin_new"]'))
    write(PIN, into=S('//*[@id="form:uiClaimant_pin_confirm"]'))
    save_txt("PIN:{}".format(PIN))
    mother_name = get_ranrom_name(7)
    print("生成随机Mother's Maiden Name:", mother_name)
    write(mother_name, into=S('//*[@id="form:uiClaimant_maidenName"]'))
    write(mother_name, into=S('//*[@id="form:uiClaimant_maidenNameConf"]'))
    save_txt("Mother's Maiden Name:{}".format(mother_name))
    click(S('//*[@id="form:submitNewPinMmn"]'))  # 点击提交
    print('请手动识别验证码，400秒后超时')


def liucheng8():
    """
    图片14，15，16
    :return:
    """
    print('开始图片第14,15,16张流程')
    try:
        wait_until(Text('File A Claim').exists, timeout_secs=400, interval_secs=0.4)
        print('识别成功')
        click(S('//*[@id="content"]/form[1]/input[5]'))  # 点击File A Claim
    except:
        print('或许图片识别超时')
    click(S('//*[@id="content"]/form/center/input'))  # 点击继续
    click(S('//*[@name="button" and @value="I Agree"]'))  # 点击同意


def liucheng9():
    """
    图片18
    :return:
    """
    print('开始图片第18张流程')
    Select(S('//*[@id="UC1G01_F05"]').web_element).select_by_visible_text('0')
    click(S('//*[@id="UC1G01_F06"]'))  # 第二行单选选 no
    write('2020', into=S('//*[@id="UC1G01_F07_Year"]'))
    Select(S('//*[@id="UC1G01_F07_Day"]').web_element).select_by_visible_text('5')
    Select(S('//*[@id="UC1G01_F07_Month"]').web_element).select_by_visible_text('May')
    click(S('//*[@id="UC1G01_F2001"]'))  # 第4行单选选 yes
    click(S('//*[@id="UC1G01_F111"]'))  # 第5行单选选 yes
    click(S('//*[@id="UC1G01_F101"]'))  # 第6行单选选 yes
    click(S('//*[@id="UC1G01_F12"]'))  # 倒数第二行选no
    click(S('//*[@id="UC1G01_F13"]'))  # 倒数第一行选no
    click(S('//input[@value="Continue"]'))  # 点击提交


def liucheng10():
    """
    图片19,19-2
    :return:
    """
    print('开始图片19,19-2流程')
    write(personal_information_dict.get('驾照号'), into=S('//*[@id="UC1G04_F08"]'))
    save_txt("驾照号:{}".format(personal_information_dict.get('驾照号')))
    Select(S('//*[@id="UC1G04_F09"]').web_element).select_by_visible_text('One employer')
    click(S('//input[@value="Continue"]'))  # 点击提交


def liucheng11():
    """
    图片20
    :return:
    """
    print('开始图片20流程')
    click(S('//*[@id="UC1G07_F011"]'))  # 第1行单选选 yes
    click(S('//*[@id="UC1G07_F02"]'))  # 第3行单选选 no
    click(S('//*[@id="UC1G07_F03"]'))  # 第6行单选选 no
    click(S('//*[@id="UC1G07_F04"]'))  # 第7行单选选 no
    click(S('//*[@id="UC1G07_F05"]'))  # 倒数第二行选no
    click(S('//*[@id="UC1G07_F06"]'))  # 倒数第一行选no
    click(S('//input[@value="Continue"]'))  # 点击提交


def liucheng12():
    """
    图片21,22
    :return:
    """
    print('开始图片第21,22张流程')
    click(S('//*[@id="UC1G08_F071"]'))  # 第1行单选选 yes
    click(S('//*[@id="UC1G08_F08"]'))  # 第3行单选选 no
    click(S('//*[@id="UC1G08_F08_B0"]'))  # 第6行单选选 no
    click(S('//*[@id="UC1G08_F09"]'))  # 第7行单选选 no
    click(S('//*[@id="UC1G08_F10"]'))  # 倒数第二行选no
    click(S('//*[@id="UC1G08_F11"]'))  # 倒数第一行选no
    click(S('//*[@id="UC1G08_F12"]'))  # 倒数第一行选no
    click(S('//*[@id="UC1G08_F13"]'))  # 倒数第一行选no
    click(S('//*[@id="UC1G08_F14"]'))  # 倒数第一行选no
    click(S('//input[@value="Continue"]'))  # 点击提交


def liucheng13():
    """
    图片24
    :return:
    """
    print('开始图片第24张流程')
    try:
        click(S('//*[@id="id"]'))
        wait_until(Text('Federal Employer Identification Number (FEIN)').exists, timeout_secs=5, interval_secs=0.4)
        click(S('//input[@value="Continue"]'))  # 点击提交
    except:
        print('请手动操作到流程第6步')
    title = driver.title
    for i in range(2000):
        sleep(1)
        if title == 'Most Recent Employer Information, Part 2':
            break
    wait_until(S('//*[@id="UC1G10_F01"]').exists, timeout_secs=1000, interval_secs=0.4)
    write(personal_information_dict.get('公司名字'), into=S('//*[@id="UC1G10_F01"]'))  # 公司名字
    write(personal_information_dict.get('公司地址'), into=S('//*[@id="UC1G10_F02"]'))  # 公地址
    write(personal_information_dict.get('公司市'), into=S('//*[@id="UC1G10_F04"]'))  # 公地市
    write(personal_information_dict.get('公司电话')[0:3], into=S('//*[@id="UC1G10_F08P1"]'))
    write(personal_information_dict.get('公司电话')[3:6], into=S('//*[@id="UC1G10_F08P2"]'))
    write(personal_information_dict.get('公司电话')[6:], into=S('//*[@id="UC1G10_F08P3"]'))
    write(personal_information_dict.get('公司邮编'), into=S('//*[@id="UC1G10_F06"]'))
    click(S('//*[@id="UC1G10_F13L"]'))  # 倒数第一行选no
    write('2018', into=S('//*[@id="UC1G10_F09_Year"]'))
    str1 = '123456789'
    Select(S('//*[@id="UC1G10_F09_Day"]').web_element).select_by_visible_text(random.choice(str1))
    str1 = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September']
    Select(S('//*[@id="UC1G10_F09_Month"]').web_element).select_by_visible_text(random.choice(str1))
    Select(S('//*[@id="UC1G10_F05"]').web_element).select_by_visible_text('New York')

    write('customer service', into=S('//*[@id="UC1G10_F17"]'))  # What wUC1G10_F01as your job title?
    write('office', into=S('//*[@id="UC1G10_F19"]'))  # What was your job location or job site?
    Select(S('//*[@id="UC1G10_F18"]').web_element).select_by_visible_text('Business and Financial')
    click(S('//input[@value="Continue"]'))  # 点击提交
    save_txt("公司名字:{}".format(personal_information_dict.get('公司名字')))
    save_txt("公司地址:{}".format(personal_information_dict.get('公司地址')))
    save_txt("公司市:{}".format(personal_information_dict.get('公司市')))
    save_txt("公司电话:{}".format(personal_information_dict.get('公司电话')))
    save_txt("公司邮编:{}".format(personal_information_dict.get('公司邮编')))


def liucheng14():
    """
    图片25
    :return:
    """
    print('开始图片25张流程')
    print('开始寻找包含Food的单选按钮')
    click(S('//*[@id="content"]//td[contains(text(),"Food")]/..//input'))  # 第1行单选选 yes
    print('寻找并点击成功')
    click(S('//td[@colspan="3"]//input[@value="Continue"]'))  # 点击提交


def liucheng15():
    """
    图片26,26-2
    :return:
    """
    print('开始图片第26,26-2张流程')
    click(S('//*[@id="UC1G05_F15"]'))  # 第1行单选选 no
    write(personal_information_dict.get('个人地址'), into=S('//*[@id="UC1G05_F03"]'))
    write(personal_information_dict.get('个人市'), into=S('//*[@id="UC1G05_F05"]'))
    Select(S('//*[@id="UC1G05_F06"]').web_element).select_by_visible_text('New York')
    Select(S('//*[@id="UC1G05_F38"]').web_element).select_by_visible_text('Four-year degree program')
    write(personal_information_dict.get('个人邮编'), into=S('//*[@id="UC1G05_F07"]'))
    write(phone_dict.get('电话')[0:3], into=S('//*[@id="UC1G05_F34P1"]'))
    write(phone_dict.get('电话')[3:6], into=S('//*[@id="UC1G05_F34P2"]'))
    write(phone_dict.get('电话')[6:], into=S('//*[@id="UC1G05_F34P3"]'))
    click(S('//*[@id="<%= IUC1G05_UIKeys.UI_UC1G05_Gender%>0"]'))  # Male
    click(S('//*[@id="UC1G05_F40"]'))  # Are you a veteran?
    click(S('//*[@id="UC1G05_F411"]'))  # Are you a citizen of the U.S?
    click(S('//*[@id="UC1G05_F42"]'))  #
    click(S('//*[@id="UC1G05_F44"]'))  #
    click(S('//*[@id="UC1G05_F43"]'))  #
    click(S('//*[@id="UC1G05_F45"]'))  #
    Select(S('//*[@id="UC1G05_F36"]').web_element).select_by_visible_text('Do not wish to answer')
    Select(S('//*[@id="UC1G05_F37"]').web_element).select_by_visible_text('Do not wish to answer')
    Select(S('//*[@id="UC1G05_F39"]').web_element).select_by_visible_text('No')
    Select(S('//*[@id="UC1G05_F210"]').web_element).select_by_visible_text('English')
    click(S('//input[@value="Continue"]'))  # 点击提交

    save_txt("个人电话:{}".format(phone_dict.get('电话')))
    save_txt("个人地址:{}".format(personal_information_dict.get('个人地址')))
    save_txt("个人市:{}".format(personal_information_dict.get('个人市')))
    save_txt("个人邮编:{}".format(personal_information_dict.get('个人邮编')))
    
def liucheng16():
    """
    图片27,28
    :return:
    """
    print('开始图片第27,28张流程')
    click(S('//form[@name="addrNormForm"]/input[@value="Use this address"]'))
    Select(S('//*[@id="DirectDeposit_PaymentOption"]').web_element).select_by_visible_text('Direct Deposit')
    click(S('//input[@value="Continue"]'))  # 点击提交
    print('流程完成，开始清理已使用的信息')
    del_line(personal_information_dict.get('驾照号'), personal_information_filename)#删除个人信息
    print('删除使用过的个人信息完成')
    del_line(email_dict.get('邮箱地址'), email_filename)#删除个人邮箱
    print('删除使用过的个人邮箱完成')
    del_line(phone_dict.get('电话'), phone_filename)#删除个人电话
    print('删除使用过的个人电话完成')
    print('剩余流程请手动完成，完成后重启软件')
    write('123', into=S('//*[@id="DirectDeposit_MothersMaidenName"]'))
wait_until(Text('Your NY GOV Username is:').exists, timeout_secs=5, interval_secs=0.4)
# liucheng1()
# liucheng2()
# liucheng3()
# liucheng4()
# liucheng5()
# liucheng6()
# liucheng7()
# liucheng8()
# liucheng9()
# liucheng10()
# liucheng11()
# liucheng12()
# liucheng13()
# liucheng14()
#liucheng15()
# liucheng16()

    # wait_until(Text('Federal Employer Identification Number (FEIN)').exists, timeout_secs=400, interval_secs=0.4)
    # wait_until(S('//*[@id="CommonNavSignoutLinktxt2"]').exists, timeout_secs=2, interval_secs=0.4)  # 需要退出登录
