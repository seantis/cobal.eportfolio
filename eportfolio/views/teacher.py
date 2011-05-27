import sha
import uuid
import Image
from cStringIO import StringIO

import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from sqlalchemy.orm.util import class_mapper

from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url   

from eportfolio.interfaces import ITeacher

from eportfolio.views.api import TemplateAPI
from eportfolio.views.validators import UniqueUsername, FormencodeState

from eportfolio.models import DBSession, get_root
from eportfolio.models import Teacher
from eportfolio.models import File

def pw_reset_key(user, salt):
    k = user.first_name + user.password + user.email + str(user.portrait_id) + salt
    return sha.sha(k.encode('utf-8')).hexdigest()

def teacher_view(context, request):
    
    return dict(teacher=context,
                api=TemplateAPI(request))
                

class TeacherSchema(formencode.Schema):
    allow_extra_fields = True
    first_name = formencode.validators.UnicodeString(not_empty=True)
    last_name = formencode.validators.UnicodeString(not_empty=True)
    email = formencode.All(formencode.validators.Email(not_empty=True), UniqueUsername())
    portrait = formencode.validators.FieldStorageUploadConverter()
    
class TeacherAddSchema(TeacherSchema):
    password = formencode.validators.String()
    
teacher_schema = TeacherSchema()
teacher_add_schema = TeacherAddSchema()
    
def teacher_edit_view(context, request):
    
    if ITeacher.providedBy(context):
        teacher = context
        context = teacher.__parent__
        add_form = False
    else:
        teacher = Teacher(id=uuid.uuid4())
        add_form = True
    
    errors = {}
    defaults = {}
    
    if 'form.submitted' in request.POST:
        try:
            # FormEncode validation
            defaults = dict(request.POST)
            state = FormencodeState()
            state.user_id = teacher.user_name
            if add_form:
                form_result = teacher_add_schema.to_python(request.POST, state)
            else:
                form_result = teacher_schema.to_python(request.POST, state)
        except formencode.validators.Invalid, why:
            errors=why.error_dict
        else:
            changed = False
            
            # Convert password to SHA hash
            if form_result.get('password', None):
                form_result['password'] = '{SHA}%s' % sha.new(form_result['password']).hexdigest()
                changed = True
            
            # Handle portrait upload
            if form_result['portrait'] is not None:
                
                # Scale image and convert to JPEG
                im = Image.open(form_result['portrait'].file)
                im.thumbnail((128, 128),Image.ANTIALIAS)
                # Convert to RGB if neccessary
                if im.mode != "RGB":
                    im = im.convert("RGB")
                outfile = StringIO()
                im.save(outfile, "JPEG")
                outfile.seek(0)

                teacher.portrait = File('portrait.jpg', outfile.read())
                changed = True
                
            del form_result['portrait']
            
            # Apply schema fields to the student object
            field_names = [ p.key for p in class_mapper(Teacher).iterate_properties ]
            for field_name in field_names:
                if field_name in form_result.keys():
                    if form_result[field_name] != getattr(teacher, field_name):
                        setattr(teacher, field_name, form_result[field_name])
                        changed = True
            
            # Add student if this is the add form
            if add_form:
                session = DBSession()
                session.add(teacher)
                
                if not form_result['password']:
                    reset_url = model_url(get_root(request), request, 'retrieve_password.html')
                    teacher.send_password_reset(reset_url)
                
            return HTTPFound(location = model_url(context, request))
            
    elif 'form.cancel' in request.POST:
        return HTTPFound(location = model_url(context, request))

        
    else:
        if not add_form:
            field_names = [ p.key for p in class_mapper(Teacher).iterate_properties ]
            for field_name in field_names:
                defaults[field_name] = getattr(teacher, field_name)
            defaults['portrait'] = ''
    
    form = render_template('templates/teacher_edit.pt',
                           teacher=teacher,
                           add_form=add_form, 
                           api=TemplateAPI(request))
    
    # FormEncode fills template with default values
    form = htmlfill.render(form, defaults=defaults, errors=errors)
    return Response(form)