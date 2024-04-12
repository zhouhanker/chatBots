import time
import platform
import os
import re
import random
import itchat
from itchat.content import (
    TEXT,
    FRIENDS,
    NOTE,
    PICTURE
)

from collections import OrderedDict
from utils import config
from utils import common
from bot import itchatHelp

# 群信息字典
group_infos_dict = OrderedDict()


def is_online(auto_login=False):
    """
    判断是否还在线。
    :param auto_login: bool,当为 Ture 则自动重连(默认为 False)。
    :return: bool,当返回为 True 时，在线；False 已断开连接。
    """

    def _online():
        """
        通过获取好友信息，判断用户是否还在线。
        :return: bool,当返回为 True 时，在线；False 已断开连接。
        """
        try:
            if itchat.search_friends():
                return True
        except IndexError:
            return False
        return True

    if _online():
        # 如果在线，则直接返回 True
        return True
    if not auto_login:  # 不自动登录，则直接返回 False
        print('微信已离线..')
        return False

    hot_reload = False
    login_callback = init_data
    exit_callback = exit_msg
    try:
        for _ in range(2):  # 尝试登录 2 次。
            if platform.system() in ('Windows', 'Darwin'):
                itchat.auto_login(hotReload=hot_reload,
                                  loginCallback=login_callback, exitCallback=exit_callback)
                itchat.run(blockThread=True)
            else:
                # 命令行显示登录二维码。
                itchat.auto_login(enableCmdQR=2, hotReload=hot_reload, loginCallback=login_callback,
                                  exitCallback=exit_callback)
                itchat.run(blockThread=True)
            if _online():
                print('登录成功')
                return True
    except Exception as exception:  # 登录失败的错误处理。
        sex = str(exception)
        if sex == "'User'":
            print('此微信号不能登录网页版微信，不能运行此项目。没有任何其它解决办法！可以换个号再试试。')
        else:
            print(sex)

    delete_cache()  # 清理缓存数据
    print('登录失败。')
    return False


def delete_cache():
    """ 清除缓存数据，避免下次切换账号时出现 """
    file_names = ('QR.png', 'itchat.pkl')
    for file_name in file_names:
        if os.path.exists(file_name):
            os.remove(file_name)

      
def init_chats_room(group_name_list):

    uid_list_compile = re.compile(
        r"(?<!'Self': )\<ChatroomMember:.*?'UserName': '(.*?)', 'NickName'.*?")  # 筛选出群所有用户的 uid
    for group_name in group_name_list:
        group_list = itchat.search_chatrooms(name=group_name)  # 通过群聊名获取群聊信息
        group_info = {}
        if group_list:
            group_uuid = group_list[0]['UserName']
            group = itchat.update_chatroom(group_uuid, detailedMember=True)  # 通过群id更新群名单
            group_uuid = group['UserName']  # 群聊 id
            group_info['group_name'] = group_name  # 群聊名称
            group_info['group_uuid'] = group_uuid  # 群聊 uuid
            count = len(group['MemberList'])  # 群聊人数
            group_info['count'] = count
            member_uid_list = uid_list_compile.findall(str(group))  # 根据正则取出群组里所有用户的 uuid。也可以用循环的方式。
            if member_uid_list:
                group_info['member_uid_list'] = member_uid_list
            group_infos_dict[group_uuid] = group_info
            print("init_chats_room Method Exec -> Group_Info:", group_info)
            print("init_chats_room Method Exec -> Group_Infos_Dict", group_infos_dict)
            
            
def init_data():
    """ 初始化微信所需数据 """
    set_system_notice('登录成功')
    # 更新好友数据
    itchat.get_friends(update=True)
    # 更新群聊数据
    itchat.get_chatrooms(update=True)

    conf = config.get_config('group_helper_conf')
    group_name_list = conf.get('group_name_white_list')

    init_chats_room(group_name_list)
    # 初始化所有配置内容
    itchatHelp.init_wechat_config()
    # init_alarm()

    print('初始化完成，开始正常工作。')
    
    
def exit_msg():
    """ 退出通知 """
    print('程序已退出')
    
    
def set_system_notice(text):
    """
    给文件传输助手发送系统日志。
    :param text:str 日志内容
    """
    if text:
        text = '系统通知：' + text
        itchat.send(text, toUserName=common.FILEHELPER)


def run():
    """ 主运行入口 """
    conf = config.init()
    # conf = get_yaml()
    if not conf:  # 如果 conf，表示配置文件出错。
        print('程序中止...')
        return
    # 判断是否登录，如果没有登录则自动登录，返回 False 表示登录失败
    print('开始登录...')
    if not is_online(auto_login=True):
        print('程序已退出...')
        return
    
    
if __name__ == '__main__':
    run()