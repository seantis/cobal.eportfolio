from zope.interface import implements

from eportfolio.interfaces import IApplication
from eportfolio.interfaces import IProjects
from eportfolio.interfaces import IUsers
from eportfolio.interfaces import IMetaCompetences
from eportfolio.interfaces import ICompetences

from eportfolio.models.container import Container
from eportfolio.models import DomainObject
from eportfolio.models import DBSession
from eportfolio.models import MetaCompetence
from eportfolio.models import Competence
from eportfolio.models import Project
from eportfolio.models import User

class Application(DomainObject):
    
    implements(IApplication)
    
    __name__ = None
    __parent__ = None

    def __getitem__(self, key):
        if key == 'projects':
            session = DBSession()
            projects_container = Container(session.query(Project), IProjects)
            projects_container.__parent__ = self
            projects_container.__name__ = key
            return projects_container
        if key == 'users':
            session = DBSession()
            container = Container(session.query(User), IUsers)
            container.__parent__ = self
            container.__name__ = key
            return container
        if key == 'meta_competences':
            session = DBSession()
            container = Container(session.query(MetaCompetence), IMetaCompetences)
            container.__parent__ = self
            container.__name__ = key
            return container
        if key == 'competences':
            session = DBSession()
            container = Container(session.query(Competence), ICompetences)
            container.__parent__ = self
            container.__name__ = u'competences'
            return container
        
        raise KeyError(key)