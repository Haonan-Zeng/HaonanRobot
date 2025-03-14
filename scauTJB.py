from requests import request
from urllib.parse import quote
from json import loads
from ast import literal_eval
from pandas import DataFrame,options
options.mode.chained_assignment=None
from time import sleep
# from datetime import datetime
# import schedule

def tjbfeild(dayadd,TimePeriod,begintime_num,fieldnum,target_email):

    # URL解码
    # url_decoded = unquote(url_encoded)
    # _=9999999999999
    # begintime_num={8:1,9:1}

    headers = {
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Linux; Android 15; FLC-AN00 Build/HONORFLC-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.103 Mobile Safari/537.36 XWEB/1300149 MMWEBSDK/20240802 MMWEBID/3750 MicroMessenger/8.0.53.2740(0x2800353F) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
    'Accept':'*/*',
    'X-Requested-With':'XMLHttpRequest',
    'Referer':'http://gzagwx.wxlgzh.com/Views/Field/FieldOrder.html?VenueNo=07&FieldTypeNo=11',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie':f'OpenId={OpenId}'}
    payload=None

    while begintime_num!={}:
        # response0 = request("GET", f"http://gzagwx.wxlgzh.com/Field/GetVenueState?dateadd={dayadd}&TimePeriod=0&VenueNo=07&FieldTypeNo=11&_={_}", headers=headers, data=payload)
        try:
            response0 = request("GET", f"http://gzagwx.wxlgzh.com/Field/GetVenueState?dateadd={dayadd}&TimePeriod={TimePeriod}&VenueNo=07&FieldTypeNo=11", headers=headers, data=payload)
        except:
            sleep(10)
            continue
        data = DataFrame(literal_eval(loads(response0.text)['resultdata']))
        free_field = data.query('FieldState=="0"')
        if free_field.shape[0]>0:
            free_field['BeginTime'] = free_field['BeginTime'].str.replace(':00','').astype('int')
            free_field['FieldName_Change'] = free_field['FieldName'].str.replace('[羽毛球号场]+','',regex=True).astype('int')

            bt = list(begintime_num.keys())
            for i in bt:
                # i=18
                num = begintime_num[i]
                free_field_fit = free_field.query('BeginTime==@i and FieldName_Change.isin(@fieldnum)').iloc[:num,:]
                if free_field_fit.shape[0]>0:
                    for j in range(free_field_fit.shape[0]):
                        # j=0
                        [FieldNo,FieldName,BeginTime] = free_field_fit.reset_index().loc[j,['FieldNo','FieldName','BeginTime']]
                        # URL编码
                        url_encoded = quote('[{"FieldNo":"'+FieldNo+'", "FieldTypeNo":"11", "FieldName":"'+FieldName+'", "BeginTime":"'+str(BeginTime)+':00", "Endtime":"'+str(BeginTime+1)+':00", "Price":"20.00"}]')
                        try:
                            response1 = request("GET", f"http://gzagwx.wxlgzh.com/Field/OrderField?checkdata={url_encoded}&dateadd={dayadd}&VenueNo=07", headers=headers, data=payload)
                        except:
                            sleep(1)
                            continue
                        print(response1.text)
                        if response1.status_code==200 and loads(response1.text)["message"]!="预订异常，请重试":
                            print(f'@@@Finish Feild***BeginTime:{i}!!!')
                            mailto(target_email, f'BeginTime:{i}!!!')
                            begintime_num[i] = begintime_num[i]-1
                            if begintime_num[i]==0:
                                del begintime_num[i]
        if begintime_num=={}:
            break
        sleep(10)

def mailto(target_email, text):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    # 邮件服务器地址和端口
    smtp_server ='smtp.qq.com'
    smtp_port = 587

    # 发件人邮箱和密码
    sender_email = '3226133844@qq.com'
    sender_password = 'dgxrrfiuyvvrdadj'

    # 收件人邮箱
    receiver_email = target_email

    # 邮件主题和内容
    subject = 'Haonan-TJB场地代抢成功'
    body = '请尽快支付场地费-{}'.format(text)

    # 创建MIMEText对象
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = Header("lonelygod <{}>".format(sender_email))
    msg['To'] = Header(receiver_email, 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启动TLS加密
        server.login(sender_email, sender_password)

        # 发送邮件
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print(f'邮件发送失败: {e}')
    finally:
        server.quit()

if __name__ == '__main__':

    cmd=input('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@***HAONAN TJB PROGRAM 20 Dec 2024***@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\nPlease Input Command:\n1#20:1,21:1#1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22#o_xxx#xxx@qq.com\n')
    
    # haonanCMD
    # cmd='7#20:1,21:1#1,2,3,4,5,6,7,8,9,10,11,12,13,15,17,18,20,22#o_DYGt9-Zdv4S5m_MDhJCTH6bLXc#844047017@qq.com'

    # wjCMD
    # cmd='2#20:1#1#o_DYGtwBUQwDNt0TgEDLVmhtz28o#806016719@qq.com'
    
    dayadd=cmd.split('#')[0] #几天后
    begintime_num=eval('{'+cmd.split('#')[1]+'}') #上午0,下午1,晚上2
    begintimelist=list(begintime_num.keys())
    if (min(begintimelist)>=8 and max(begintimelist)<=11):
        TimePeriod=0
    elif (min(begintimelist)>=12 and max(begintimelist)<=17):
        TimePeriod=1
    elif (min(begintimelist)>=18 and max(begintimelist)<=21):
        TimePeriod=2
    else:
        print("!!!BeginTime Error!!!")

    fieldnum=eval('['+cmd.split('#')[2]+']')
    OpenId=cmd.split('#')[3]
    target_email=cmd.split('#')[4]

    # dayadd=6 #几天后
    # TimePeriod=2 #上午0,下午1, 晚上2
    # begintime_num={20:1,21:1} #上午0,下午1, 晚上2
    # fieldnum=[1,2,3,4,5,6,7,8,9,10]
    # OpenId='o_DYGt9-Zdv4S5m_MDhJCTH6bLXc'

    tjbfeild(dayadd,TimePeriod,begintime_num,fieldnum,target_email)

    input('Enter to Close')

    # schedule.every().day.at("12:00").do(tjbfeild(dayadd,TimePeriod,begintime_num,fieldnum))

    # while True:
    #     schedule.run_pending()
    #     sleep(1)
