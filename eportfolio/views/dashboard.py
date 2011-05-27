from zope.component import queryMultiAdapter

from webob.exc import HTTPFound

from repoze.bfg.url import model_url

from eportfolio.views.api import TemplateAPI

def dashboard_view(context, request):
    
    return dict(api=TemplateAPI(request))