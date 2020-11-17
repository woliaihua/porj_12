
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
    获取需要 填写的文本信息
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
        for line in f.readlines():
            if line:
                try:
                    l =line.split('：')
                    dict1[l[0].strip()] = l[1].strip('\n')
                except:
                    pass
    return dict1

if __name__ == '__main__':
    filename = get_filename('.txt', 'template')
    print(get_temp_dict(filename))
    print(get_filename('.txt','template'))
    os.remove(filename)