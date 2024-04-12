import asyncio
import random

import itchat
from utils import TextCheckUtils
from utils import logUtils


# @itchat.msg_register('Text', isGroupChat=True)
# def text_reply(msg):
#     print(msg['Text'])
#     black_text = TextCheckUtils.check_black_text(msg['Text'])
#     if black_text is not None:
#         return f'注意文明用语, 警告一次,三次移除 敏感词: {black_text}'
#
#
# itchat.auto_login(hotReload=True)
# itchat.run()

if __name__ == '__main__':
	print(logUtils.log_warn_group_prefix())
	

