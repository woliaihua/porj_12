
import  win32con
from PIL import  ImageGrab
from win32gui  import *
import win32api
import win32gui
import win32clipboard as w
from  time import sleep
from mouseToClick import MouseToClick
from img_2_text import png_2_text
import os
from exe_oper import re_start_exe
import chardet
import configparser

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

def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    sleep(0.35)
    print(handle)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        # 返回坐标值和handle
        return win32gui.GetWindowRect(handle), handle

def fetch_image():
    (x1, y1, x2, y2), handle = get_window_pos('网易邮箱大师')
    #print(x1,y1,x2,y2)
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # 设为高亮
    win32gui.SetForegroundWindow(handle)
    # 截图
    grab_image = ImageGrab.grab((x1, y1, x2, y2))
    #image = Image.open('./screenshot.png')   #打开图片
    box = (831,576,1163,607)#设置要裁剪的区域,可以使用画图工具识别坐标
    region =  grab_image.crop(box)#此时，region是 一个新的对象
    #region.show()#显示的话就会被占用，所以要注释
    region.save("123.png")
    return "123.png"

class GetWindowMsg():
    def __init__(self,clasename,window_name):
        self.window_name = window_name
        self.handle = FindWindow(clasename, window_name)#获取窗口句柄
        self.shezhi()
        # self.title = GetWindowText(self.handle)#获取窗口标题
        # print(self.title)

    def shezhi(self):
        """
        设置窗口前台
        :return:
        """
        # 发送还原最小化窗口的信息
        win32gui.SendMessage(self.handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        win32api.keybd_event(13, 0, 0, 0)  #
        SetForegroundWindow(self.handle)  # 设置窗口前台
        ShowWindow(self.handle, 1)  # 显示窗口

    #鼠标后台点击 这里是点击不是好友的位置
    def doClick(self,handle,x=106, y=256,):
        long_position = win32api.MAKELONG(x, y)  # 模拟鼠标指针 传送到指定坐标
        sleep(0.05)
        back1 = win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
        sleep(0.05)
        back2 = win32api.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起

    # 发送文字
    def setText(self,info):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, info)  # 设置剪切板内容
        w.CloseClipboard()  # 关闭剪贴板
        sleep(0.3)

    # 定位QQ窗口，进行昵称备注的搜索，再回车弹出此好友窗口
    def send_usernmae(self):
        # SetForegroundWindow(self.handle)  # 设置窗口前台
        # ShowWindow(self.handle, 1)  # 显示窗口
        # win32gui.SendMessage(self.handle, 52, 199, 2080193)  # 指定坐标发送
        # win32gui.SendMessage(self.handle, 770, 0, 0)
        sleep(0.3)
        win32gui.SendMessage(self.handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.SendMessage(self.handle, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    def login(self,u,p):
        G = GetWindowMsg('LoginWindow', '网易邮箱大师')
        G.send_usernmae()  # 光标点击输入框
        G.setText(u)
        # 模拟键盘组合键Ctrl+v将剪贴板的内容复制到搜索输入框中
        MouseToClick.twoKey('CTRL', 'V')  # 输入账号
        sleep(0.1)
        # 回车，光标移动到密码
        MouseToClick.oneKey('ENTER')
        sleep(0.1)
        G.setText(p)
        sleep(0.01)
        MouseToClick.twoKey('CTRL', 'V')  # 输入密码
        MouseToClick.oneKey('ENTER')
    def login2(self,u,p):
        G = GetWindowMsg('LoginWindow', '网易邮箱大师')
        G.send_usernmae()  # 光标点击输入框
        G.setText(u)
        MouseToClick.oneKey('ENTER')
        sleep(0.1)
        # 模拟键盘组合键Ctrl+v将剪贴板的内容复制到搜索输入框中
        MouseToClick.twoKey('CTRL', 'V')  # 输入账号
        sleep(0.1)
        # 回车，光标移动到密码
        MouseToClick.oneKey('ENTER')
        sleep(0.1)
        G.setText(p)
        sleep(0.01)
        MouseToClick.twoKey('CTRL', 'V')  # 输入密码
        MouseToClick.oneKey('ENTER')
    def login3(self,u,p):
        sleep(0.2)
        self.setText(u)
        MouseToClick.click_img('./img/email_u.png')  # 点击邮件用户名
        sleep(0.2)
        MouseToClick.twoKey('CTRL', 'V')  # 输入账号
        sleep(0.1)
        self.setText(p)
        sleep(0.1)
        MouseToClick.oneKey('ENTER')
        sleep(0.15)
        MouseToClick.twoKey('CTRL', 'V')  # 输入密码
        sleep(0.2)
        MouseToClick.oneKey('ENTER')
        #MouseToClick.click_img('./img/email_p.png')  # 点击邮件密码
    def login_out(self):
        GetWindowMsg('MainWindow', '网易邮箱大师')
        sleep(0.3)
        try:
            MouseToClick.click_img('./img/shezhi.png')#点击设置
        except:
            MouseToClick.click_img('./img/shezhi2.png')
        try:
            MouseToClick.click_img('./img/del_email_button.png')#点击删除此邮箱
        except:
            sleep(1)
            MouseToClick.click_img('./img/email_setting.png')  # 点击邮箱设置
            sleep(1.5)
            MouseToClick.click_img('./img/del_email_button.png')  # 点击删除此邮箱
        MouseToClick.click_img('./img/bubaoliu.png')#点击不包含

    def get_url(self):
        """
        先置顶窗口再截图，再切小图，再使用图片识别提取文字
        :return:
        """
        #先循环检测是否有亚马逊的邮件
        try:
            #先点击邮箱
            MouseToClick.click_img('./img/email.png')
        except:
            pass
        while 1:
            sleep(2)
            self.shezhi()
            MouseToClick.click_img('./img/shuaxin.png')
            try:
                MouseToClick.click_img('./img/new_email.png')
                sleep(3)
                break
            except:
                pass
        #获取小图
        filename = fetch_image()
        #提取文字
        text = png_2_text(filename)
        if text:
            try:
                url = 'https://www.amazon.co.uk/a/c/r?k='+text.split('k=')[1].strip()
                os.remove(filename)
                return url
            except:
                print('第一次提取失败，尝试重新提取url，请勿挡住或者关闭邮件窗口，url需要肉眼可见')
                GetWindowMsg('MainWindow', '网易邮箱大师')
                sleep(0.5)
                # 获取小图
                filename = fetch_image()
                # 提取文字
                text = png_2_text(filename)
                url = 'https://www.amazon.co.uk/a/c/r?k=' + text.split('k=')[1].strip()
                os.remove(filename)
                return url
        else:
            sleep(3)
            # 获取小图
            filename = fetch_image()
            # 提取文字
            text = png_2_text(filename)
            url = 'https://www.amazon.co.uk/a/c/r?k=' + text.split('k=')[1].strip()
            return url


def get_url(u, p):
    try:
        # 打开网易邮箱登录框，登录
        G = GetWindowMsg('LoginWindow', '网易邮箱大师')
        sleep(3)
        G.login3(u, p)  # 登录
    except:
        re_start_exe(email_exe_path)
        sleep(3)
        G = GetWindowMsg('LoginWindow', '网易邮箱大师')
        G.login3(u, p)  # 登录
    sleep(1)
    # 获取url地址
    G = GetWindowMsg('MainWindow', '网易邮箱大师')  # 获取数据与退出句柄不一样了
    url = G.get_url()


    # 退出网易邮箱登录

    G.login_out()
    return url

if __name__ == '__main__':
    u = 'yeshan87057pa@163.com'
    p = 'kejv0059'
    #打开网易邮箱登录框，登录
    G = GetWindowMsg('LoginWindow', '网易邮箱大师')
    sleep(4)
    G.login3(u, p)  # 登录
    #get_url(u, p)
    # re_start_exe(email_exe_path)
    # sleep(2)
    # G = GetWindowMsg('LoginWindow', '网易邮箱大师')

