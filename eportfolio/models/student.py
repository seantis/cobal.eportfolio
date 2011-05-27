from zope.interface import implements

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Unicode 
from sqlalchemy import UnicodeText 
from sqlalchemy import Date

from sqlalchemy.orm import dynamic_loader, backref

from eportfolio.interfaces import IStudent

from eportfolio.models import Base, UUID
from eportfolio.models import User
from eportfolio.models.project import Project

students_projects = Table('students_projects', Base.metadata,
    Column('student_id', UUID, ForeignKey('students.id')),
    Column('project_id', UUID, ForeignKey('projects.id'))
)

class Student(User):
    
    implements(IStudent)
    
    __tablename__ = 'students'
    id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': u'student'}
    
    # student specific fields
    date_of_birth = Column(Date)
    languages = Column(Unicode(255))
    interests = Column(UnicodeText)
    experiences = Column(UnicodeText)
    hobbies = Column(UnicodeText)
    
    projects = dynamic_loader(Project, secondary=students_projects, 
                              backref=backref('students', lazy='dynamic'))
                              
    @property
    def groups(self):
        groups = ['group:students',]
        for project in self.projects:
            groups.append('group:students_%s' % project.id)
        
        return tuple(groups)
