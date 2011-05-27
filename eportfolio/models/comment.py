import uuid  
from zope.interface import implements 

from sqlalchemy import UnicodeText
from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relation, backref

from eportfolio.models import DomainObject, Base, UUID
from eportfolio.interfaces import IComment   

class Comment(DomainObject, Base):
    
    implements(IComment)  
    
    __tablename__ = 'comments'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'))
    journal_entry_id = Column(UUID, ForeignKey('journal_entries.id'))
    date = Column(DateTime)
    text = Column(UnicodeText)
    
    user = relation('User', 
        backref=backref('comments', lazy='dynamic', cascade='all,delete-orphan'))
    journal_entry = relation('JournalEntry', 
        backref=backref('comments', lazy='dynamic', cascade='all,delete-orphan'))
    
    @property
    def __name__(self):
        return str(self.id) 