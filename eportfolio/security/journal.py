from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow, Deny, Everyone

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import IJournalEntry

class JournalEntryPermissions(object):
    
    implements(IPermissionProvider)
    adapts(IJournalEntry)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
        
        acl.append((Allow, self.context.user.user_name, 'edit'))
        acl.append((Deny, Everyone, 'edit'))
        if not self.context.comments.count():
            acl.append((Allow, self.context.user.user_name, 'remove')) 
        
        return acl