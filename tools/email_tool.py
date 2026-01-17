# 1 导入模块
import smtplib
from email.mime.text import MIMEText  # 往邮件中写内容的对象

from email.utils import formataddr  # 发件人信息

from mima import EmailConfig


def send_email(subject: str, content: str, receivers: list, cc: list = None, bcc: list = None):
    s = smtplib.SMTP_SSL(EmailConfig.HOST, EmailConfig.PORT)
    s.login(EmailConfig.ADDR, EmailConfig.PWD)

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = formataddr((EmailConfig.ADDR, EmailConfig.ADDR))
    msg['To'] = ','.join(receivers)

    all_receivers = [x for x in receivers]
    if cc:
        all_receivers.extend(cc)
        msg['Cc'] = ','.join(cc)
    if bcc:
        all_receivers.extend(bcc)
        msg['Bcc'] = ','.join(bcc)

    all_receivers = list(set(all_receivers))

    s.sendmail(EmailConfig.ADDR, all_receivers, msg.as_string())
    s.quit()


if __name__ == '__main__':
    pass
    send_email('测试', '<H1>张新波</H1>', ['zxb1727@qq.com'])
