from repoze.bfg.security import authenticated_userid

from sqlalchemy.orm.exc import NoResultFound

from eportfolio.models import DBSession
from eportfolio.models import User

def authenticated_user(request):
    user_id = authenticated_userid(request)
    try:
        session = DBSession()
        user = session.query(User).filter_by(user_name=user_id).one()
        user.__parent__ = request.root['users']
        return user
    except NoResultFound:
        return None