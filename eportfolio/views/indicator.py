import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from sqlalchemy.orm.util import class_mapper

from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url
from repoze.bfg.traversal import find_interface

from eportfolio.interfaces import IIndicator, ICompetences

from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import Indicator
    

class IndicatorSchema(formencode.Schema):
    allow_extra_fields = True
    title = formencode.validators.UnicodeString(not_empty=True, max=255)
    description = formencode.validators.UnicodeString(not_empty=True)
    
indicator_schema = IndicatorSchema()

def indicator_edit_view(context, request):
    
    if IIndicator.providedBy(context):
        indicator = context
        indicator_set = indicator.indicator_set
        add_form = False
    else:
        indicator = Indicator()
        indicator_set = context.__parent__
        add_form = True
    
    competences_container = find_interface(context, ICompetences)
    
    errors = {}
    defaults = {}
    
    if 'form.submitted' in request.POST:
        try:
            # FormEncode validation
            defaults = dict(request.POST)
            form_result = indicator_schema.to_python(request.POST)
        except formencode.validators.Invalid, why:
            errors=why.error_dict
        else:
            # Apply schema fields to the project object
            field_names = [ p.key for p in class_mapper(Indicator).iterate_properties ]
            changed = False
            for field_name in field_names:
                if field_name in form_result.keys():
                    if form_result[field_name] != getattr(indicator, field_name):
                        setattr(indicator, field_name, form_result[field_name])
                        changed = True
            # Add project if this is the add form
            if add_form:
                session = DBSession()
                indicator.indicator_set = indicator_set
                indicator.index = indicator_set.indicators.count() - 1
                session.add(indicator)
            return HTTPFound(location = model_url(competences_container, request))
    elif 'form.cancel' in request.POST:
        return HTTPFound(location = model_url(competences_container, request))
        
    else:
        if not add_form:
            field_names = [ p.key for p in class_mapper(Indicator).iterate_properties ]
            for field_name in field_names:
                defaults[field_name] = getattr(indicator, field_name)
    
    form = render_template('templates/indicator_edit.pt',
                           indicator=indicator,
                           add_form=add_form, 
                           api=TemplateAPI(request))
    # FormEncode fills template with default values
    form = htmlfill.render(form, defaults=defaults, errors=errors)
    return Response(form)