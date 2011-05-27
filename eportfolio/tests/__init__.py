import datetime
import sha
import unittest

from zope.interface import implements
from repoze.sendmail.interfaces import IMailDelivery

from repoze.bfg.configuration import Configurator

from eportfolio.utilities.mail import MailService

def _initTestingDB():
    from eportfolio.models import initialize_sql
    session = initialize_sql('sqlite://')
    return session
    
class DummyMailer(object):
    
    implements(IMailDelivery)
    
    def __init__(self):
        self.reset()
    
    def send(self, fromaddr, toaddrs, message):
        self.mails.append(message)
        
    def reset(self):
        self.mails = []
        
class AuthTktCookiePluginDummy(object):
    """
    Dummy authentication plugin to test re-authentication if user name is changed. 
    """
    
    def remember(self, environ, identity):
        self.identity = identity
    
class EPortfolioTestCase(unittest.TestCase):
    
    def setUp(self):
        # Warnings become errors!
        #import warnings
        #warnings.filterwarnings('error',category=Warning)
        
        self.config = Configurator()
        self.config.begin()
        _initTestingDB()
        
        # Setup dummy mailer
        self.mailer = DummyMailer()
        self.config.registry.registerUtility(self.mailer)
        self.config.registry.registerUtility(MailService())
        
    def tearDown(self):
        from eportfolio.models import DBSession
        import transaction
        DBSession.remove()
        transaction.abort()
        self.config.end()
        
    def _add_student(self, first_name=u"Buck", last_name=u"Mulligan", 
                     email=u"buck@seantis.ch", password=u'123456'):
        from eportfolio.models.student import Student
        from eportfolio.models import DBSession
        session = DBSession()
        student = Student()
        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        student.password = u'{SHA}%s' % sha.new(password).hexdigest()
        session.add(student)
        session.flush()
        return student
        
    def _add_teacher(self, first_name=u'Leopold', last_name=u'Bloom',
                     email=u'leopold@seantis.ch', password=u'12345'):
        from eportfolio.models.teacher import Teacher
        from eportfolio.models import DBSession
        session = DBSession()
        teacher = Teacher()
        teacher.first_name = first_name
        teacher.last_name = last_name
        teacher.email = email
        teacher.password = u'{SHA}%s' % sha.new(password).hexdigest()
        session.add(teacher)
        session.flush()
        return teacher
        
    def _add_project(self, title=u"Project", start_date=None, end_date=None):
        from eportfolio.models.project import Project
        from eportfolio.models import DBSession
        
        if not start_date:
            start_date = datetime.date.today() - datetime.timedelta(days=10)
            
        if not end_date:
            end_date = datetime.date.today() + datetime.timedelta(days=10)
            
        session = DBSession()
        project = Project()
        project.title = title
        project.start_date = start_date
        project.end_date = end_date
        session.add(project)
        session.flush()
        return project
        
    def _add_objective(self, title=u'Objective', description=u'Objective', project=None):
        from eportfolio.models.objective import Objective
        from eportfolio.models import DBSession
        
        if not project:
            project = self._add_project()
        
        session = DBSession()
        objective = Objective(title=title, description=description, project=project)
        session.add(objective)
        session.flush()
        return objective
        
    def _add_meta_competence(self, title=u'Meta competence', description=u'Meta competence'):
        from eportfolio.models.meta_competence import MetaCompetence
        from eportfolio.models import DBSession
        
        session = DBSession()
        meta_competence = MetaCompetence(title=title, description=description)
        session.add(meta_competence)
        session.flush()
        return meta_competence
        
    def _add_competence(self, title=u'Competence', description=u'Competence', meta_competence=None):
        from eportfolio.models.competence import Competence
        from eportfolio.models import DBSession
        
        if not meta_competence:
            meta_competence = self._add_meta_competence()
        
        session = DBSession()
        competence = Competence(title=title, description=description, meta_competence=meta_competence)
        session.add(competence)
        session.flush()
        return competence
        
    def _add_indicator_set(self, title=u'Indicator set', description=u'Indicator set', competence=None):
        from eportfolio.models.indicator_set import IndicatorSet
        from eportfolio.models import DBSession
        
        if not competence:
            competence = self._add_competence()
            
        session = DBSession()
        indicator_set = IndicatorSet(title=title, description=description, competence=competence)
        session.add(indicator_set)
        session.flush()
        return indicator_set
        
    def _add_indicator(self, title=u'Indicator', description=u'Indicator', indicator_set=None):
        from eportfolio.models.indicator import Indicator
        from eportfolio.models import DBSession
        
        if not indicator_set:
            indicator_set = self._add_indicator_set()
        
        session = DBSession()
        indicator = Indicator(title=title, description=description, indicator_set=indicator_set)
        session.add(indicator)
        session.flush()
        return indicator
        
class EPortfolioIntegrationTestCase(EPortfolioTestCase):
    
    def setUp(self):
        self.config = Configurator()
        self.config.hook_zca()
        self.config.begin()
        self.config.load_zcml('eportfolio:configure.zcml')
        _initTestingDB()
        