from webob import Response
from z3c.rml.rml2pdf import parseString

from eportfolio.views.api import TemplateAPI 
from repoze.bfg.chameleon_zpt import render_template


def objectives_view(context, request):
    
    project = context.__parent__     
    
    return dict(api = TemplateAPI(request),
                project = project) 
                
def objectives_pdf_view(context, request):

    project = context.__parent__     

    result =  render_template('templates/objectives_pdf.pt',
               api=TemplateAPI(request),
               project = project)
     
    response = Response(parseString(result.encode('utf-8')).read())
    response.content_type =  "application/pdf"
    return response