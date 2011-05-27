import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from sqlalchemy.orm.util import class_mapper

from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url

from eportfolio.interfaces import ICompetence

from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import MetaCompetence
from eportfolio.models import Competence
    

class CompetenceSchema(formencode.Schema):
    allow_extra_fields = True
    title = formencode.validators.UnicodeString(not_empty=True, max=255)
    description = formencode.validators.UnicodeString(not_empty=True)
    meta_competence_id = formencode.validators.String(not_empty=True)
    
competence_schema = CompetenceSchema()

def competence_edit_view(context, request):
    
    session = DBSession()
    meta_competences = session.query(MetaCompetence).all()
    
    if ICompetence.providedBy(context):
        competence = context
        context = competence.__parent__
        add_form = False
    else:
        competence = Competence()
        add_form = True
    
    errors = {}
    defaults = {}
    
    if 'form.submitted' in request.POST:
        try:
            # FormEncode validation
            defaults = dict(request.POST)
            form_result = competence_schema.to_python(request.POST)
        except formencode.validators.Invalid, why:
            errors=why.error_dict
        else:
            # Apply schema fields to the project object
            field_names = [ p.key for p in class_mapper(Competence).iterate_properties ]
            changed = False
            for field_name in field_names:
                if field_name in form_result.keys():
                    if form_result[field_name] != getattr(competence, field_name):
                        setattr(competence, field_name, form_result[field_name])
                        changed = True
            # Add project if this is the add form
            if add_form:
                session.add(competence)
            return HTTPFound(location = model_url(context, request))
    elif 'form.cancel' in request.POST:
        return HTTPFound(location = model_url(context, request))
        
    else:
        if not add_form:
            field_names = [ p.key for p in class_mapper(Competence).iterate_properties ]
            for field_name in field_names:
                defaults[field_name] = getattr(competence, field_name)
    
    form = render_template('templates/competence_edit.pt',
                           competence=competence,
                           meta_competences=meta_competences,
                           add_form=add_form, 
                           api=TemplateAPI(request))
    # FormEncode fills template with default values
    form = htmlfill.render(form, defaults=defaults, errors=errors)
    return Response(form)