# Python code to send mail
import email.utils
import smtplib
from email.mime.text import MIMEText
from propertyreader import Properties


properties = Properties()


def SendEmail(version, chost=None, shost=None):
    login_username = properties.mymail.login_mailid
    login_password = properties.mymail.login_password
    to_mail = properties.mymail.to_mail
    msg = MIMEText('Hello Folks,'
                   '\n\nHere are the systems details for the week ..\n'
                   '\nSatellite Host => {}\n'
                   'Content Host => {}\n\n\n Thanks\nquicksystem Tool.'.format(shost, chost))

    msg['To'] = email.utils.formataddr(('Recipient', to_mail))
    msg['From'] = email.utils.formataddr(('Author', login_username))
    msg['Subject'] = '[{}] Systems for Bugzilla verification and Automation testing'.format(
        version)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(login_username, login_password)
    s.sendmail(from_addr=login_username, to_addrs=to_mail, msg=msg.as_string())
    s.quit()
