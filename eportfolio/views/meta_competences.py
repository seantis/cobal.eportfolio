from eportfolio.views.api import TemplateAPI

def meta_competences_view(context, request):
    
    return dict(api = TemplateAPI(request),
                meta_competences = context)