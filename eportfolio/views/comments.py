import datetime
import simplejson
from webob import Response

from repoze.bfg.url import model_url
from repoze.bfg.chameleon_zpt import render_template

from eportfolio.views.api import TemplateAPI
from eportfolio.utils import authenticated_user

from eportfolio.models import Comment

def comments_view(context, request):
    
    journal_entry = context.__parent__
    
    return render_template('templates/comments.pt',
                           api=TemplateAPI(request),
                           journal_entry=journal_entry,
                           number=journal_entry.comments.count(),
                           context=context)
                           
def comments_add_view(context, request):
    
    journal_entry = context.__parent__
    
    # Comment to add
    if request.POST.get('comment_text', None):
        comment = Comment()
        comment.journal_entry = journal_entry
        comment.user = authenticated_user(request)
        comment.text = request.POST['comment_text']
        comment.date = datetime.datetime.now()
        
    html = comments_view(context, request)
    response = simplejson.dumps(dict(id=model_url(context, request), html=html))
    
    return Response(response)