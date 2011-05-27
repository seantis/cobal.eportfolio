import math

from sqlalchemy import func

from repoze.bfg.chameleon_zpt import render_template

from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import Project
from eportfolio.models import Competence
from eportfolio.models import IndicatorSet
from eportfolio.models import Indicator
from eportfolio.models import JournalEntry
from eportfolio.models import Student

def norm(factor, stddev):
    if factor >= 2 * stddev:
        weight = 7
    elif factor >= stddev:
        weight = 6
    elif factor >= 0.5 * stddev:
        weight = 5
    elif factor > -0.5 * stddev:
        weight = 4
    elif factor > -stddev:
        weight = 3
    elif factor > -2 * stddev:
        weight = 2
    else:
        weight = 1
    return weight

def _calculateTagWeights(taglist):
    if not taglist:
        return taglist
    counts = list()
    for tag in taglist:
        counts.append(tag['count'])
    count = len(taglist)
    total = reduce(lambda x, y: x+ y, counts)
    mean = total/count
    var = reduce(lambda x,y: x + math.pow(y-mean, 2), counts, 0)/count
    stddev = math.sqrt(var)
    for t in taglist:
        factor = (t['count'] - mean)
        weight = t['weight'] = norm(factor, stddev)
        t['class'] = 'tagweight%d' % weight
    return taglist

def project_competence_cloud_view(context, request):
    session = DBSession()
    query = session.query(Competence.title, func.count(Competence.id))
    query = query.filter(Project.id == context.id)
    query = query.join(Project.journal_entries)
    query = query.join(JournalEntry.indicators)
    query = query.join(Indicator.indicator_set)
    query = query.join(IndicatorSet.competence)
    query = query.group_by(Competence.id, Competence.title)
    
    tags = query.all()
    if tags is not None:
        cloud = [{'name': x[0], 'count': x[1]} for x in tags]
        limited = list(reversed(sorted(cloud, key=lambda x: x['count'])))[:100]
        entries = sorted(_calculateTagWeights(limited), key=lambda x: x['name'])
    else:
        entries = ()

    return render_template(
        'templates/competence_cloud.pt',
        api=TemplateAPI(request),
        entries=entries,
        )
        
def student_competence_cloud_view(context, request):
    session = DBSession()
    query = session.query(Competence.title, func.count(Competence.id))
    query = query.filter(Student.id == context.id)
    query = query.join(Student.journal_entries)
    query = query.join(JournalEntry.indicators)
    query = query.join(Indicator.indicator_set)
    query = query.join(IndicatorSet.competence)
    query = query.group_by(Competence.id, Competence.title)
    
    tags = query.all()
    if tags is not None:
        cloud = [{'name': x[0], 'count': x[1]} for x in tags]
        limited = list(reversed(sorted(cloud, key=lambda x: x['count'])))[:100]
        entries = sorted(_calculateTagWeights(limited), key=lambda x: x['name'])
    else:
        entries = ()

    return render_template(
        'templates/competence_cloud.pt',
        api=TemplateAPI(request),
        entries=entries,
        )
