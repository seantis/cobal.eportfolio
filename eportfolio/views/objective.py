import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url

from eportfolio.interfaces import IObjective

from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import Objective
from eportfolio.models import Competence

class ObjectiveSchema(formencode.Schema):
    allow_extra_fields = True
    title = formencode.validators.UnicodeString(not_empty=True, max=255)
    description = formencode.validators.UnicodeString(not_empty=True)      
    competences = formencode.ForEach(formencode.validators.String())
    
objective_schema = ObjectiveSchema()

def objective_edit_view(context, request):
    
    session = DBSession()
    competences = session.query(Competence).all()
    
    if IObjective.providedBy(context):
        add_form = False
        objective = context
        project = context.project
        context = objective.__parent__
    else:
        objective = Objective()
        add_form = True
        project = context.__parent__ 
    
    errors = {}
    defaults = {}
    
    if 'form.submitted' in request.POST:
        try:
            # FormEncode validation
            defaults = dict(request.POST)
            form_result = objective_schema.to_python(request.POST)
        except formencode.validators.Invalid, why:
            errors=why.error_dict
        else:
            # Apply schema fields to the project object
            changed = False
            competences = []
            for competence_id in form_result['competences']:
                competence = session.query(Competence).filter_by(id=competence_id).first()
                if competence:
                    competences.append(competence)
            form_result['competences'] = competences
            for field_name in objective_schema.fields.keys():
                if form_result[field_name] != getattr(objective, field_name):
                    setattr(objective, field_name, form_result[field_name])
                    changed = True
            # Add onjective if this is the add form
            if add_form:
                objective.project = project
                session.add(objective) 
            return HTTPFound(location = model_url(context, request))
    elif 'form.cancel' in request.POST:
        return HTTPFound(location = model_url(context, request))
        
    else:
        if not add_form:
            for field_name in objective_schema.fields.keys():
                value = getattr(objective, field_name)
                if field_name == 'competences':
                    values = []
                    for competence in value:
                        values.append(competence.id)
                    value = values
                defaults[field_name] = value
    
    form = render_template('templates/objective_edit.pt',
                           objective=objective,
                           competences=competences,
                           add_form=add_form,
                           api=TemplateAPI(request))
    # FormEncode fills template with default values
    form = htmlfill.render(form, defaults=defaults, errors=errors)
    return Response(form)