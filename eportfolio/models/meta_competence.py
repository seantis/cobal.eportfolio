from zope.interface import implements 
import uuid

from sqlalchemy import Unicode
from sqlalchemy import UnicodeText 
from sqlalchemy import Column

from eportfolio.models import DomainObject, Base, UUID
from eportfolio.interfaces import IMetaCompetence 

class MetaCompetence(DomainObject, Base):
    
    implements(IMetaCompetence) 
    
    __tablename__ = 'meta_competences'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(Unicode(255))
    description = Column(UnicodeText)
    
    @property
    def __name__(self):
        return str(self.id)