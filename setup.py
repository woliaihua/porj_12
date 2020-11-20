#coding=utf-8

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



def get_login_code(driver):
    """
    获取登录验证码
    :return:
    """
    while 1:
        set_driver(driver)
        print('识别中...')
        scr = S('//*[@id="auth-captcha-image"]').web_element.get_attribute('src')
        get_src_img(scr, './img/login_code8.png')
        sleep(0.3)
        code = png_2_text('./img/login_code8.png')
        if code:
            code = code.strip().replace(' ', '')
        else:
            code = ''
        if len(code) == 6:
            return code
        else:
            click(S('//*[@id="auth-captcha-refresh-link"]'))  # 点击换一张
            wait_until(S('//*[@id="auth-captcha-refresh-link" and @style="display: inline;"]').exists,
                       timeout_secs=20, interval_secs=0.4)  ## 等待图片加载成功
            return get_login_code(driver)

class BaseStartChome():
    """
    反爬模式启动浏览器
    """

    def __init__(self,port):
        self.personal_information_filename = get_filename('.txt', '个人信息')
        self.personal_information_dict = get_temp_dict(self.personal_information_filename)  # 个人信息
        self.phone_filename = get_filename('.txt', '个人电话')
        self.phone_dict = get_phone_dict(self.phone_filename)  # 个人电话
        self.email_filename = get_filename('.txt', '个人邮箱')
        self.email_dict = get_email_dict(self.email_filename)  # 邮箱
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
        Config.implicit_wait_secs =10 #设置隐式等待时间15秒

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
        for i in range(200):
            if i == 0:
                sleep(2.5)
            sleep(1)
            img_exist = self.check_img_exist('./img/ok.png')
            if img_exist:#ok图片存在表示成功
                print('验证码通过')
                return
            else:
                print('循环检测验证码是否验证成功...')
            if i == 99:
                print('超时，程序退出')
                sys.exit()

    def liucheng1(self):
        """
        第一二张：注册
        :return:
        """
        self.firse_name = self.personal_information_dict.get('First 名字')
        self.last_name = self.personal_information_dict.get('last 姓')
        self.email = self.email_dict.get('邮箱地址')
        self.driver.get('https://applications.labor.ny.gov/IndividualReg/xhtml/individual/emailVerification.faces')
        write(self.firse_name, into=S('//*[@id="userNameFirst"]'))  # firse name
        write(self.last_name, into=S('//*[@id="userNameLast"]'))  # last name
        write(self.email, into=S('//*[@id="userEmail"]'))  # E-mail Address
        write(self.email, into=S('//*[@id="userEmailConfirm"]'))  # Confirm E-mail Address
        click(S('//div[contains(@id,"j_id_jsp_")]/div/div/iframe')) #点击弹出验证码
        print('请输出验证码')
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
        print('开始激活邮箱')
        self.email_pwd = self.email_dict.get('邮箱密码')
        #switch_to(find_all(Window())[1])  # 打开第0个窗口
        self.driver.get("https://login.yahoo.com/")
        self.driver.delete_all_cookies()
        self.driver.refresh()
        try:
            wait_until(S('//*[@id="login-username"]').exists, timeout_secs=2, interval_secs=0.4)
        except:
            click(Link('Sign in'))
            wait_until(Link('Use another account').exists, timeout_secs=2, interval_secs=0.4)
            click(Link('Use another account'))
        write(self.email, into=S('//*[@id="login-username"]'))  # 输入邮箱地址
        click(S('//*[@id="login-signin"]'))  # 点击下一步
        write(self.email_pwd, into=S('//*[@id="login-passwd"]'))  # E-mail Address
        click(S('//*[@id="login-signin"]'))  # 点击下一步
        click(S('//*[@id="ybarMailLink"]/span[1]'))  # 点击收件箱
        for i in range(60):
            try:
                click(Text('Individual Account Creation for Online Services'))  # 点击第一封邮件
                break
            except:
                print('暂时没有收到邮件，1秒后面重新检测...')
            if i == 59:
                print('1分钟还未收到邮件，程序退出')
                sys.exit()
        self.save_txt('邮箱密码：{}'.format(self.email_pwd))
        try:
            click(Link('Click here to continue with the registration process.'))  # 点击激活链接
        except:
            sleep(1)
            try:
                click(Text('Individual Account Creation for Online Services'))  # 点击第一封邮件
                click(Link('Click here to continue with the registration process.'))  # 点击激活链接
            except:
                print('没有收到邮件')

    def liucheng3(self):
        """
        第五张图，激活邮件种输入详细信息
        :return:
        """
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
        self.save_txt('用户名：{}'.format(self.username))
        self.save_txt('密码：{}'.format(self.pwd))
        self.save_txt('问题1：{}'.format('What was the name of my first pet?'))
        self.save_txt('答案1：{}'.format(Answer1))
        self.save_txt('确认答案1：{}'.format(Answer1))
        self.save_txt('问题2：{}'.format("What was my first grade teacher's last name?"))
        self.save_txt('确认答案2：{}'.format(Answer2))
        self.save_txt('描述2：{}'.format(Answer2))
        self.save_txt('问题3：{}'.format('What is the first name of my childhood best friend?'))
        self.save_txt('确认答案3：{}'.format(Answer3))
        self.save_txt('描述3：{}'.format(Answer3))

    def liucheng4(self):
        """
        图片6,7 填写生日 SSN ， 和确认提交
        :return:
        """
        birth_date = self.personal_information_dict.get('生日')#1985/5/19
        birth_date = birth_date.split('/')
        if len(birth_date[1]) == 1:
            birth_date[1] = '0'+birth_date[1]
        str2 = birth_date[1] + '/'+ birth_date[2] + '/' + birth_date[0]
        write(str2, into=S('//*[@id="formRegister:dob"]'))#生日
        self.save_txt('生日：{}'.format(str2))
        SSN = self.personal_information_dict.get('SSN')  # 1985/5/19
        write(SSN, into=S('//*[@id="formRegister:UIClaimant_social"]'))#SSN
        self.save_txt('SSN：{}'.format(SSN))
        click(S('//*[@id="formRegister:buttondoAddReg"]')) #确认
        click(S('//*[@id="formRegister:buttondoReg"]')) #图片7 确认

    def liucheng5(self):
        """
        图片9，10
        :return:
        """
        self.driver.get('https://applications.labor.ny.gov/IndividualReg/xhtml/individual/home.faces?ptnx=1')
        click(S('//*[@id="signInButton"]')) #点击 sign in
        write(self.username, into=S('//*[@id="loginform:username"]'))  # 用户名
        write(self.pwd, into=S('//*[@id="loginform:password"]'))  # 密码
        click(S('//*[@id="recaptcha-anchor-label"]'))    # 点击弹出验证码
        print('请输出验证码')
        self.chick_yanzhengma()  # 开始检查验证码是否通过
        click(S('//*[@id="loginform:signinButton"]'))


    def login(self,u,p):
        self.name = u.strip('\n')
        self.pwd = p.strip('\n')
        print('开始执行账号{}注册'.format(u))
        self.driver.get(
            'https://sellercentral.amazon.co.uk/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fsellercentral.amazon.co.uk%2Fhome&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=sc_uk_amazon_v2&openid.mode=checkid_setup&language=zh_CN&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=sc_uk_amazon_v2&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ssoResponse=eyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.a5mUI1lQr80X3ikb1RfOscCl9fzyVVqmwXRr7HiL8LvGu6_LPzJA3w.T45gQk4uPvjQ7NW0.Na-asGEBLFxeUQFlqMQgwJNXHMC74exdYEpDoxF-LZ9sURBQONC_tTvjCK5Rsr781XOY-SMbZMSmm3q4UhtKJKJVN3tYK-vsOlfm01WkIwsztXXVAtPK50U3GNL1TdWt83BC2gUPzCVvkSVunLWRqUtS3yqesp5rCOyBl4SKfhHTQs2581J8-15xVwQ7LiN1vVYU_tMMJWMimFq2SITB6lvXS9cm8Hs8Rv81scAwDMJUtyHMddsgLnOSZ3wRbY_YmVcS.IwaDHOGL2wtpgIvB_we95A')
        self.login_out()
        write(u, into=S('//*[@id="ap_email"]'))
        write(p, into=S('//*[@id="ap_password"]'))
        click(S('//*[@id="signInSubmit"]'))
        try:
            wait_until(Link("看不清, 换一张").exists, timeout_secs=8, interval_secs=0.4)  # 需要安全验证
            print('需要安全验证，开始安全验证')
            def chick_code(self):
                try:
                    wait_until(Link("看不清, 换一张").exists, timeout_secs=8, interval_secs=0.4)  # 有验证码
                    try:
                        wait_until(Text('我们找不到具有该电子邮件地址的账户').exists, timeout_secs=1, interval_secs=0.4)
                        print('找不到具有该电子邮件地址的账户')
                        return False
                    except:
                        pass
                    print('开始识别验证码')
                    code = get_login_code(self.driver)
                    print("验证码是：",code)
                    print('开始输入验证码')
                    write(p, into=S('//*[@id="ap_password"]'))
                    write(code, into=S('//*[@id="auth-captcha-guess"]'))
                    click(S('//*[@id="signInSubmit"]'))
                    return chick_code(self)
                except Exception as e:
                    print(e)
                    return True
            chick_state = chick_code(self)#验证码登录状态
            if not chick_state:#找不到具有该电子邮件地址的账户的情况
                return False
            try:
                wait_until(S('//*[@id="channelDetails"]').exists, timeout_secs=10, interval_secs=0.4)  ## 是否有批准按钮
                return True
            except:
                return False
        except Exception as e:
            print(e)
            try:
                wait_until(S('//*[@id="channelDetails"]').exists, timeout_secs=3, interval_secs=0.4)  ## 是否有批准按钮
                return True
            except:
                return False

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
        filename ='./result/'+ self.last_name+self.last_name+'.txt'
        encod = 'utf-8'
        with open(filename, 'a', encoding=encod) as f:
            f.write(txt+'\n')

    def quit(self):
        self.driver.quit()

def setup(B):
    B.liucheng1()
    B.liucheng2()
    B.liucheng3()
    B.liucheng4()


if __name__ == '__main__':
    B = BaseStartChome(9022)
    setup(B)
