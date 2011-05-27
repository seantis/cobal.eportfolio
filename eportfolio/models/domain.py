from repoze.bfg.threadlocal import get_current_registry

from eportfolio.interfaces import IPermissionProvider

class DomainObject(object):
    
    @property
    def __acl__(self):
        """
        Returns ACL for this object.
        """
        acl = []
        
        adapter = get_current_registry().queryAdapter(self, IPermissionProvider)
        if adapter:
            acl = adapter.acl()
        
        return acl