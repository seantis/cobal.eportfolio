import datetime
from repoze.bfg import testing

from eportfolio.tests import EPortfolioTestCase

class TestMembersView(EPortfolioTestCase):
    
    def test_members_view(self):
        from eportfolio.models.app import Application
        from eportfolio.models.project import Project
        from eportfolio.views.members import members_view
        
        root = Application()
        project = Project()
        
        # No members assigned yet
        request = testing.DummyRequest(root=root)
        response = members_view(project, request)
        self.assertEquals([], response['all_students'])
        self.assertEquals([], response['all_teachers'])
        
        # Student in list of students that can be assigned
        student = self._add_student()
        response = members_view(project, request)
        self.assertEquals([student], response['all_students'])
        
        # Assign student to project
        request.POST['student_id'] = student.id
        request.POST['form.submitted'] = 1
        response = members_view(project, request)
        self.assertEquals([student], project.students.all())
        
        request = testing.DummyRequest(root=root)
        response = members_view(project, request)
        # Student cannot be assigned a second time
        self.assertEquals([], response['all_students'])
        self.assertEquals([student], response['students'])
        
        # Teacher in the list of teachers than can be assigned
        teacher = self._add_teacher()
        response = members_view(project, request)
        self.assertEquals([teacher], response['all_teachers'])
        
        # Assign teacher to project
        request.POST['teacher_id'] = teacher.id
        request.POST['form.submitted'] = 1
        response = members_view(project, request)
        self.assertEquals([teacher], project.teachers.all())
        
        request = testing.DummyRequest(root=root)
        response = members_view(project, request)
        # Teacher cannot be assigned a second time
        self.assertEquals([], response['all_teachers'])
        self.assertEquals([teacher], response['teachers'])