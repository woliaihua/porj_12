import requests
from PIL import Image
from io import BytesIO


def get_src_img(imge_url, filename):
    """
    使用img_url 来获取图片
    :return:
    """
    response = requests.get(imge_url, timeout=180).content
    img_content = BytesIO(response)
    image2 = Image.open(img_content)
    image2.save(filename)
    return filename


if __name__ == '__main__':
    get_src_img(
        'https://www.google.com/recaptcha/api2/payload?p=06AGdBq26JbQdro-34SAf8I9p10kEXu717R5wX21ZRrhthCyH9T4NyUPoVprA-JNZRwyrKNgmsfwj01ECsmnhLB3Omy-Ta18ppuGI1kAstY1Lk1p-umPT5Gtu8lVg8643Av9vwuV8z4ulyJzrvRUqlt-E4A3iP4FaFDEvHEz_8opz80XHqLugqhYmK_rxpNlZ5dW-8QvP76Hj3HuSq3SA9En-tBgKwI2JLKw&k=6LcIKDUUAAAAAKCjYcEFzq5UT8gTZJNIB6He5Dnm',
        '444.png')
