from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession
from eportfolio.models import Student
from eportfolio.models import Teacher

def users_view(context, request):
    
    session = DBSession()
    students = session.query(Student).order_by(Student.last_name, Student.first_name).all()
    for student in students:
        student.__parent__ = context
        
    teachers = session.query(Teacher).order_by(Teacher.last_name, Teacher.first_name).all()
    for teacher in teachers:
        teacher.__parent__ = context
    
    return dict(context=context,
                students=students,
                teachers=teachers,
                api=TemplateAPI(request))