from telegram.client import Telegram
import re,time
an=[1] #账号数量
# 如有两个账号，则an=[1，2]，以此类推，并在下方填入多账号信息
for accn in an:
    if accn == 1: # 第一个账号
        tg = Telegram(
            api_id='your api id', # 填入api id
            api_hash='your api hash', # 填入 api hash
            phone='your phone number', # Telegram账号
            database_encryption_key='passw0rd!',
            files_directory="/home/your_login_name/emby-server-checkin-bot/sessions", # 修改储存session文件位置，防止重启后session失效
            library_path='/home/your_login_name/emby-server-checkin-bot/libtdjson.so', # 填入libtdjson.so的绝对路径
        )
    # #多账号支持
    # if accn == 2:
    #     tg = Telegram(
    #         api_id='your api id', # 填入api id
    #         api_hash='your api hash', # 填入 api hash
    #         phone='your phone number', # Telegram账号
    #         database_encryption_key='passw0rd!',
    #         files_directory="/home/your_login_name/emby-server-checkin-bot/sessions", # 修改储存session文件位置，防止重启后session失效
    #         library_path='/home/your_login_name/emby-server-checkin-bot/libtdjson.so', # 填入libtdjson.so的绝对路径
    #     )

    tg.login()
    # chat id
    # 厂妹 1429576125
    # 卷毛鼠活动机器人 1260610044

    def send_verification_code(update):
        # 所有的新消息都会被监听，增加判断只监听自己感兴趣的
        if 1260610044 == update['message']['chat_id']:
            # print(update)
            # 提取问题并且计算
            question = update['message']['content']['text']['text']
            print(question)
            numtocal=re.findall(r"-?[0-999]\d*",question)
            if len(numtocal) > 1:
                a=numtocal[0]
                b=numtocal[1]
            else:
                a=''
                b=''
            cr=re.findall(r"[‘加’‘减’‘乘’‘除’]", question)
            if a and b and cr:
                print(a, b, cr)
                #c = int(a[-1].strip()) + int(b[-1].strip())
                if cr == ['加']:
                    c = int(a.strip()) + int(b.strip())
                if cr == ['减']:
                    c = int(a.strip()) - int(b.strip())
                if cr == ['乘']:
                    c = int(a.strip()) * int(b.strip())
                if cr == ['除']:
                    c = int(a.strip()) / int(b.strip())
                answers = update['message']['reply_markup']['rows'][0]
                print(f'{a} {cr[-1].strip()} {b} = {c}')
                # 用答案和内联键盘值做匹配，一旦匹配执行按钮点击效果
                for answer in answers:
                    #print(f'答案：{answer["text"]}')
                    if int(answer['text']) == c:
                        payload = {
                            '@type': 'callbackQueryPayloadData',
                            'data': answer['type']['data'],  ##每一个内联键盘都带有data数据
                        }
                        # 发送答案（点击内联键盘）
                        result = tg.call_method(method_name='getCallbackQueryAnswer',
                                                params={'chat_id': update['message']['chat_id'],
                                                        'message_id': update['message']['id'], 'payload': payload})
                        result.wait()
                        if result.error:
                            print(f'getCallbackQueryAnswer error: {result.error_info}')
                        else:
                            print(f'getCallbackQueryAnswer: {result.update}')
                        break
    tg.add_update_handler('updateNewMessage', send_verification_code)                   
    result = tg.get_chats()
    result.wait()
    result=tg.send_message(
            chat_id=1260610044,
            text="/checkin", # 发送签到指令
        )
    result.wait()
    time.sleep(10) # 等待15秒签到完毕后退出程序
    tg.stop()  