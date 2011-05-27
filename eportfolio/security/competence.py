from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import ICompetence

class CompetencePermissions(object):
    
    implements(IPermissionProvider)
    adapts(ICompetence)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
        
        # Permissions for teachers on the competences
        # TODO: We probably need a special role here.
        acl.append((Allow, 'group:teachers', 'view'))
        acl.append((Allow, 'group:teachers', 'edit'))
        acl.append((Allow, 'group:teachers', 'remove'))
        
        return acl