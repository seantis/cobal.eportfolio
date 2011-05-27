from zope.component import queryMultiAdapter

from webob.exc import HTTPFound

from repoze.bfg.url import model_url
from repoze.bfg.threadlocal import get_current_registry

from eportfolio.views.api import TemplateAPI
from eportfolio.views.interfaces import IGlobalMenuEntry
from eportfolio.utils import authenticated_user

def login_view(context, request):
    
    return dict(api=TemplateAPI(request))
    
def logged_in_view(context, request):
    
    user = authenticated_user(request)
    
    # Direct to the url of the "home" menu item which is user type specific.
    home_entry = get_current_registry().queryMultiAdapter((user, request), IGlobalMenuEntry, name="home")
    if home_entry:
        return HTTPFound(location = home_entry.url)
    else:
        return HTTPFound(location = model_url(context, request, 'login.html', query={'login_failed' : '1'}))