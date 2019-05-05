# Python code to send mail
import email.utils
import smtplib
from email.mime.text import MIMEText
from propertyreader import Properties


properties = Properties()


def SendEmail(version, chost=None, shost=None):
    from_mail = properties.mymail.from_mail
    to_mail = properties.mymail.to_mail
    msg = MIMEText('Hello,'
                   '\n\nHere are the systems details for the week ..\n'
                   '\nSatellite Host => {}\n'
                   'Hosts which could use as content host => {}\n\n\n Thanks\nquicksystem '
                   'Tool.'.format(shost, chost))

    msg['To'] = email.utils.formataddr(('Recipient', to_mail))
    msg['From'] = email.utils.formataddr(('quicksystem', from_mail))
    msg['Subject'] = '[{}] Systems for Bugzilla verification and Automation testing'.format(
        version)

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(from_mail, to_mail, msg=msg.as_string())
    smtpObj.quit()
