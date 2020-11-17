import requests
from PIL import Image
from  io import BytesIO

def get_src_img(imge_url, filename):
    """
    使用img_url 来获取图片
    :return:
    """
    response = requests.get(imge_url,timeout=180).content
    img_content = BytesIO(response)
    image2 = Image.open(img_content)
    image2.save(filename)
    return filename