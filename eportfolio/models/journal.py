import uuid
from zope.interface import implements

from sqlalchemy import UnicodeText
from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relation, backref

from eportfolio.models import Base, DomainObject, UUID
from eportfolio.models.container import Container
from eportfolio.interfaces import IJournalEntry, IComments
from eportfolio.models import File  

class JournalEntry(DomainObject, Base):
    
    implements(IJournalEntry)
    
    __tablename__ = 'journal_entries'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'))
    project_id = Column(UUID, ForeignKey('projects.id'))
    date = Column(DateTime)
    text = Column(UnicodeText)
    image_id = Column(UUID, ForeignKey(File.id))
    
    user = relation('User', backref=backref('journal_entries', 
            order_by=date.desc(), lazy='dynamic', cascade='all,delete-orphan'))
    project = relation('Project', backref=backref('journal_entries', 
            order_by=date.desc(), lazy='dynamic', cascade='all,delete-orphan'))       
    image = relation(File, backref='journal_entry', uselist=False, 
            cascade='all,delete,delete-orphan', single_parent=True)
            
    @property
    def __name__(self):
        return str(self.id)
    
    def __getitem__(self, key):
        if key == 'comments':
            container = Container(self.comments, IComments)
            container.__parent__ = self
            container.__name__ = u'comments'
            return container
        
        raise KeyError(key)