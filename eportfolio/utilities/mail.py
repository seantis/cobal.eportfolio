import email.MIMEText
import email.Header
import email.MIMEBase
import email.MIMEMultipart
from email import Encoders
from zope.interface import implements

from repoze.bfg.settings import get_settings
from repoze.bfg.threadlocal import get_current_registry

from repoze.sendmail.interfaces import IMailDelivery

from eportfolio.interfaces import IMailService

class MailService(object):
    
    implements(IMailService)

    def send(self, recipient, subject, body, attachments=[], sender=None):
        
        if not sender:
            settings = get_settings()
            sender = settings.get('from_mail_address')

        if attachments:
            msg = email.MIMEMultipart.MIMEMultipart()
            msg.attach(email.MIMEText.MIMEText(body.encode('UTF-8'), 'plain', 'UTF-8'))
        
            for name, fd in attachments:
                part = email.MIMEBase.MIMEBase('application', "octet-stream")
                part.set_payload(fd.read())
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 
                                'attachment; filename="%s"' % name)
                msg.attach(part)
        else:
            msg = email.MIMEText.MIMEText(body.encode('UTF-8'), 'plain', 'UTF-8')
    
        msg["From"] = sender
        msg["To"] = recipient.encode('utf-8')
        msg["Subject"] = email.Header.Header(subject.encode('UTF-8'), 'UTF-8')

        mailer = get_current_registry().getUtility(IMailDelivery)
        mailer.send(sender, [recipient.encode('UTF-8')], msg)