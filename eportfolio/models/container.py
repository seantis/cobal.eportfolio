from zope.interface import directlyProvides, implements
from sqlalchemy.orm.exc import NoResultFound

from eportfolio.interfaces import IContainer
from eportfolio.models.domain import DomainObject

class Container(DomainObject):
    
    implements(IContainer)
    
    def __init__(self, query, interface=None):
        self.query = query
        if interface:
            directlyProvides(self, interface)
    
    def __getitem__(self, key):
        # Slice access
        if isinstance(key, slice):
            items = self.query[range]
            for item in items:
                item.__parent__ = self
            return items
        # Key access
        try:
            item = self.query.filter_by(id=key).one()
            item.__parent__ = self
            return item
        except (ValueError, NoResultFound):
            pass
        raise KeyError(key)
        
    def __delitem__(self, key):
        self.query.session.delete(self[key])
        
    def get(self, key, default=None):
        try:
            item = self.__getitem__(key)
        except KeyError:
            item = default
        return item

    def __iter__(self):
        for item in self.query:
            item.__parent__ = self
            yield item
            
    def __len__(self):
        return self.query.count()
        