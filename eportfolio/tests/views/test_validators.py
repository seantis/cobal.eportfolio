from os.path import join, dirname
import Image
from formencode import Invalid

from eportfolio.tests import EPortfolioTestCase

class TestImageUploadConverter(EPortfolioTestCase):
    
    def test_to_python(self):
        from eportfolio.views.validators import ImageUploadConverter
        
        validator = ImageUploadConverter()
        
        # Empty values
        result = validator._to_python(None, None)
        self.assertEqual(None, result)
        
    def test_to_python_jpeg(self):
        from eportfolio.views.validators import ImageUploadConverter
        from cgi import MiniFieldStorage
        
        validator = ImageUploadConverter()
        
        image_path = join(dirname(__file__), 'data', 'image.jpg')
        fd = open(image_path, 'rb')
        storage = MiniFieldStorage('image', 'image.jpg')
        storage.file = fd
        storage.filename = 'image.jpg'
        result = validator._to_python(storage, None)
        image = Image.open(result)
        # Image has been scaled  
        # FIXME: why do we have 130 x 130 here
        self.assertEqual((130, 130), image.size)
        self.assertEqual('JPEG', image.format)
        
    def test_to_python_png(self):
        from eportfolio.views.validators import ImageUploadConverter
        from cgi import MiniFieldStorage
        
        validator = ImageUploadConverter()
        
        image_path = join(dirname(__file__), 'data', 'image.png')
        fd = open(image_path, 'rb')
        storage = MiniFieldStorage('image', 'image.png')
        storage.file = fd
        storage.filename = 'image.png'
        result = validator._to_python(storage, None)
        image = Image.open(result)
        # Image has been scaled 
        # FIXME: why do we have 130 x 130 here
        self.assertEqual((130, 130), image.size)
        self.assertEqual('JPEG', image.format)
        
    def test_to_python_invalid(self):
        from eportfolio.views.validators import ImageUploadConverter
        from cgi import MiniFieldStorage
        
        validator = ImageUploadConverter()
        
        image_path = join(dirname(__file__), 'data', 'image.pdf')
        fd = open(image_path, 'rb')
        storage = MiniFieldStorage('image', 'image.pdf')
        storage.file = fd
        storage.filename = 'image.pdf'
        self.assertRaises(Invalid, validator._to_python, storage, None)
        