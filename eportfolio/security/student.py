from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import IStudent

class StudentPermissions(object):
    
    implements(IPermissionProvider)
    adapts(IStudent)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
        
        acl.append((Allow, self.context.user_name, 'view'))
        acl.append((Allow, self.context.user_name, 'edit'))
        # All teachers can access all students
        acl.append((Allow, 'group:teachers', 'view'))
        # TODO: Not sure whether teachers should be able to edit student's profiles.
        acl.append((Allow, 'group:teachers', 'edit'))
        if not self.context.journal_entries.count():
            acl.append((Allow, 'group:teachers', 'remove'))
        
        return acl