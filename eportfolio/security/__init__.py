from eportfolio.models import DBSession
from eportfolio.models import User

def groupfinder(identity, request):
    groups = []
    user_id = identity['repoze.who.userid'].decode('UTF-8')
    session = DBSession()
    user = session.query(User).filter_by(email = user_id).first()
    if user:
        groups.extend(user.groups)
    
    return groups