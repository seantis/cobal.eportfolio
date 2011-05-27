import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from sqlalchemy.orm.util import class_mapper

from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url

from eportfolio.interfaces import IIndicatorSet

from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import IndicatorSet

class IndicatorSetSchema(formencode.Schema):
    allow_extra_fields = True
    title = formencode.validators.UnicodeString(not_empty=True, max=255)
    
indicator_set_schema = IndicatorSetSchema()

def indicator_set_edit_view(context, request):
    
    if IIndicatorSet.providedBy(context):
        indicator_set = context
        competence = indicator_set.competence
        context = indicator_set.__parent__
        add_form = False
    else:
        indicator_set = IndicatorSet()
        competence = context.__parent__
        add_form = True
    
    errors = {}
    defaults = {}
    
    if 'form.submitted' in request.POST:
        try:
            # FormEncode validation
            defaults = dict(request.POST)
            form_result = indicator_set_schema.to_python(request.POST)
        except formencode.validators.Invalid, why:
            errors=why.error_dict
        else:
            # Apply schema fields to the project object
            field_names = [ p.key for p in class_mapper(IndicatorSet).iterate_properties ]
            changed = False
            for field_name in field_names:
                if field_name in form_result.keys():
                    if form_result[field_name] != getattr(indicator_set, field_name):
                        setattr(indicator_set, field_name, form_result[field_name])
                        changed = True
            # Add project if this is the add form
            if add_form:
                session = DBSession()
                indicator_set.competence = competence
                session.add(indicator_set)
            return HTTPFound(location = model_url(competence.__parent__, request))
    elif 'form.cancel' in request.POST:
        return HTTPFound(location = model_url(competence.__parent__, request))
        
    else:
        if not add_form:
            field_names = [ p.key for p in class_mapper(IndicatorSet).iterate_properties ]
            for field_name in field_names:
                defaults[field_name] = getattr(indicator_set, field_name)
    
    form = render_template('templates/indicator_set_edit.pt',
                           indicator_set=indicator_set,
                           competence=competence,
                           add_form=add_form, 
                           api=TemplateAPI(request))
    # FormEncode fills template with default values
    form = htmlfill.render(form, defaults=defaults, errors=errors)
    return Response(form)
    