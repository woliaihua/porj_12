import win32api
import os
from time import sleep
"""
重新启动exe
"""

def start_exe(exe_path):
    """
    启动exe
    :param exe_path: 'F:\项目19-亚马逊卖家批量注册\非代码相关资料\验证器.exe'
    :return:
    """
    win32api.ShellExecute(0,'open',exe_path,'','',1)

def kill_exe(exe_name):
    """
    杀死进程
    :param exe_name:验证器.exe
    :return:
    """
    os.popen('taskkill /f /t /im '+exe_name)


def re_start_exe(exe_path):
    exe_name = exe_path.split('\\')[-1]
    kill_exe(exe_name)
    sleep(1)
    start_exe(exe_path)

if __name__ == '__main__':
    re_start_exe('F:\项目19-亚马逊卖家批量注册\非代码相关资料\验证器.exe')

