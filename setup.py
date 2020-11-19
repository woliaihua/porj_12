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
        self.personal_information_filename = get_filename('.txt', '个人信息')
        self.personal_information_dict = get_temp_dict(self.personal_information_filename)  # 个人信息
        self.phone_filename = get_filename('.txt', '个人电话')
        self.phone_dict = get_phone_dict(self.phone_filename)  # 个人电话
        self.email_filename = get_filename('.txt', '个人邮箱')
        self.email_dict = get_email_dict(self.email_filename)  # 邮箱
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
        for i in range(100):
            if i == 0:
                sleep(2.5)
            sleep(1)
            img_exist = self.check_img_exist('./img/ok.png')
            if img_exist:#ok图片存在表示成功
                print('验证码通过')
                return
            else:
                print('循环检测验证码是否验证成功种...')
            if i == 99:
                print('超时，程序退出')
                sys.exit()

    def liucheng1(self):
        """
        第一二张：注册
        :return:
        """
        self.driver.get('https://applications.labor.ny.gov/IndividualReg/xhtml/individual/emailVerification.faces')
        write(self.personal_information_dict.get('First 名字'), into=S('//*[@id="userNameFirst"]'))  # firse name
        write(self.personal_information_dict.get('last 姓'), into=S('//*[@id="userNameLast"]'))  # last name
        write(self.email_dict.get('邮箱地址'), into=S('//*[@id="userEmail"]'))  # E-mail Address
        write(self.email_dict.get('邮箱地址'), into=S('//*[@id="userEmailConfirm"]'))  # Confirm E-mail Address
        click(S('//div[contains(@id,"j_id_jsp_")]/div/div/iframe')) #点击弹出验证码
        print('请输出验证码')
        self.chick_yanzhengma()#开始检查验证码是否通过
        # click(Link('Contact Us'))  # 打开一个新的标签页面
        # switch_to(find_all(Window())[0])  # 切换到第0个窗口
        click(S('//*[@id="buttondoAddReg"]'))  # 点击continue

    def liucheng2(self):
        """
        第三四张：激活邮箱
        :return:
        """
        #switch_to(find_all(Window())[1])  # 打开第0个窗口
        self.driver.get("https://login.yahoo.com/")
        write('VioletAugustinelAa84460@yahoo.com', into=S('//*[@id="login-username"]'))  # 输入邮箱地址
        click(S('//*[@id="login-signin"]'))  # 点击下一步
        write('ziIgJAbUKCr', into=S('//*[@id="login-passwd"]'))  # E-mail Address
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
        click(Link('Click here to continue with the registration process.'))  # 点击第一封邮件

    def liucheng3(self):
        """
        第五张图，激活邮件种输入详细信息
        :return:
        """
        self.username = get_ranrom_str(12)
        print("生成随机用户名:", self.username)
        self.pwd = get_ranrom_str(16)
        print("生成随机密码:", self.pwd)
        write(self.username, into=S('//*[@id="userID"]'))  # 用户名
        write(self.pwd, into=S('//*[@id="userPassword"]'))  # 密码
        write(self.pwd, into=S('//*[@id="userPassword2"]'))  # 确认密码


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
        def get_file_code():
            f3 = open('结果.txt', 'rb')
            data = f3.read()
            encode = chardet.detect(data).get('encoding')
            f3.close()
            return encode

        try:
            encod = get_file_code()
        except:
            encod = 'utf-8'
        with open('结果.txt', 'a', encoding=encod) as f:
            f.write(txt+'\n')

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
    import sys
    #文件对象是迭代器。要一次迭代文件N行，与线程数一致，一次迭代N行就执行多少个线程
    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)
    # 分批读取账号
    with open('邮箱.txt', 'r') as f:
        txt_lines = f.readlines()
    def setup_chick_ip(port):
        ip = get_ip()
        if ip:
            B = BaseStartChome(port, ip)
            ip_state = B.ip_state
            if not ip_state:  # ip不可用
                print(ip, '不可用，切换ip')
                setup_chick_ip(port)
            return B
        else:
            print('没有ip了，退出程序！')
            sys.exit()
    ip_num = 1  # 几次账号就换一次ip
    for lines in grouper(txt_lines, int(ip_num), ''):
        B = setup_chick_ip(9022)
        for line in lines:  # 一次读取N个账号
            setup(B, line)
        print('切换ip')
        B.driver.quit()

    # with open('邮箱.txt', 'r') as f:
    #     for line in f.readlines():
    #         B = BaseStartChome(9022, 'ip')
    #         setup(B,line,'port')
            #print(1+'1')
