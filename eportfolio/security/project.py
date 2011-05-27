from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import IProject

class ProjectPermissions(object):
    
    implements(IPermissionProvider)
    adapts(IProject)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
        # Permissions for students in this project
        acl.append((Allow, 'group:students_%s' % self.context.id, 'view'))
        acl.append((Allow, 'group:students_%s' % self.context.id, 'add_journal_entry'))
        # Permissions for teachers in this project
        acl.append((Allow, 'group:teachers_%s' % self.context.id, 'view'))
        acl.append((Allow, 'group:teachers_%s' % self.context.id, 'edit'))
        if not self.context.journal_entries.count():
            acl.append((Allow, 'group:teachers_%s' % self.context.id, 'remove'))
        acl.append((Allow, 'group:teachers_%s' % self.context.id, 'add_journal_entry'))
        
        return acl