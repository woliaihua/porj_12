
import chardet
import os


def get_filename(endswith, filename):
    """

    :param endswith: 文件结尾
    :param filename:  文件名包含filename
    :return:
    """
    for dirpath, dirnames, filenames in os.walk('./template'):
        for f in filenames:
            fpath = os.path.join(dirpath, f)
            if os.path.isfile(fpath):
                if fpath.endswith(endswith) and filename in f:
                    return os.path.join(dirpath, f)

def get_temp_dict(filename):
    """
    获取个人信息文本信息
    :return: 字典
    """
    def get_file_code(filename):
        f3 = open(filename, 'rb')
        data = f3.read()
        encode = chardet.detect(data).get('encoding')
        f3.close()
        return encode
    dict1 = {}
    with open(filename,'r',encoding=get_file_code(filename)) as f:
        for index,line in enumerate(f.readlines()):
            if index==0:
                continue
            else:
                try:
                    l = line.split('----')
                    if len(l) != 13:
                        print(filename + "第{}行格式不对，跳过此行".format(index + 1))
                        continue
                    dict1['First 名字'] = l[0].strip().strip('\n')
                    dict1['last 姓'] = l[1].strip().strip('\n')
                    dict1['个人地址'] = l[2].strip().strip('\n')
                    dict1['个人市'] = l[3].strip().strip('\n')
                    dict1['个人邮编'] = l[4].strip().strip('\n')
                    dict1['SSN'] = l[5].strip().strip('\n')
                    dict1['生日'] = l[6].strip().strip('\n')
                    dict1['驾照号'] = l[7].strip().strip('\n')
                    dict1['公司名字'] = l[8].strip().strip('\n')
                    dict1['公司地址'] = l[9].strip().strip('\n')
                    dict1['公司市'] = l[10].strip().strip('\n')
                    dict1['公司邮编'] = l[11].strip().strip('\n')
                    dict1['公司电话'] = l[12].strip().strip('\n')
                    break
                except:
                    print(filename+"第{}行格式不对，跳过此行".format(index+1))
    if dict1:
        return dict1
    else:
        print(filename+'所有数据格式都不正确，无法取到正确的数据，请检查')
def get_phone_dict(filename):
    """
    获取个人信息文本信息
    :return: 字典
    """
    def get_file_code(filename):
        f3 = open(filename, 'rb')
        data = f3.read()
        encode = chardet.detect(data).get('encoding')
        f3.close()
        return encode
    dict1 = {}
    with open(filename,'r',encoding=get_file_code(filename)) as f:
        for index,line in enumerate(f.readlines()):
            try:
                dict1['电话'] = line.strip().strip('\n')
                break
            except:
                print(filename+"第{}行格式不对，跳过此行".format(index+1))
    return dict1
def get_email_dict(filename):
    """
    获取个人信息文本信息
    :return: 字典
    """
    def get_file_code(filename):
        f3 = open(filename, 'rb')
        data = f3.read()
        encode = chardet.detect(data).get('encoding')
        f3.close()
        return encode
    dict1 = {}
    with open(filename,'r',encoding=get_file_code(filename)) as f:
        for index,line in enumerate(f.readlines()):
            try:
                l = line.split('----')
                dict1['邮箱地址'] = l[0].strip().strip('\n')
                dict1['邮箱密码'] = l[1].strip().strip('\n')
                break
            except:
                print(filename+"第{}行格式不对，跳过此行".format(index+1))
    return dict1
if __name__ == '__main__':
    filename = get_filename('.txt', '个人信息')
    print(get_temp_dict(filename))
    # print(get_filename('.txt','template'))
    # os.remove(filename)