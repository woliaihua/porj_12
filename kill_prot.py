import os

def get_prod_pid(prot):
    """
    根据端口号，获取对应的pid
    :return:
    """
    with os.popen('netstat -aon|findstr "{}"'.format(str(prot))) as res:
        res = res.read().split('\n')
    result = []
    for line in res:
        pid = line.split(' ')[-1]
        if pid:
            result.append(pid)
    return list(set(result))

def kill_pid(prot):
    """
    根据pid杀死对应的进程
    :param pids:
    :return:
    """
    pids = get_prod_pid(prot)
    for pid in pids:
        try:
            os.popen('taskkill /pid {} /f /t'.format(pid))
        except:
            pass

def kill_all_chorme():
    os.popen('taskkill /im chrome.exe /F')
    os.popen('taskkill /im chromedriver.exe /F')
if __name__ == '__main__':
    kill_all_chorme()