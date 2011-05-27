from webob.exc import HTTPFound

from repoze.bfg.url import model_url

from eportfolio.utils import authenticated_user
from eportfolio.views.api import TemplateAPI 
from eportfolio.interfaces import ITeacher

def application_view(context, request):
    
    user = authenticated_user(request)
    if user:
        if ITeacher.providedBy(user):
            return HTTPFound(location = model_url(context, request, 'dashboard.html'))
        return HTTPFound(location = model_url(user, request))
    
    return HTTPFound(location = model_url(context, request, 'login.html'))
    
def forbidden_view(context, request):
    
    return dict(api=TemplateAPI(request),
                referrer=request.referrer)