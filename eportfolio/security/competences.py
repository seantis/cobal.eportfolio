from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import ICompetences

class CompetencesContainerPermissions(object):
    
    implements(IPermissionProvider)
    adapts(ICompetences)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        acl = []
        
        # Permissions for teachers on the competences container
        acl.append((Allow, 'group:teachers', 'view'))
        acl.append((Allow, 'group:teachers', 'edit'))
        
        return acl