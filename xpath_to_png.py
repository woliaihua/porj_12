from helium import *
from time import sleep
import cv2
import requests
from PIL import Image
from  io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains

"""
滑动图片验证
"""

class GetPng():
    def __init__(self,driver):
        self.driver = driver

    def get_position(self):
        """
        获取验证码位置,这里没有使用这个方式
        :return: 验证码位置元组
        """
        img = S('//*[@id="rc-imageselect"]').web_element
        #print('img')
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        print(top, bottom, left, right)
        return (top+10, bottom+10, left+286, right+286)



    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        screenshot.save('screen.png')
        return screenshot


    def get_geetest_image(self, name='./chaojiying_Python/captcha.png'):
        """
        获取验证码图片,大图切小图
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

if __name__ == '__main__':
    #HuaDong(driver).move_to_gap()
    def get_integral():
        """
        获取积分
        :return:
        """
        integral = S('//*[@id="app"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/a/span').web_element
        integral = integral.text
        print(integral)
        return int(integral)
    get_integral()