# --coding:utf-8--
import settings
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from common.log_utils import getLogger
log = getLogger('send_mail.py')


def email(email_list, content, subject, sender):  # email_list邮件列表，content邮件内容，subject：发送标题
    '''
    :param email_list: 收件人，list ['rs.yan@idiaoyan.com', 'rex_yan@126.com', '1572402228@qq.com']
    :param content:  邮件内容，str
    :param subject:  邮件主题 str
    :param sender:   发件人 list ["kinlde15推送", 'push@kindle15.com']
    :return:
    '''
    subject = subject
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(sender)
    msg['Subject'] = subject
    server = smtplib.SMTP(settings.SMTP_ADD, settings.SMTP_PORT)
    server.login(settings.SMTP_USER, settings.SMTP_PASS)  # 邮箱名，密码
    server.sendmail('push@kindle15.com', email_list, msg.as_string())
    server.quit()
    log.debug(u'普通邮件发送成功', email_list, content, subject, sender)


def email_att(email_list, content, subject, sender, file_path, file_name):
    '''
    :param email_list: 收件人，list ['rs.yan@idiaoyan.com', 'rex_yan@126.com', '1572402228@qq.com']
    :param content: 邮件内容，str
    :param subject: 邮件主题 str
    :param sender:  发件人 list ["kinlde15推送", 'push@kindle15.com']
    :param file_path: 附件路径 str
    :param file_name: 附件名称 str
    :return:
    '''
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header
    sender = sender
    email_list = email_list  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = formataddr(sender)
    message['Subject'] = subject
    # 邮件正文内容
    message.attach(MIMEText(content, 'plain', 'utf-8'))
    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename=' + file_name
    message.attach(att1)
    # 构造附件2，传送当前目录下的 runoob.txt 文件
    # att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
    # att2["Content-Type"] = 'application/octet-stream'
    # att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
    # message.attach(att2)
    try:
        server = smtplib.SMTP(settings.SMTP_ADD, settings.SMTP_PORT)
        server.login(settings.SMTP_USER, settings.SMTP_PASS)  # 邮箱名，密码
        server.sendmail('push@kindle15.com', email_list, message.as_string())
        log.debug(u'附件邮件发送成功', email_list, content, subject, sender)
    except smtplib.SMTPException:
        log.debug(u'附件邮件发送失败', email_list, content, subject, sender)


if __name__ == '__main__':
    #email(['rs.yan@idiaoyan.com', 'rex_yan@126.com', '1572402228@qq.com'], u'邮件推送测试', u"邮件主题" ,["kinlde15推送", 'push@kindle15.com'])
    email_att(['rs.yan@idiaoyan.com', 'rex_yan@126.com', '1572402228@qq.com'], u'邮件推送测试', u"邮件主题" ,[u"kinlde15推送", u'push@kindle15.com'], './Monaco.TTF', 'Monaco.TTF')
    print u'ok'