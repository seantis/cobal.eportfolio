import sha
import uuid
import Image
from cStringIO import StringIO

import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from z3c.rml.rml2pdf import parseString

from sqlalchemy.orm.util import class_mapper

from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url 

from eportfolio.interfaces import IStudent
from eportfolio.utils import authenticated_user
from eportfolio.views.api import TemplateAPI
from eportfolio.views.competence_cloud import student_competence_cloud_view
from eportfolio.views.comments import comments_view

from eportfolio.views.validators import UniqueUsername, FormencodeState

from eportfolio.models import DBSession, get_root
from eportfolio.models import Student
from eportfolio.models import File
from eportfolio.models import JournalEntry
from eportfolio.models import Project
from eportfolio.models import Competence
from eportfolio.models import IndicatorSet
from eportfolio.models import Indicator

def student_view(context, request):
    
    competence_cloud = student_competence_cloud_view(context, request)
    
    # Redirect if the student is accessed by a teacher (gives a nicer URL).
    if authenticated_user(request) != context:
        return HTTPFound(location = model_url(context, request, 'stats.html'))
    
    return dict(student=context,
                competence_cloud=competence_cloud,
                request=request,
                comments_view=comments_view,
                api=TemplateAPI(request))
                
def gained_competences(student):
    """
    Returns a list of project, competences and indicator in the following form:
    
    [ { 'project' : project, 'competences' : [ 'competence' : competence, 'indicators' : [indicator, ...]] } ]
    
    """
    
    session = DBSession()
    
    query = session.query(Project, Competence, Indicator)
    query = query.filter(Student.id == student.id)
    query = query.join(Student.journal_entries)
    query = query.join(JournalEntry.indicators)
    query = query.join(JournalEntry.project)
    query = query.join(Indicator.indicator_set)
    query = query.join(IndicatorSet.competence)
    query = query.order_by(Project.title)
    
    data = []
    current_project = None
    current_competence = None
    for project, competence, indicator in query.all():
        if project != current_project:
            current_project = project
            data.append(dict(project=project, competences=[]))
        if competence != current_competence:
            current_competence = competence
            data[-1]['competences'].append(dict(competence=competence, indicators=[]))
            
        data[-1]['competences'][-1]['indicators'].append(indicator)
        
    return data

def student_application_view(context, request):
    
    data = gained_competences(context)

    return dict(student=context,
                api=TemplateAPI(request),
                data=data)
                
def student_application_pdf_view(context, request):
    
    data = gained_competences(context)
    
    show_projects = request.GET.get('show_projects', False)
    show_journal = request.GET.get('show_journal', False)
    show_indcators = request.GET.get('show_indcators', False)
    
    result = render_template('templates/student_application_pdf.pt',
                             api=TemplateAPI(request),
                             student = context,
                             show_projects = show_projects,
                             show_journal = show_journal,
                             show_indcators = show_indcators,
                             data=data)
    response = Response(parseString(result.encode('utf-8')).read())
    response.content_type =  "application/pdf"
    return response
    
    
class StudentSchema(formencode.Schema):
    allow_extra_fields = True
    first_name = formencode.validators.UnicodeString(not_empty=True)
    last_name = formencode.validators.UnicodeString(not_empty=True)
    email = formencode.All(formencode.validators.Email(not_empty=True), UniqueUsername())
    date_of_birth = formencode.validators.DateConverter(month_style='dd/mm/yyyy', not_empty=True)
    portrait = formencode.validators.FieldStorageUploadConverter() 
    languages = formencode.validators.UnicodeString(max=255)
    interests = formencode.validators.UnicodeString()
    experiences = formencode.validators.UnicodeString()
    hobbies = formencode.validators.UnicodeString()
    
class StudentAddSchema(StudentSchema):
    password = formencode.validators.String()
    
student_schema = StudentSchema()
student_add_schema = StudentAddSchema()
    
def student_edit_view(context, request):
    
    if IStudent.providedBy(context):
        student = context
        context = student.__parent__
        add_form = False
    else:
        student = Student(id=uuid.uuid4())
        add_form = True
    
    errors = {}
    defaults = {}
    
    if 'form.submitted' in request.POST:
        try:
            # FormEncode validation
            defaults = dict(request.POST)
            state = FormencodeState()
            state.user_id = student.user_name
            if add_form:
                form_result = student_add_schema.to_python(request.POST, state)
            else:
                form_result = student_schema.to_python(request.POST, state)
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

                student.portrait = File('portrait.jpg', outfile.read())
                changed = True
                
            del form_result['portrait']
            
            # Apply schema fields to the student object
            field_names = [ p.key for p in class_mapper(Student).iterate_properties ]
            for field_name in field_names:
                if field_name in form_result.keys():
                    if form_result[field_name] != getattr(student, field_name):
                        setattr(student, field_name, form_result[field_name])
                        changed = True
            
            # Add student if this is the add form
            if add_form:
                session = DBSession()
                session.add(student)
                
                if not form_result['password']:
                    reset_url = model_url(get_root(request), request, 'retrieve_password.html')
                    student.send_password_reset(reset_url)
                
            return HTTPFound(location = model_url(context, request, str(student.id)))
            
    elif 'form.cancel' in request.POST:
        if add_form:
            return HTTPFound(location = model_url(context, request))
        else:
            return HTTPFound(location = model_url(context, request, str(student.id)))
        
    else:
        if not add_form:
            field_names = [ p.key for p in class_mapper(Student).iterate_properties ]
            for field_name in field_names:
                defaults[field_name] = getattr(student, field_name)
            defaults['portrait'] = ''
            if defaults['date_of_birth']:
                defaults['date_of_birth'] = defaults['date_of_birth'].strftime('%d/%m/%Y')
                
    
    form = render_template('templates/student_edit.pt',
                           student=student,
                           add_form=add_form, 
                           api=TemplateAPI(request))
    
    # FormEncode fills template with default values
    form = htmlfill.render(form, defaults=defaults, errors=errors)
    return Response(form)

    
def student_projects_view(context, request):
 
    student = context
    projects = student.projects
    
    return dict(student=context,
               request=request,
               projects=projects,
               api=TemplateAPI(request))
    