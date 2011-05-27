import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url

from eportfolio.interfaces import IProject, ITeacher
from eportfolio.utils import authenticated_user

from eportfolio.views.competence_cloud import project_competence_cloud_view
from eportfolio.views.comments import comments_view
from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import Project

class ProjectSchema(formencode.Schema):
    allow_extra_fields = True
    title = formencode.validators.UnicodeString(not_empty=True, max=255)
    number = formencode.validators.UnicodeString()
    start_date = formencode.validators.DateConverter(month_style='dd/mm/yyyy', not_empty=True)
    end_date = formencode.validators.DateConverter(month_style='dd/mm/yyyy', not_empty=True)
    description = formencode.validators.UnicodeString()
    customer_request = formencode.validators.UnicodeString()
    customer_benefit = formencode.validators.UnicodeString()
    customer_outcome = formencode.validators.UnicodeString()
    budget = formencode.validators.Int()
    risks = formencode.validators.UnicodeString()
    preconditions = formencode.validators.UnicodeString()
    environment = formencode.validators.UnicodeString()
    exclusions = formencode.validators.UnicodeString()
    
project_schema = ProjectSchema()

def project_edit_view(context, request):
    
    if IProject.providedBy(context):
        project = context
        context = project.__parent__
        add_form = False
    else:
        project = Project()
        add_form = True
    
    errors = {}
    defaults = {}
    
    if 'form.submitted' in request.POST:
        try:
            # FormEncode validation
            defaults = dict(request.POST)
            form_result = project_schema.to_python(request.POST)
        except formencode.validators.Invalid, why:
            errors=why.error_dict
        else:
            # Apply schema fields to the project object
            changed = False
            for field_name in project_schema.fields.keys():
                if form_result[field_name] != getattr(project, field_name):
                    setattr(project, field_name, form_result[field_name])
                    changed = True
            # Add project if this is the add form
            if add_form:
                session = DBSession()
                # Add the teacher that created the project to the project.
                user = authenticated_user(request)
                if ITeacher.providedBy(user):
                    project.teachers.append(user)
                session.add(project)
            return HTTPFound(location = model_url(context, request))
    elif 'form.cancel' in request.POST:
        return HTTPFound(location = model_url(context, request))
        
    else:
        if not add_form:
            for field_name in project_schema.fields.keys():
                defaults[field_name] = getattr(project, field_name)
                
            if defaults['start_date']:
                defaults['start_date'] = defaults['start_date'].strftime('%d.%m.%Y')
            if defaults['end_date']:
                defaults['end_date'] = defaults['end_date'].strftime('%d.%m.%Y')
    
    form = render_template('templates/project_edit.pt',
                           project=project,
                           add_form=add_form, 
                           api=TemplateAPI(request))
    # FormEncode fills template with default values
    form = htmlfill.render(form, defaults=defaults, errors=errors)
    return Response(form)


def project_view(context, request):
        
    project = context
    competence_cloud = project_competence_cloud_view(context, request)
    
    return dict(api=TemplateAPI(request),
                project=project,
                request=request,
                comments_view=comments_view,
                competence_cloud=competence_cloud)