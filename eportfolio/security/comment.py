from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow, Deny, Everyone

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import IComment

class CommentPermissions(object):
    
    implements(IPermissionProvider)
    adapts(IComment)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
                
        acl.append((Allow, self.context.user.user_name, 'remove'))
        
        return acl