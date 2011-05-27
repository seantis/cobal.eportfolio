import uuid

from zope.interface import implements

from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import Integer

from sqlalchemy.orm import relation, backref, dynamic_loader

from eportfolio.interfaces import IIndicator

from eportfolio.models import Base, UUID
from eportfolio.models import IndicatorSet
from eportfolio.models import JournalEntry

journal_entries_indicators = Table('journal_entries_indicators', Base.metadata,
    Column('journal_entries_id', UUID, ForeignKey('journal_entries.id')),
    Column('indicators_id', UUID, ForeignKey('indicators.id'))
)

class Indicator(Base):
    
    implements(IIndicator)
    
    __tablename__ = 'indicators'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    indicator_set_id = Column(UUID, ForeignKey('indicator_sets.id'))
    title = Column(Unicode(255))
    description = Column(UnicodeText)
    type = Column(Unicode(255))
    weight = Column(Float)
    sort_order = Column(Integer)
    
    indicator_set = relation(IndicatorSet, backref=backref('indicators', lazy='dynamic', 
                            cascade='all,delete-orphan', order_by='indicators.c.sort_order'))
                              
    journal_entries = dynamic_loader(JournalEntry, secondary=journal_entries_indicators, 
                            backref=backref('indicators', lazy='dynamic'))
                              
    @property
    def __name__(self):
        return str(self.id)