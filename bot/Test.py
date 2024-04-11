import itchat


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    chat_rooms = itchat.get_chatrooms(update=True)
    for i in chat_rooms:
        print(i)
    