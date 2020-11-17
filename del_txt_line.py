
import os
from time import sleep
def del_line(name,filename):
    """
    用一条删除一条支持多进程
    :param name:
    :return:
    """
    try:
        lines = (i for i in open(filename, 'r', encoding="utf-8") if name not in i )
        with open('test_new.txt', 'w', encoding="utf-8") as f:
            f.writelines(lines)
        os.rename(filename, 'test.bak')
        os.rename('test_new.txt', filename)
        os.remove('test.bak')

    except Exception(PermissionError) as e:
        sleep(0.05)
        del_line(name,filename)





if __name__ == '__main__':
    # del_line('117.57.62.236','ip.txt')\
    print(get_ip())