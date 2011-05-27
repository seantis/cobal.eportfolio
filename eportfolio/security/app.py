from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import IApplication

class ApplicationPermissions(object):
    
    implements(IPermissionProvider)
    adapts(IApplication)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
        
        acl.append((Allow, 'group:teachers', 'edit'))
        acl.append((Allow, 'group:teachers', 'manage_users'))
        acl.append((Allow, 'group:teachers', 'manage_projects'))
        
        return acl