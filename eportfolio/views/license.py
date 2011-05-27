from webob import Response

from eportfolio.views.api import TemplateAPI

def license_view(context, request):
    
    return dict(api=TemplateAPI(request),)