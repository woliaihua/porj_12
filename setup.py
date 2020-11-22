#coding=utf-8

from helium import *
from kill_prot import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from locale import atof,setlocale,LC_NUMERIC
from email_oper import *
from get_template import *
from selenium.webdriver.support.ui import Select
from del_txt_line import del_line#用一行删除一行
from xpath_to_png import GetPng
from chaojiying_Python.chaojiying import get_coordinate
from selenium.webdriver import ActionChains #动作操作
from picture_recognition import PictureRecognition
from random_str import *
import sys
import random

setlocale(LC_NUMERIC, 'English_US')

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
yanzhengqi_path = config.get('userinfo', "yanzhengqi_path")  # 0-12 如果是0 就表示不指定月份
email_exe_path = config.get('userinfo', "email_exe_path")  # 0-12 如果是0 就表示不指定月份


class BaseStartChome():
    """
    反爬模式启动浏览器
    """

    def __init__(self,port):
        self.information_init()
        #kill_pid(port)
        kill_all_chorme()
        sleep(3)
        # 关闭进程
        self.cmd = r'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="C:\selenum\AutomationProfile{port}" --window-size=1080,800 '.format(chrome_path=chrome_path,port=port)  # --headless
        #加代理ip，#标记要修改
        # self.cmd = r'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="C:\selenum\AutomationProfile{port}" --window-size=1080,800 --proxy-server=http://{ip}'.format(
        #     chrome_path=chrome_path, port=port, ip=ip)  # --headless
        os.popen(self.cmd)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{port}".format(port=port))
        self.driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
        script = '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''
        set_driver(self.driver)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        Config.implicit_wait_secs =15 #设置隐式等待时间15秒

    def information_init(self):
        """
        一些异常情况需要重头开实执行，重新初始化
        :return:
        """
        self.personal_information_filename = get_filename('.txt', '个人信息')
        self.personal_information_dict = get_temp_dict(self.personal_information_filename)  # 个人信息
        self.phone_filename = get_filename('.txt', '个人电话')
        self.phone_dict = get_phone_dict(self.phone_filename)  # 个人电话
        self.email_filename = get_filename('.txt', '个人邮箱')
        self.email_dict = get_email_dict(self.email_filename)  # 邮箱

    def login_out(self):
        self.driver.delete_all_cookies()
        self.driver.refresh()

    def chick_login(self):
        """
        只有冻结账号，错误密码账号，还有登录需要手机令牌的账号。这3种就直接跳过账号登录下一个
        :return:
        """
        sleep(2)
        title = self.driver.title
        if '登录' in title:
            try:
                pass
            except:
                pass
    def chick_yanzhengma(self):
        """
        检查验证码是否正常通过
        :return:
        """
        for i in range(400):
            if i == 0:
                sleep(2.5)
            sleep(1)
            img_exist = self.check_img_exist('./img/ok.png')
            if img_exist:#ok图片存在表示成功
                print('验证码通过')
                return
            if i == 99:
                print('超时，程序退出')
                sys.exit()

    def zhuce(self):
        self.liucheng1()
        self.liucheng2()
        self.liucheng3()
        self.liucheng4()

    def liucheng1(self):
        """
        第一二张：注册
        :return:
        """
        print('开始图片第1,2张流程')
        self.firse_name = self.personal_information_dict.get('First 名字')
        self.last_name = self.personal_information_dict.get('last 姓')
        self.email = self.email_dict.get('邮箱地址')
        self.driver.get('https://applications.labor.ny.gov/IndividualReg/xhtml/individual/emailVerification.faces')
        write(self.firse_name, into=S('//*[@id="userNameFirst"]'))  # firse name
        write(self.last_name, into=S('//*[@id="userNameLast"]'))  # last name
        write(self.email, into=S('//*[@id="userEmail"]'))  # E-mail Address
        write(self.email, into=S('//*[@id="userEmailConfirm"]'))  # Confirm E-mail Address
        click(S('//div[contains(@id,"j_id_jsp_")]/div/div/iframe')) #点击弹出验证码
        print('请输出验证码,450秒后超时')
        self.chick_yanzhengma()#开始检查验证码是否通过
        # click(Link('Contact Us'))  # 打开一个新的标签页面
        # switch_to(find_all(Window())[0])  # 切换到第0个窗口
        click(S('//*[@id="buttondoAddReg"]'))  # 点击continue
        self.save_txt('firse name: {}'.format(self.firse_name))
        self.save_txt('last_name: {}'.format(self.last_name))
        self.save_txt('email: {}'.format(self.email))

    def liucheng2(self):
        """
        第三四张：激活邮箱
        :return:
        """
        print('开始图片第3,4张流程，激活邮箱')
        email_pwd = self.email_dict.get('邮箱密码')
        # switch_to(find_all(Window())[1])  # 打开第0个窗口
        self.driver.get("https://login.yahoo.com/")
        print('开始退出登录')
        self.driver.delete_all_cookies()
        self.driver.refresh()
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
            write(self.email, into=S('//*[@id="login-username"]'))  # 输入邮箱地址
        write(self.email, into=S('//*[@id="login-username"]'))  # 输入邮箱地址
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
            self.driver.refresh()
            try:
                click(S('//*[@title="Individual Account Creation for Online Services"]'))  # 点击第一封邮件
            except:
                click(S('//*[@id="ybarMailLink"]/span[1]'))  # 点击收件箱
                click(S('//*[@title="Individual Account Creation for Online Services"]'))  # 点击第一封邮件
        self.save_txt('邮箱密码：{}'.format(email_pwd))
        try:
            click(Link('Click here to continue with the registration process.'))  # 点击激活链接
        except:
            try:
                print('激活链接点击失败，刷新页面重试')
                click(Text('Individual Account Creation for Online Services'))  # 点击第一封邮件
                click(Link('Click here to continue with the registration process.'))  # 点击激活链接
            except:
                print('没有收到邮件')

    def liucheng3(self):
        """
        第五,5-2张图，激活邮件种输入详细信息
        :return:
        """
        print('开始图片第5,5-2张流程，激活邮件输入详细信息')
        try:
            write(self.firse_name, into=S('//*[@id="userNameFirst"]'))  # firse name
            write(self.last_name, into=S('//*[@id="userNameLast"]'))  # last name
            write(self.email, into=S('//*[@id="userEmail"]'))  # E-mail Address
        except:
            pass
        self.username = get_ranrom_str(12)
        print("生成随机用户名:", self.username)
        self.pwd = get_ranrom_str(16)
        print("生成随机密码:", self.pwd)
        write(self.username, into=S('//*[@id="userID"]'))  # 用户名
        write(self.pwd, into=S('//*[@id="userPassword"]'))  # 密码
        write(self.pwd, into=S('//*[@id="userPassword2"]'))  # 确认密码
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
        click(S('//*[@id="buttondoAddReg"]'))#点击继续

        print('开始写入数据')
        self.save_txt('用户名：{}'.format(self.username))
        self.save_txt('密码：{}'.format(self.pwd))
        self.save_txt('问题1：{}'.format('What was the name of my first pet?'))
        self.save_txt('答案1：{}'.format(Answer1))
        self.save_txt('确认答案1：{}'.format(Answer1))
        self.save_txt('问题2：{}'.format("What was my first grade teacher's last name?"))
        self.save_txt('答案2：{}'.format(Answer2))
        self.save_txt('确认答案2：{}'.format(Answer2))
        self.save_txt('问题3：{}'.format('What is the first name of my childhood best friend?'))
        self.save_txt('答案3：{}'.format(Answer3))
        self.save_txt('确认答案3：{}'.format(Answer3))

    def liucheng4(self):
        """
        图片6,6-2,7 ,8填写生日 SSN ， 和确认提交
        :return:
        """
        print('开始图片第6,6-2,7,8张流程，填写生日 SSN信息等')
        birth_date = self.personal_information_dict.get('生日')#1985/5/19
        birth_date = birth_date.split('/')
        if len(birth_date[1]) == 1:
            birth_date[1] = '0'+birth_date[1]
        str2 = birth_date[1] + '/'+ birth_date[2] + '/' + birth_date[0]
        write(str2, into=S('//*[@id="formRegister:dob"]'))#生日
        self.save_txt('生日：{}'.format(str2))
        SSN = self.personal_information_dict.get('SSN')
        write(SSN, into=S('//*[@id="formRegister:UIClaimant_social"]'))#SSN
        self.save_txt('SSN：{}'.format(SSN))
        click(S('//*[@id="formRegister:buttondoAddReg"]')) #继续
        try:#监测是否被注册
            wait_until(Text('The SSN you provided is already in our records').exists, timeout_secs=5, interval_secs=0.4)
            print('SSN已被注册，跳过此行数据，从头开始注册')
            self.save_txt('SSN已经被注册，停止流程')
            del_line(self.personal_information_dict.get('驾照号'), self.personal_information_filename)  # 删除个人信息
            sleep(0.15)
            self.information_init()#从新初始化个人信息
            self.zhuce()
        except:
            pass
        click(S('//*[@id="formRegister:buttondoReg"]'))  # 图片7点击确认
        try:#监测是否有系统 问题
            wait_until(Text('There was a problem with the system. Please try again later.').exists, timeout_secs=5,
                       interval_secs=0.4)
            print('系统出现问题。刷新页面重试。')
            self.driver.refresh()
            click(S('//*[@id="formRegister:buttondoReg"]'))  # 图片7点击确认
        except:
            pass
        #图 片8  出现这个表示注册成功
        try:
            wait_until(Text('Your NY GOV Username is:').exists, timeout_secs=15, interval_secs=0.4)
            print('注册流程完成')
        except:
            print('没有注册成功')
    def liucheng5(self):
        """
        图片9，10,11
        :return:
        """
        print('开始图片第9,10,11张流程')
        self.driver.get('https://www.labor.ny.gov/signin')
        click(S('//*[@id="signInButton"]'))  # 点击 sign in
        try:
            write(self.username, into=S('//*[@id="loginform:username"]'))  # 用户名
            write(self.pwd, into=S('//*[@id="loginform:password"]'))  # 密码
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
                self.check_img_exist('/img/login.png')
            print('开始输入用户名密码')
            write(self.username, into=S('//*[@id="loginform:username"]'))  # 用户名
            write(self.pwd, into=S('//*[@id="loginform:password"]'))  # 密码
        print("请手动输入验证码,400秒后超时")
        self.chick_yanzhengma()
        click(S('//*[@id="loginform:signinButton"]'))  # 点击登录
    def liucheng6(self):
        """
        图片12，13
        :return:
        """
        print('开始图片第12,13张流程')
        wait_until(Link('Unemployment Services').exists, timeout_secs=40, interval_secs=0.4)
        click(Link('Unemployment Services'))  # 点击Unemployment Services
        write(self.personal_information_dict.get('SSN'), into=S('//*[@id="form:uiClaimant_ssn1to9"]'))
        write(self.personal_information_dict.get('SSN'), into=S('//*[@id="form:uiClaimant_confirmSsn1to9"]'))
        click(S('//*[@id="form:submitClaimantInfo"]'))#点击提交
    def liucheng7(self):
        """
        图片14
        :return:
        """
        print('开始图片第14张流程')
        PIN = get_ranrom_pin(4)
        print("生成随机PIN:", PIN)
        write(PIN, into=S('//*[@id="form:uiClaimant_pin_new"]'))
        write(PIN, into=S('//*[@id="form:uiClaimant_pin_confirm"]'))
        self.save_txt("PIN:{}".format(PIN))
        self.mother_name = get_ranrom_name(7)
        print("生成随机Mother's Maiden Name:", self.mother_name)
        write(self.mother_name, into=S('//*[@id="form:uiClaimant_maidenName"]'))
        write(self.mother_name, into=S('//*[@id="form:uiClaimant_maidenNameConf"]'))
        self.save_txt("Mother's Maiden Name:{}".format(self.mother_name))
        click(S('//*[@id="form:submitNewPinMmn"]'))  # 点击提交
        print('请手动识别验证码，400秒后超时')


    def liucheng8(self):
        """
        图片15，16，17
        :return:
        """
        print('开始图片第15，16，17张流程')
        try:
            wait_until(Text('File A Claim').exists, timeout_secs=400, interval_secs=0.4)
            print('识别成功')
            click(S('//*[@id="content"]/form[1]/input[5]')) #点击File A Claim
        except:
            print('或许图片识别超时')
        click(S('//*[@id="content"]/form/center/input')) #点击继续
        click(S('//*[@name="button" and @value="I Agree"]'))#点击同意

    def liucheng9(self):
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
        click(S('//input[@value="Continue"]'))#点击提交

    def liucheng10(self):
        """
        图片19,19-2
        :return:
        """
        print('开始图片19,19-2流程')
        write(self.personal_information_dict.get('驾照号'), into=S('//*[@id="UC1G04_F08"]'))
        self.save_txt("驾照号:{}".format(self.personal_information_dict.get('驾照号')))
        Select(S('//*[@id="UC1G04_F09"]').web_element).select_by_visible_text('One employer')
        click(S('//input[@value="Continue"]'))  # 点击提交

    def liucheng11(self):
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

    def liucheng12(self):
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

    def liucheng13(self):
        """
        图片24
        :return:
        """
        print('开始图片第24张流程')
        try:
            wait_until(Text('Federal Employer Identification Number (FEIN)').exists, timeout_secs=5, interval_secs=0.4)
            click(S('//input[@value="Continue"]'))  # 点击提交
        except:
            print('请手动操作到流程第6步')
        title = self.driver.title
        for i in range(2000):
            sleep(1)
            if title == 'Most Recent Employer Information, Part 2':
                break
        wait_until(S('//*[@id="UC1G10_F01"]').exists, timeout_secs=1000, interval_secs=0.4)
        write(self.personal_information_dict.get('公司名字'), into=S('//*[@id="UC1G10_F01"]'))  # 公司名字
        write(self.personal_information_dict.get('公司地址'), into=S('//*[@id="UC1G10_F02"]'))  # 公地址
        write(self.personal_information_dict.get('公司市'), into=S('//*[@id="UC1G10_F04"]'))  # 公地市
        write(self.personal_information_dict.get('公司电话')[0:3], into=S('//*[@id="UC1G10_F08P1"]'))
        write(self.personal_information_dict.get('公司电话')[3:6], into=S('//*[@id="UC1G10_F08P2"]'))
        write(self.personal_information_dict.get('公司电话')[6:], into=S('//*[@id="UC1G10_F08P3"]'))
        write(self.personal_information_dict.get('公司邮编'), into=S('//*[@id="UC1G10_F06"]'))
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
        self.save_txt("公司名字:{}".format(self.personal_information_dict.get('公司名字')))
        self.save_txt("公司地址:{}".format(self.personal_information_dict.get('公司地址')))
        self.save_txt("公司市:{}".format(self.personal_information_dict.get('公司市')))
        self.save_txt("公司电话:{}".format(self.personal_information_dict.get('公司电话')))
        self.save_txt("公司邮编:{}".format(self.personal_information_dict.get('公司邮编')))
    def liucheng14(self):
        """
        图片25
        :return:
        """
        print('开始图片25张流程')
        click(S('//*[@id="UC1G10_UC10_F01"]'))  # 第1行单选选 yes
        click(S('//td[@colspan="3"]//input[@value="Continue"]'))  # 点击提交

    def liucheng15(self):
        """
        图片26,26-2
        :return:
        """
        print('开始图片第26,26-2张流程')
        click(S('//*[@id="UC1G05_F15"]'))  # 第1行单选选 no
        write(self.personal_information_dict.get('个人地址'), into=S('//*[@id="UC1G05_F03"]'))
        write(self.personal_information_dict.get('个人市'), into=S('//*[@id="UC1G05_F05"]'))
        Select(S('//*[@id="UC1G05_F06"]').web_element).select_by_visible_text('New York')
        Select(S('//*[@id="UC1G05_F38"]').web_element).select_by_visible_text('Four-year degree program')
        write(self.personal_information_dict.get('个人邮编'), into=S('//*[@id="UC1G05_F07"]'))
        write(self.phone_dict.get('电话')[0:3], into=S('//*[@id="UC1G05_F34P1"]'))
        write(self.phone_dict.get('电话')[3:6], into=S('//*[@id="UC1G05_F34P2"]'))
        write(self.phone_dict.get('电话')[6:], into=S('//*[@id="UC1G05_F34P3"]'))
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
        self.save_txt("个人电话:{}".format(self.phone_dict.get('电话')))
        self.save_txt("个人地址:{}".format(self.personal_information_dict.get('个人地址')))
        self.save_txt("个人市:{}".format(self.personal_information_dict.get('个人市')))
        self.save_txt("个人邮编:{}".format(self.personal_information_dict.get('个人邮编')))
    def liucheng16(self):
        """
        图片27,28
        :return:
        """
        print('开始图片第27,28张流程')
        click(S('//form[@name="addrNormForm"]/input[@value="Use this address"]'))
        Select(S('//*[@id="DirectDeposit_PaymentOption"]').web_element).select_by_visible_text('Direct Deposit')
        click(S('//input[@value="Continue"]'))  # 点击提交
        print('流程完成，开始清理已使用的信息')
        del_line(self.personal_information_dict.get('驾照号'), self.personal_information_filename)#删除个人信息
        print('删除使用过的个人信息完成')
        del_line(self.email_dict.get('邮箱地址'), self.email_filename)#删除个人邮箱
        print('删除使用过的个人邮箱完成')
        del_line(self.phone_dict.get('电话'), self.phone_filename)#删除个人电话
        print('删除使用过的个人电话完成')
        write(self.mother_name, into=S('//*[@id="DirectDeposit_MothersMaidenName"]'))
        print('剩余流程请手动完成，完成后重启软件')
    def check_img_exist(self,img_name):
        """
        检测当前页面是否有 图片 存在
        :param img_name:
        :return:
        """
        self.driver.save_screenshot('./img/screen_all.png')
        sleep(0.2)
        try:
            x, y = PictureRecognition.matchImg(img_name, './img/screen_all.png')
            return True
        except:
            return False

    #print(check_img_exist('./img/ok.png'))

    def click_yanzhengma(self):
        """
        验证码识别点击
        :return:
        """
        click(S('//div[contains(@id,"j_id_jsp_")]/div/div/iframe'))  # 点击弹出验证码
        sleep(2)
        img_element = S('//*[@id="rc-imageselect"]').web_element #获取验证码元素
        GetPng(self.driver).get_geetest_image()  # 获取验证码图片

        l = get_coordinate()  # 获取识别的坐标 [['90', '331'], ['244', '346'], ['213', '436'], ['308', '451']] #g
        print(l)
        for position in l:
            print(position)
            # 动作链对象
            action = ActionChains(self.driver)
            # action.move_to_element_with_offset(img_element,int(position[0])+286,int(position[1])).click().perform()#鼠标移动到元素点击坐标
            action.move_to_element_with_offset(img_element, int(position[0]),
                                               int(position[1])).click().perform()  # 鼠标移动到元素点击坐标
            sleep(0.3)
        click(Button('Verify')) #点击确认


    def save_txt(self,txt):
        """
        保存文本，用户名， 手机号，机器码
        :param txt:
        :return:
        """
        print(txt)
        filename ='./result/'+ self.firse_name+self.last_name+'.txt'
        encod = 'utf-8'
        with open(filename, 'a', encoding=encod) as f:
            f.write(txt+'\n')
        sleep(0.1)

    def quit(self):
        self.driver.quit()

def setup_zhuce(B):
    B.liucheng1()
    B.liucheng2()
    B.liucheng3()
    B.liucheng4()

def setup_2(B):
    B.liucheng5()
    B.liucheng6()
    B.liucheng7()
    B.liucheng8()
    B.liucheng9()
    B.liucheng10()
    B.liucheng11()
    B.liucheng12()
    B.liucheng13()
    B.liucheng14()
    B.liucheng15()
    B.liucheng16()

def setup(B):
    setup_zhuce(B)
    setup_2(B)

if __name__ == '__main__':
    B = BaseStartChome(9022)
    # setup(B)
    setup_zhuce(B)