import requests

 
def servers_chick_ip(ip):
    proxies = {'http': 'http://{ip}'.format(ip=ip),
               'https': 'https://{ip}'.format(ip=ip)
               }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        p = requests.get('http://icanhazip.com', headers=headers, proxies=proxies, timeout=5)
        res = p.text
        if res.strip() in ip:
            print("后台检测ip{}可用".format(ip))
            return True
    except:
        print("后台检测ip{}不可用".format(ip))
if __name__ == '__main__':
    ip = '49.85.81.193:4257'
    servers_chick_ip(ip)
