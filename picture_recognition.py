# coding=utf-8
import aircv as ac
from PIL import ImageGrab
import os

class CustomError(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo

class PictureRecognition(object):
    #截取整个屏幕
    @classmethod
    def screenshot(cls):
        filename = 'screen.png'
        im = ImageGrab.grab()
        im.save(filename)

    #获取对应的图片的坐标点
    @classmethod
    def matchImg(cls,imgobj, imgsrc='screen.png', confidence=0.5):
        imsrc = ac.imread(imgsrc)
        imobj = ac.imread(imgobj)
        match_result = ac.find_template(imsrc,imobj,confidence)
        os.remove(imgsrc)
        #match_result为None或不为None时满足自定义条件
        if not match_result or match_result and match_result['confidence']<0.8:
            imgobj_name = imgobj.split('data/image/')[1]
            raise CustomError(imgobj_name+'图片识别失败')
        else:
            x = match_result['result'][0]
            y = match_result['result'][1]
            #当前 x y 为识别图片的中心点，可以进行直接点击
            return x,y