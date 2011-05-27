from qc.statusmessage.message import Message

def show(request, msg, msg_type=u'notice'):
    msg = Message(msg, msg_type=msg_type)
    # WSGI pipeline thus not present in tests
    if 'qc.statusmessage' in request.environ:
        request.environ['qc.statusmessage'].append(msg)