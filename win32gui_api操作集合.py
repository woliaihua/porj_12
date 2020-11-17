from win32gui  import *
import win32con
from mouseToClick import MouseToClick

import win32gui_struct
import win32api
import win32gui
import win32clipboard as w
from  time import sleep


class GetWindowMsg():
    def __init__(self,window_name):
        self.window_name = window_name
        self.handle = FindWindow(None,window_name)#获取窗口句柄
        SetForegroundWindow(self.handle)#设置窗口前台
        ShowWindow(self.handle,1)#显示窗口
        self.title = GetWindowText(self.handle)#获取窗口标题
        #print(self.title)

    @staticmethod
    def print_hwnd_title():
        """
        获取电脑种所有启动程序的窗口的句柄与标题
        :return:
        """
        hwnd_title = dict()
        def get_all_hwnd(hwnd,msg):
            if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
                hwnd_title.update({hwnd:GetWindowText(hwnd)})
        EnumWindows(get_all_hwnd,0)
        for h ,t in hwnd_title.items():
            if t is not '':
                print(h, t)

    def get_focus(self):
        """
        获取光标处的文本句柄
        :return:
        """
        hWnd = GetFocus()
        print('hWnd: ',hWnd)
        return hWnd

    def get_menu_item_txt(self,menu,idx):
        """
        获取当前句柄窗口所有子窗口的句柄与名字
        :param menu:
        :param idx:
        :return:
        """

        mii, extra = win32gui_struct.EmptyMENUITEMINFO()  # 新建一个win32gui的空的结构体mii
        GetMenuItemInfo(menu, idx, True, mii)  # 将子菜单内容获取到mii
        ftype, fstate, wid, hsubmenu, hbmpchecked, hbmpunchecked, \
        dwitemdata, text, hbmpitem = win32gui_struct.UnpackMENUITEMINFO(mii)  # 解包mii
        return text
        #
        # for i in range(9):
        #     print (get_menu_item_txt(menu,i))
    def get_son_handle(self,handle):
        """
        # 搜索子窗口
        # 枚举子窗口
        #获取某个菜单的内容
        #大概意思就是这个函数返回的是一个结构体，要用他提供的方法来获得这个结构体，然后在解包这个结构体就能获得标题了
        :return:
        """
        hwndChildList = []
        EnumChildWindows(handle, lambda hwnd, param: param.append(hwnd), hwndChildList)

        print(hwndChildList)
        for son_handle in hwndChildList:
            title = GetWindowText(son_handle)
            clsname = GetClassName(son_handle)
            #win32gui.PostMessage(son_handle, win32con.BM_CLICK, 0, 0) #点击
            print(son_handle,title,clsname)
            # if title == '伙伴ID':
            #     win32gui.PostMessage(son_handle, win32con.BM_CLICK, 0, 0) #点击
            #     break

    def get_length(self,edtextHand):
        """
        #获取文本框的长度
        :param edtextHand:
        :return:
        """
        length = SendMessage(edtextHand,win32con.WM_GETTEXTLENGTH)+1
        print("length:",length)
        return length

    def get_txt_content(self,edtextHand):
        """
        获取文本框内容
        :param edtextHand:
        :return:
        """
        pass

    #鼠标后台点击
    def doClick(self,x=106, y=256):
        long_position = win32api.MAKELONG(x, y)  # 模拟鼠标指针 传送到指定坐标
        sleep(0.05)
        back1 = win32api.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
        sleep(0.05)
        back2 = win32api.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起
        sleep(0.05)
class OperWindow(GetWindowMsg):
    def __init__(self,window_name):
        super().__init__(window_name)

def send_input_msg(name_list):
    """
    给桌面程序的文本框种输入内容，使用还是图片识别技术
    :param name_list:
    :return:
    """
    welink = OperWindow('网易邮箱大师') #打开窗口
    sleep(0.5)
    #点击创建群里图片
    # MouseToClick.click('建群图标.png')
    # #循环输入拉群的人员名单
    # for name in name_list:
    #     #打开剪贴板
    #     w.OpenClipboard()
    #     #清空剪切版
    #     w.EmptyClipboard()
    #     #设置剪贴版内容
    #     w.SetClipboardData(win32con.CF_UNICODETEXT,name)
    #     #点击输入框,先截图
    #     MouseToClick.screenshot()
    #     result = MouseToClick.matchImg('输入框.png')
    #     if result:
    #         MouseToClick.matchImg('输入框.png')
    #     else:
    #         OperWindow('选择联系人或添加电话号码')
    #         #点击输入框
    #         MouseToClick.matchImg('输入框.png')
    #     #清空输入框
    #     for i in range(20):
    #         sleep(0.04)
    #         MouseToClick.oneKey('BACKSPACE')
    #     #模拟键盘操作ctrl+v
    #     MouseToClick.twoKey('CTRL','V')
    #     sleep(1)
    #     MouseToClick.oneKey('ENTER')
    # #点击确定图片
    # result2 = MouseToClick.click('确定.png')
    # if result2:
    #     MouseToClick.click('确定.png')
    # else:
    #     OperWindow("这是另一个窗口的标题")
    #     MouseToClick.click('确定.png')

if __name__ == '__main__':
    welink = OperWindow('网易邮箱大师')  # 打开窗口
    welink.get_son_handle(657488)