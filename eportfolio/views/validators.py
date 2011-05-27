import formencode
import Image
from cStringIO import StringIO

from eportfolio import translation_factory as _
from eportfolio.models import DBSession
from eportfolio.models import User

class FormencodeState(object):
    """
    The state argument of to_python must be an object that formencode can hang 
    additional attributes on.
    """
    pass
           
class UniqueUsername(formencode.FancyValidator):
    def _to_python(self, value, state):
        session = DBSession()
        value = value.lower()
        if session.query(User).filter_by(user_name=value).count():
            if not state or state.user_id != value:  
                raise formencode.Invalid(u'Ein Benutzer mit diesem Namen existiert bereits.', value, state)
        return value
        
class ImageUploadConverter(formencode.validators.FieldStorageUploadConverter):
    
    def _to_python(self, value, state):
        value = super(ImageUploadConverter, self)._to_python(value, state)
    
        if value is not None:
            # Scale image and convert to JPEG
            try:
                im = Image.open(value.file)

                im.thumbnail((600, 480),Image.ANTIALIAS)
            
                # TODO: we also want a thumbnail image here
            
                # Convert to RGB if neccessary
                if im.mode != "RGB":
                    im = im.convert("RGB")
                outfile = StringIO()
                im.save(outfile, "JPEG")
                outfile.seek(0)

                return outfile
            except IOError:
                raise formencode.Invalid(u'Unbekanntes Bildformat', value, state)
            
        return value