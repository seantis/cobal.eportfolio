from datetime import datetime

import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url

from eportfolio.utils import authenticated_user
from eportfolio.views.api import TemplateAPI
from eportfolio.views.validators import ImageUploadConverter
from eportfolio.interfaces import IJournalEntry, ITeacher

from eportfolio.models import DBSession, get_root
from eportfolio.models import Indicator
from eportfolio.models import JournalEntry
from eportfolio.models import Project
from eportfolio.models import Competence
from eportfolio.models import IndicatorSet
from eportfolio.models import Objective
from eportfolio.models import File

class JournalEntrySchema(formencode.Schema):
    allow_extra_fields = True
    text = formencode.validators.UnicodeString(not_empty=True)
    indicators = formencode.ForEach(formencode.validators.String())
    image = ImageUploadConverter(if_missing=None)
    image_action = formencode.validators.OneOf((u'nochange', u'delete', u'replace'), hideList=True, if_missing=u'nochange')
    
entry_schema = JournalEntrySchema()

def journal_add_view(context, request):
    
    if IJournalEntry.providedBy(context):
        entry = context
        project = context.__parent__.__parent__
        add_form = False
    else:
        entry = JournalEntry()
        project = context
        add_form = True
        
    errors = {}
    defaults = {}
    
    if 'form.submitted' in request.POST:
        try:
            # FormEncode validation
            defaults = dict(request.POST)
            defaults['indicators'] = request.POST.get('indicators')
            form_result = entry_schema.to_python(request.POST)
        except formencode.validators.Invalid, why:
            errors=why.error_dict
        else:
            
            session = DBSession()
            
            # Handle image upload
            if form_result['image'] is not None:
                entry.image = File('image.jpg', form_result['image'].read())

            elif form_result['image_action'] == 'delete' and entry.image:
                session.delete(entry.image)
            
            entry.date = datetime.now()
            entry.text = form_result['text']
            entry.user = authenticated_user(request)
            
            # Check whether indicator belongs to this project.
            indicator_query = session.query(Indicator)
            indicator_query = indicator_query.filter(Project.id == project.id)
            indicator_query = indicator_query.join(Project.objectives)
            indicator_query = indicator_query.join(Objective.competences)
            indicator_query = indicator_query.join(Competence.indicator_sets)
            indicator_query = indicator_query.join(IndicatorSet.indicators)
            if form_result['indicators']:
                indicator_query = indicator_query.filter(Indicator.id.in_(form_result['indicators']))
                indicators = indicator_query.all()
                entry.indicators = indicators
            
            if add_form:
                project.journal_entries.append(entry)
                
            if ITeacher.providedBy(authenticated_user(request)):
                return HTTPFound(location = model_url(get_root(request)['projects'][project.id], request))
            return HTTPFound(location = model_url(authenticated_user(request), request))
            
    elif 'form.cancel' in request.POST:
        if ITeacher.providedBy(authenticated_user(request)):
            return HTTPFound(location = model_url(get_root(request)['projects'][project.id], request))
        return HTTPFound(location = model_url(authenticated_user(request), request))
        
    else:
        if not add_form:
            for field_name in entry_schema.fields.keys():
                if hasattr(entry, field_name):
                    defaults[field_name] = getattr(entry, field_name)
                
            defaults['indicators'] = [indicator.id for indicator in entry.indicators]
            if entry.image:
                defaults['image_action'] = 'nochange'
            defaults['image'] = '' 
    
    session = DBSession()
    user = authenticated_user(request)
    query = session.query(Indicator)
    query = query.filter(JournalEntry.user == user)
    query = query.filter(JournalEntry.project == project)
    query = query.filter(JournalEntry.id != entry.id)
    query = query.join(Indicator.journal_entries)
    already_tagged = query.all()
    
    query = session.query(IndicatorSet)
    query = query.filter(Project.id == project.id)
    query = query.join(Project.objectives)
    query = query.join(Objective.competences)
    query = query.join(Competence.indicator_sets)
    indicator_sets = []
    for indicator_set in query.all():
        indicators = []
        for indicator in indicator_set.indicators:
            if indicator not in already_tagged:
                indicators.append({'id' : str(indicator.id), 'description' : indicator.description})
        if indicators:
            indicator_sets.append({'title' : indicator_set.title, 'indicators' : indicators, 'competence' : indicator_set.competence.title})
    
    form = render_template(
        'templates/journal_add.pt',
        api=TemplateAPI(request),
        indicator_sets=indicator_sets,
        project=project,
        entry=entry,
        add_form=add_form)
    
    # FormEncode fills template with default values
    form = htmlfill.render(form, defaults=defaults, errors=errors)
    return Response(form)