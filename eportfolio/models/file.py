import os
import uuid
import mimetypes

from zope.interface import implements

from sqlalchemy import Unicode
from sqlalchemy import Column
from sqlalchemy.orm.interfaces import MapperExtension

from repoze.filesafe import createFile
from repoze.bfg.settings import get_settings

from eportfolio.interfaces import IFile

from eportfolio.models import Base, UUID, DomainObject

class FileRemovalExtension(MapperExtension):
    """
    Mapper extension that makes sure that the actual file is
    removed from the filesystem if the file object is removed
    from the DB.
    """

    def after_delete(self, mapper, connection, instance):
        path = os.path.join(self.path, '%s.%s' % (instance.id, instance.content_type.split('/')[-1]))
        os.remove(path)

# Global variable so that we can configure it with the settings in eportfolio.run.app()
removal_extension = FileRemovalExtension()

class File(DomainObject, Base):
    
    implements(IFile)
    
    __tablename__ = 'files'
    __mapper_args__ = {'extension': removal_extension}
    
    id = Column(UUID, primary_key=True)
    content_type = Column(Unicode(100))
    
    def __init__(self, name, content):
        
        self.id = uuid.uuid4()
        self.content_type =  mimetypes.guess_type(name)[0]
        f = createFile(self.path(), "w")
        f.write(content)
        f.close()
        
    def path(self):
        settings = get_settings()
        path = settings.get('upload_directory')
        return os.path.join(path, '%s.%s' % (self.id, self.content_type.split('/')[-1]))