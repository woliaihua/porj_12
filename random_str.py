from random import Random
def get_ranrom_str(num):
    """
    生成随机字符串
    :param num: 字符串长度
    :return:
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(int(num)):
        str+=chars[random.randint(0,length)]
    #print(str)
    return str

def get_ranrom_pin(num):
    """
    生成随机字符串
    :param num: 字符串长度
    :return:
    """
    str = ''
    chars = '123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(int(num)):
        str+=chars[random.randint(0,length)]
    #print(str)
    return str

def get_ranrom_name(num):
    """
    生成随机字符串
    :param num: 字符串长度
    :return:
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    length = len(chars) - 1
    random = Random()
    for i in range(int(num)):
        str+=chars[random.randint(0,length)]
    #print(str)
    return str
if __name__ == '__main__':
    print(get_ranrom_name(7))