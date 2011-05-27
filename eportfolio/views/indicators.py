from eportfolio.views.api import TemplateAPI

def indicators_view(context, request):
    
    indicators = context.indicators
    
    return dict(api=TemplateAPI(request),
                competence=context,
                indicators=indicators)
                