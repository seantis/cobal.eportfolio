from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from eportfolio.models.uuid_type import UUID
from eportfolio.models.domain import DomainObject
from eportfolio.models.file import File
from eportfolio.models.project import Project
from eportfolio.models.user import User
from eportfolio.models.student import Student
from eportfolio.models.journal import JournalEntry
from eportfolio.models.meta_competence import MetaCompetence
from eportfolio.models.competence import Competence
from eportfolio.models.indicator_set import IndicatorSet
from eportfolio.models.indicator import Indicator
from eportfolio.models.comment import Comment
from eportfolio.models.app import Application
from eportfolio.models.teacher import Teacher
from eportfolio.models.objective import Objective

def initialize_sql(db_string):
    engine = create_engine(db_string)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    
root = Application()

def get_root(request):
    return root
