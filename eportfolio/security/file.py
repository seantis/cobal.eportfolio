from zope.interface import implements
from zope.component import adapts

from repoze.bfg.security import Allow

from eportfolio.interfaces import IPermissionProvider
from eportfolio.interfaces import IFile

class FilePermissions(object):
    
    implements(IPermissionProvider)
    adapts(IFile)
    
    def __init__(self, context):
        self.context = context
        
    def acl(self):
        user = self.context.__parent__.__parent__
        acl = []
        # User can view and edit files
        acl.append((Allow, user.user_name, 'view'))
        acl.append((Allow, user.user_name, 'edit'))
        # Permissions for students and teachers in user's projects
        for project in user.projects:
            acl.append((Allow, 'group:students_%s' % project.id, 'view'))
            acl.append((Allow, 'group:teachers_%s' % project.id, 'view'))
        return acl