import logging

from repoze.bfg.settings import get_settings

from repoze.sendmail.delivery import QueuedMailDelivery
from repoze.sendmail.mailer import SMTPMailer
from repoze.sendmail.queue import QueueProcessor

settings = get_settings()
hostname = settings.get('mail_hostname', 'localhost')
port = settings.get('mail_port', 25)
username = settings.get('mail_username', None)
password = settings.get('mail_password', None)
no_tls = settings.get('mail_no_tls', None)
force_tls = settings.get('mail_force_tls', None)
mailer = SMTPMailer(hostname, port, username, password, no_tls, force_tls)

queue_path = settings.get('mail_queue_path', 'maildir')
queued_mail_delivery = QueuedMailDelivery(queue_path)

log = logging.getLogger('eportfolio')

qp = QueueProcessor(mailer, queue_path)
qp.log = log

def trigger_queued_delivery():
    try:
        qp.send_messages()
    except Exception, e:
        log.error(e)