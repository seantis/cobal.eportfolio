from zope.interface import implements

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey

from sqlalchemy.orm import dynamic_loader, backref

from eportfolio.interfaces import ITeacher

from eportfolio.models import Base, UUID
from eportfolio.models import User
from eportfolio.models.project import Project

teachers_projects = Table('teachers_projects', Base.metadata,
    Column('teacher_id', UUID, ForeignKey('teachers.id')),
    Column('project_id', UUID, ForeignKey('projects.id'))
)

class Teacher(User):
    
    implements(ITeacher)
    
    __tablename__ = 'teachers'
    id = Column(UUID, ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': u'teacher'}
    
    # teacher specific fields
    
    projects = dynamic_loader(Project, secondary=teachers_projects, 
                              backref=backref('teachers', lazy='dynamic'))
                              
    @property
    def groups(self):
        groups = ['group:teachers',]
        for project in self.projects:
            groups.append('group:teachers_%s' % project.id)
        
        return tuple(groups)