from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow, Deny, Everyone

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import IMetaCompetence

class MetaCompetencePermissions(object):
    
    implements(IPermissionProvider)
    adapts(IMetaCompetence)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
        
        if not self.context.competences:
            acl.append((Allow, 'group:teachers', 'remove'))
        
        return acl