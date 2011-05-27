from webob.exc import HTTPFound

from repoze.bfg.url import model_url

from eportfolio.views.api import TemplateAPI

from eportfolio.models import DBSession, get_root
from eportfolio.models import Student
from eportfolio.models import Teacher

def members_view(context, request):
    
    session = DBSession()
    all_students = session.query(Student).all()
    all_students = [student for student in all_students if not student in context.students]
    all_teachers = session.query(Teacher).all()
    all_teachers = [teacher for teacher in all_teachers if not teacher in context.teachers]
    
    if 'form.submitted' in request.POST:
        student_id = request.POST.get('student_id', None)
        if student_id:
            student = session.query(Student).filter_by(id=student_id).first()
            if student:
                context.students.append(student)
        teacher_id = request.POST.get('teacher_id', None)
        if teacher_id:
            teacher = session.query(Teacher).filter_by(id=teacher_id).first()
            if teacher:
                context.teachers.append(teacher)
        
        return HTTPFound(location = model_url(context, request, 'members.html'))
    # This should be a post request, but it has to be finished today ...
    elif 'remove_student' in request.GET:
        student_id = request.GET.get('remove_student', None)
        if student_id:
            student = context.students.filter_by(id=student_id).first()
            if student:
                context.students.remove(student)
        return HTTPFound(location = model_url(context, request, 'members.html'))
    elif 'remove_teacher' in request.GET:
        teacher_id = request.GET.get('remove_teacher', None)
        if teacher_id:
            teacher = context.teachers.filter_by(id=teacher_id).first()
            if teacher:
                context.teachers.remove(teacher)
        return HTTPFound(location = model_url(context, request, 'members.html'))
        
    root = get_root(request)
    students = []
    for student in context.students:
        students.append(root['users'][student.id])
        
    teachers = []
    for teacher in context.teachers:
        teachers.append(root['users'][teacher.id])
    
    return dict(api=TemplateAPI(request),
                context=context,
                students=students,
                all_students=all_students,
                teachers=teachers,
                all_teachers=all_teachers)
    