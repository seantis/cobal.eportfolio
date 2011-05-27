import simplejson
from sqlalchemy import func

from repoze.bfg.i18n import TranslationStringFactory
from repoze.bfg.i18n import get_localizer

from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import Student
from eportfolio.models import Project
from eportfolio.models import Objective
from eportfolio.models import Competence
from eportfolio.models import IndicatorSet
from eportfolio.models import Indicator
from eportfolio.models import JournalEntry

_ = TranslationStringFactory('eportfolio')

def student_stats_view(context, request):
    
    session = DBSession()
    
    # Achievable competences
    query = session.query(Competence.id, Competence.title, func.count(Competence.id))
    query = query.filter(Student.id == context.id)
    query = query.join(Student.projects)
    query = query.join(Project.objectives)
    query = query.join(Objective.competences)
    query = query.join(Competence.indicator_sets)
    query = query.join(IndicatorSet.indicators)
    query = query.group_by(Competence.id, Competence.title)
    achiveable = query.order_by(Competence.title).all()
    
    # Subquery in order to count each indicator only once
    subquery = session.query(Indicator.id.label('indicator_id'))
    subquery = subquery.filter(Student.id == context.id)
    subquery = subquery.join(Student.journal_entries)
    subquery = subquery.join(JournalEntry.indicators)
    subquery = subquery.distinct().subquery()
    
    # Achieved competences
    query = session.query(Competence.id, Competence.title, func.count(Competence.id))
    query = query.filter(subquery.c.indicator_id == Indicator.id)
    query = query.join(Indicator.indicator_set)
    query = query.join(IndicatorSet.competence)
    query = query.group_by(Competence.id, Competence.title)
    achieved = query.order_by(Competence.title).all()
    
    # Combine the two lists into one
    numbers = []
    for element in achiveable:
        number = {'label' : element[1], 'achievable' : element[2], 'achieved' : 0}
        if len(achieved) and achieved[0][0] == element[0]:
            number['achieved'] = achieved.pop(0)[2]
        numbers.append(number)
    
    localizer = get_localizer(request)
    
    graph_axis = []
    graph_data = []
    graph_data.append({ 'label' : '&nbsp;%s&nbsp;' % localizer.translate(_('Achieved')), 'data' : [] })
    graph_data.append({ 'label' : '&nbsp;%s&nbsp;' % localizer.translate(_('Achievable')), 'data' : [] })
    for index, number in enumerate(numbers):
        graph_axis.append([index, number['label']])
        graph_data[0]['data'].append([index, number['achieved']])
        graph_data[1]['data'].append([index, number['achievable'] - number['achieved']])
        
    projects = []
    for project in context['projects']:
        project_data = {'title' : project.title}
        # Collect all competences for the project
        competences = []
        for objective in project.objectives:
            for competence in objective.competences:
                achieved = False
                if not competence in competences:
                    competence_data = {'title' : competence.title, 'indicator_sets' : [], 'achieved' : False}
                    for indicator_set in competence.indicator_sets:
                        indicator_set_data = {'title' : indicator_set.title, 'achieved' : False}
                        indicators = []
                        for indicator in indicator_set.indicators:
                            indicator_data = {'title' : indicator.title, 'achieved' : False}
                            # Check whether indicator has been achieved
                            query = session.query(Indicator)
                            query = query.filter(JournalEntry.user_id == context.id)
                            query = query.filter(Indicator.id == indicator.id)
                            query = query.join(JournalEntry.indicators)
                            if query.first():
                                achieved = True
                                indicator_data['achieved'] = True
                            indicators.append(indicator_data)
                        indicator_set_data['indicators'] = indicators
                        if achieved:
                            indicator_set_data['achieved'] = True
                        competence_data['indicator_sets'].append(indicator_set_data)
                        
                    if achieved:
                        competence_data['achieved'] = True
                    competences.append(competence_data)
        project_data['competences'] = competences
        projects.append(project_data)
    
    return dict(api=TemplateAPI(request),
                projects=projects,
                graph_axis=simplejson.dumps(graph_axis),
                graph_data=simplejson.dumps(graph_data))
