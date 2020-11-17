#coding=utf-8

from helium import *
from itertools import zip_longest
from kill_prot import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from locale import atof,setlocale,LC_NUMERIC
from email_oper import *
from get_template import get_temp_dict,get_filename
from send_request import SendRequest
from selenium.webdriver.support.ui import Select
from yanzhengqi_oper import get_make_code
from base64_to_img import to_png
from chick_proxy import servers_chick_ip
from del_txt_line import del_line#用一行删除一行
from url_2_png import get_src_img
from email_oper import get_url

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

    def __init__(self,port,ip):
        self.temp_filename = get_filename('.txt', 'template')
        self.temp_dict = get_temp_dict(self.temp_filename)  # 模板
        self.ip = ip
        #kill_pid(port)
        kill_all_chorme()
        sleep(3)
        # 关闭进程
        #self.cmd = r'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="C:\selenum\AutomationProfile{port}" --window-size=1080,800 '.format(chrome_path=chrome_path,port=port)  # --headless
        #加代理ip，#标记要修改
        self.cmd = r'"{chrome_path}" --remote-debugging-port={port} --user-data-dir="C:\selenum\AutomationProfile{port}" --window-size=1080,800 --proxy-server=http://{ip}'.format(
            chrome_path=chrome_path, port=port, ip=ip)  # --headless
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
        self.ip_state = self.chick_ip() #标记要修改

    def chick_ip(self):
        """
        检测ip是否有效
        :return:
        """
        self.driver.get("https://www.baidu.com/")
        title = self.driver.title
        del_line(self.ip, 'ip.txt')  # 访问百度之后删除ip
        if title == 'www.baidu.com':
            return False
        else:
            return True

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



    def chick_liucheng_bakeup(self):
        """
        流程准备工作检测，登录成功后可能提示We're sorry!
        :return:
        """
        try:
            wait_until(Text("We're sorry!").exists, timeout_secs=6, interval_secs=0.4)
            return False
        except:
            return True
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
    def save_txt(self,txt):
        """
        保存文本，用户名， 手机号，机器码
        :param txt:
        :return:
        """
        def get_file_code():
            f3 = open('结果.txt', 'rb')
            data = f3.read()
            encode = chardet.detect(data).get('encoding')
            f3.close()
            return encode
        with open('结果.txt', 'a', encoding=get_file_code()) as f:
            f.write(txt+'\n')
    def liucheng1(self):
        """
        邮箱注册成功之后的流程的第一步基本信息填写
        :return:
        """
        click(S('//*[@id="a-autoid-0"]/span/input'))#点击批准
        wait_until(S('//input[@name="pincode"]').exists, timeout_secs=20, interval_secs=0.4)  ## 是否有邮编输入框
        write(self.temp_dict.get('邮编'),into=S('//input[@name="pincode"]'))
        write(self.temp_dict.get('街道地址'),into=S('//input[@name="address_line1"]'))
        write(self.temp_dict.get('城市'), into=S('//input[@name="city"]'))
        write(self.temp_dict.get('省'), into=S('//input[@name="state"]'))
        #获取电话号码
        self.SR = SendRequest()
        self.phone = self.SR.get_phone()
        print('获取到的手机号是{}'.format(self.phone))
        write('+86 {}'.format(self.phone), into=S('//*[@name="phoneno"]'))
        write(self.temp_dict.get('英文名'),into=S('//input[@name="firstName"]'))
        write(self.temp_dict.get('英文姓'),into=S('//input[@name="lastName"]'))
        write(self.temp_dict.get('统一社会信用代码'), into=S('//input[@name="businessLicenseNumber"]'))
        click(S('//*[@name="Submit"]'))  # 点击保存并继续


    def liucheng2(self):
        print('开始第二步流程')
        wait_until(S('//*[@name="countryOfCitizenship"]').exists, timeout_secs=100, interval_secs=0.4)  ## 是否有邮编输入框
        Select(S('//*[@name="countryOfCitizenship"]').web_element).select_by_visible_text('China')#国籍
        sleep(3)
        Select(S('//*[@name="countryOfBirth"]').web_element).select_by_visible_text('United States')#出生地
        sleep(2)
        def send_data():
            Select(S(
                '//div[contains(@id,"PointOfContact_SIV_Identity_")]/div/div/div[2]/form/div/div/div[3]/div/div[2]/div[2]/div[2]/div/div/dropdown-date-picker/div/span[3]/select').web_element).select_by_visible_text(
                '1993')#出生日期年
            sleep(0.3)
            Select(S(
                '//div[contains(@id,"PointOfContact_SIV_Identity_")]/div/div/div[2]/form/div/div/div[3]/div/div[2]/div[2]/div[2]/div/div/dropdown-date-picker/div/span[2]/select').web_element).select_by_visible_text(
                'Mar')#出生日期月
            sleep(0.3)
            Select(S(
                '//div[contains(@id,"PointOfContact_SIV_Identity_")]/div/div/div[2]/form/div/div/div[3]/div/div[2]/div[2]/div[2]/div/div/dropdown-date-picker/div/span[1]/select').web_element).select_by_visible_text(
                '23')#出生日期日
            sleep(0.3)
            Select(S(
                '//div[contains(@id,"PointOfContact_SIV_Identity_")]/div/div/div[2]/form/div/div/div[3]/div/div[3]/div[5]/div/div[1]/div[2]/div/div[1]/div[2]/dropdown-date-picker/div/span[3]/select').web_element).select_by_visible_text(
                '2023')#有效期 年
            sleep(0.3)
            Select(S(
                '//div[contains(@id,"PointOfContact_SIV_Identity_")]/div/div/div[2]/form/div/div/div[3]/div/div[3]/div[5]/div/div[1]/div[2]/div/div[1]/div[2]/dropdown-date-picker/div/span[2]/select').web_element).select_by_visible_text(
                'May')#有效期 月
            sleep(0.3)
            Select(S(
                '//div[contains(@id,"PointOfContact_SIV_Identity_")]/div/div/div[2]/form/div/div/div[3]/div/div[3]/div[5]/div/div[1]/div[2]/div/div[1]/div[2]/dropdown-date-picker/div/span[1]/select').web_element).select_by_visible_text(
                '07')#有效期 日
            sleep(0.3)
        send_data()
        write(self.temp_dict.get('身份证'), into=S('//*[@name="docNumber"]'))
        write(self.temp_dict.get('中文姓'), into=S('//*[@name="chineseLastName"]'))
        write(self.temp_dict.get('中文名'), into=S('//*[@name="chineseFirstName"]'))
        try:
            click(RadioButton(self.temp_dict.get('省')))
        except:
            click(RadioButton(self.temp_dict.get('城市')))
        write('+86 {}'.format(self.phone), into=S('//*[@id="country-phone-input"]'))
        click(S('//*[@name="sendVerificationButton" and not(@disabled)]//span[contains(text(),"Text me now")]'))  # 点击提交
        def get_phone_code(self):
            phone_code = self.SR.get_phone_msg(self.phone)
            if phone_code:
                return phone_code
            else:#此号码不可用
                click(S('//*[@id="cancelOTPLink"]/span'))#取消弹窗
                self.phone = self.SR.get_phone() #重新获取号码
                write('+86 {}'.format(self.phone), into=S('//*[@id="country-phone-input"]'))
                click(S('//*[@name="sendVerificationButton" and not(@disabled)]//span[contains(text(),"Text me now")]'))
                return get_phone_code(self)
        phone_code = get_phone_code(self)
        write(phone_code, into=S('//*[@name="otpInput"]'))#输入验证码
        click(S('//*[@name="verifyOTPButton"]'))#点击提交
        #if not CheckBox("is a beneficial owner of the business").is_checked():#复选框没有被选中
        click(CheckBox("is a beneficial owner of the business"))
        #if not CheckBox("is a legal representative of the business").is_checked():
        click(CheckBox("is a legal representative of the business"))
        #if not CheckBox("I confirm that I have added all the beneficial owners of the business.").is_checked():
        click(CheckBox("I confirm that I have added all the beneficial owners of the business."))
        click('Save and Continue')  # 点击提交
        try:
            wait_until(Text('Enter a valid date of').exists, timeout_secs=2, interval_secs=0.4)  ## 日期没有输入成功
            send_data()
            click('Save and Continue')  # 点击提交
        except:
            pass
    def liucheng3(self):
        print('开始第三步流程')
        wait_until(S('//*[@name="addCreditCardNumber"]').exists, timeout_secs=100, interval_secs=0.5)  # 需要安全验证
        write(self.temp_dict.get('银行卡号'), into=S('//*[@name="addCreditCardNumber"]'))
        Select(S('//*[@name="ccExpirationMonth" and not(@disabled)]').web_element).select_by_visible_text(
            self.temp_dict.get('到期日'))  # 有效期 日
        Select(S('//*[@name="ccExpirationYear" and not(@disabled)]').web_element).select_by_visible_text(
            self.temp_dict.get('到期年'))  # 有效期 日
        write(self.temp_dict.get('英文姓') + self.temp_dict.get('英文名'), into=S('//*[@name="ccHolderName"]'))
        #write('854639', into=S('//*[@name="otpInput"]'))  # 输入验证码
        click('Save')
        wait_until(S('//*[@name="Submit"]').exists, timeout_secs=60, interval_secs=0.5)
        click(S('//*[@name="Submit"]'))#保存并继续

    def liucheng4(self):
        print('开始第四步流程')
        wait_until(Link('listing your products').exists, timeout_secs=120, interval_secs=0.5)  # 需要安全验证
        click(Link('listing your products'))
        name = self.temp_dict.get('商品英文名')
        try:
            write(name, into=S('//*[@name="displayNameField"]'))
        except:
            self.driver.refresh()
            write(name, into=S('//*[@name="displayNameField"]'))
        click(S('//*[@name="Submit"]'))  # 点击提交，但是提交后可能没货
        def chick():  # 检查是否有货
            for i in range(1, 1000):
                try:
                    wait_until(Text('Not available').exists, timeout_secs=4, interval_secs=0.4)  ## 没保存表示没货
                    write(name + str(i), into=S('//*[@name="displayNameField"]'))
                    click(S('//*[@name="Submit"]'))  # 点击提交，但是提交后可能没货
                except:  # 有货
                    return
        chick()
        try:
            click('Start listing your products')
            wait_until(Text('View Credit Card Info').exists, timeout_secs=100, interval_secs=0.5)
            click(Button('View Credit Card Info'))  #查看信用卡信息
        except:
            pass
        click(Button('Enable Two-Step Verification')) #启动两步验证
        #这里要输入密码
        try:
            write(self.pwd, into=S('//*[@id="ap_password"]'))
            click(S('//*[@id="signInSubmit"]')) #点击登录
            self.driver.get('https://sellercentral.amazon.co.uk/authorization/failed/invalid-credit-card?returnTo=%2Fgp%2Fhomepage.html')
            click(Button('View Credit Card Info'))  # 查看信用卡信息
            click(Button('Enable Two-Step Verification'))  # 启动两步验证
        except:
            pass
        click(S('//*[@id="sia-otp-accordion-totp-header"]/i')) #点击充应用器注册
        sleep(1.5)
        click(Link("Can't scan the barcode?"))
        sleep(0.2)
        tet = S('//*[@id="sia-auth-app-formatted-secret"]').web_element.text #这个是生成玛
        print(tet)
        try:
            code = get_make_code(tet)
        except:
            sleep(0.3)
            code = get_make_code(tet)
        write(code, S('//*[@id="ch-auth-app-code-input"]'))
        # APP转码这里留着下次做
        base64_str = S('//*[@id="container"]//img').web_element.get_attribute('src')
        to_png(base64_str,'./img2/{}.png'.format(self.name)) #保存图片
        #存储
        self.save_txt(self.name)
        self.save_txt(self.phone)
        self.save_txt(tet)
        self.save_txt('*'*70)
        click(S('//*[@id="ch-auth-app-submit"]'))#点击验证
        if not CheckBox("Don't require OTP on this browser").is_checked():#勾选请勿记住密码
            click(CheckBox("Don't require OTP on this browser"))
        click(S('//*[@id="enable-mfa-form-submit"]'))#提交

    def quit(self):
        self.driver.quit()
def get_ip():
    with open("ip.txt", "r", encoding='utf-8') as f:
        txt_lines = f.readlines()
    for txt_line in txt_lines:
        ip = txt_line.strip('\n')
        if servers_chick_ip(ip):
            return ip
        else:
            del_line(ip, 'ip.txt')
            sleep(0.05)

def setup(B, line):
    try:
        u = line.split('----')[0].strip('\n')
        p = line.split('----')[1].strip('\n')
    except:
        u= ''
        p =''
        print(line + '格式不对')
    if u:
        # #登录,且发送注册邮件
        state_login = B.login(u, p)
        if state_login:
            print('登录成功，开始获取邮箱信息')
            # 打开网易邮箱登录框，登录
            url =get_url(u, p)
            B.driver.get(url)
            if B.chick_liucheng_bakeup():
                B.liucheng1()
                B.liucheng2()
                B.liucheng3()
                B.liucheng4()
                os.remove(B.temp_filename)#删除模板文件
            else:
                print("出现We're sorry!页面，跳过账号！")
            B.quit()
        else:
            print(u + '登录失败！开始下一个')



if __name__ == '__main__':
    #文件对象是迭代器。要一次迭代文件N行，与线程数一致，一次迭代N行就执行多少个线程
    print(get_ip())
