import hashlib
import json
import os
import urllib.request
import datetime
import sys


__all__ = [
    'FILEHELPER_MARK', 'FILEHELPER',
    'is_json', 'md5_encode', '']

FILEHELPER_MARK = ['文件传输助手', 'filehelper']  # 文件传输助手标识
FILEHELPER = 'filehelper'


def is_json(resp):
    """
    判断数据是否能被 Json 化。 True 能，False 否。
    :param resp: request.
    :return: bool, True 数据可 Json 化；False 不能 JOSN 化。
    """
    try:
        json.loads(resp.text)
        return True
    except AttributeError as error:
        return False
    

def md5_encode(text):
    """ 把数据 md5 化 """
    if not isinstance(text, str):
        text = str(text)
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest().upper()


def _progress(block_num, block_size, total_size):
    """ 回调函数
       @block_num: 已经下载的数据块
       @block_size: 数据块的大小
       @total_size: 远程文件的大小
    """
    sys.stdout.write('\r>> Downloading file %.1f%%' % (
                     float(block_num * block_size) / float(total_size) * 100.0))
    sys.stdout.flush()


def save_pic(img_url, item_id):
    """
    :param img_url: 图片url
    :param item_id:  物料id，仅限用于图片命名
    :return: filename str, 返回一个图片名称，用来定位删除的。
    """
    try:
        file_suffix = os.path.splitext(img_url)[1]
        # print(file_suffix)
        # 拼接图片名（包含路径）
        filename = f'''tb_{datetime.datetime.now().strftime("%y%m%d-%H%M%S")}_{item_id}{file_suffix}'''
        # print(filename)
        # 下载图片，并保存到文件夹中
        urllib.request.urlretrieve(img_url, filename=filename)
        print(f'''图片下载成功：{filename}''')
        return filename
    except IOError as e:
        print(e)
        return
    except Exception as e:
        print(e)
        return


def del_pic(filename):
    os.remove(filename)
    

def short_2_long(short_url: str) -> str:
    """
    短址还原
    :param short_url: str 短址
    :return: str, 真实地址
    """
    req = urllib.request.Request(short_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
    response = urllib.request.urlopen(req)
    # 跳转后的真实下载链接
    return response.geturl()


if __name__ == '__main__':
    print(md5_encode("asd"))
