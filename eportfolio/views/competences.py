from eportfolio.views.api import TemplateAPI

def competences_view(context, request):
    
    return dict(api=TemplateAPI(request))
    