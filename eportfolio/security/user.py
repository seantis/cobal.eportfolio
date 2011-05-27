from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import IUser

class UserPermissions(object):
    
    implements(IPermissionProvider)
    adapts(IUser)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
        
        acl.append((Allow, self.context.user_name, 'view'))
        acl.append((Allow, self.context.user_name, 'edit'))
        
        return acl