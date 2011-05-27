import os
import shutil

# repoze.filesafe uses os.rename(...) which does not work
# across filesystems.

from repoze.filesafe.manager import FileSafeDataManager

def commit(self, transaction):
    self.in_commit=True
    for target in self.vault:
        info=self.vault[target]
        if os.path.exists(target):
            info["has_original"]=True
            os.link(target, "%s.filesafe" % target)
        else:
            info["has_original"]=False
        # NEXT LINE IS PATCHED: Use shutil.move instead of os.rename
        shutil.move(info["tempfile"], target)
        info["moved"]=True
        
FileSafeDataManager.commit = commit