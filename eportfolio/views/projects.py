import datetime 

from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import Project  

def projects_view(context, request):
      
    session = DBSession()
    projects = session.query(Project)
    today = datetime.date.today()
    
    # Projects need to be traversal wrapped to make the links work.
    current_projects = []
    for project in projects.filter(Project.end_date >= today).order_by(Project.end_date.desc()):
        current_projects.append(context[project.id])
        
    past_projects = []
    for project in projects.filter(Project.end_date < today).order_by(Project.end_date.desc()):
        past_projects.append(context[project.id])
    
    api = TemplateAPI(request)
    return dict(context=context, api=api,current_projects=current_projects,past_projects=past_projects)