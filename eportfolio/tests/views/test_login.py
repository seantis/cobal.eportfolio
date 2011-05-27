from repoze.bfg import testing

from eportfolio.tests import EPortfolioTestCase

class TestLoginView(EPortfolioTestCase):
    
    def test_logged_in_view(self):
        from eportfolio.models.app import Application
        from eportfolio.views.login import logged_in_view
        
        root = Application()
        
        # Not logged in
        request = testing.DummyRequest(root=root)
        response = logged_in_view(root, request)
        self.assertEquals(302, response.status_int)
        url = 'http://example.com/login.html?login_failed=1'
        self.assertEquals(url, response.headers['Location'])
        
        # Menu's 'Home' entry is used to find the homepage
        from eportfolio.views.menu import GlobalMenu
        from eportfolio.views.menu import StudentHomeEntry
        self.config.registry.registerAdapter(GlobalMenu)
        self.config.registry.registerAdapter(StudentHomeEntry, name='home')
        
        # Logged in student
        student = self._add_student()
        self.config.testing_securitypolicy(userid=student.email)
        request = testing.DummyRequest(root=root)
        response = logged_in_view(root, request)
        self.assertEquals(302, response.status_int)
        url = 'http://example.com/users/%s/' % student.id
        self.assertEquals(url, response.headers['Location'])
        
        from eportfolio.views.menu import TeacherHomeEntry
        self.config.registry.registerAdapter(TeacherHomeEntry, name='home')
        
        # Logged in teacher
        teacher = self._add_teacher()
        self.config.testing_securitypolicy(userid=teacher.email)
        request = testing.DummyRequest(root=root)
        response = logged_in_view(root, request)
        self.assertEquals(302, response.status_int)
        url = 'http://example.com/dashboard.html'
        self.assertEquals(url, response.headers['Location'])