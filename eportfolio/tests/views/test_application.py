from repoze.bfg import testing

from eportfolio.tests import EPortfolioTestCase

class TestApplicationView(EPortfolioTestCase):
    
    def test_application_view(self):
        from eportfolio.models.app import Application
        from eportfolio.views.application import application_view
        
        root = Application()
        
        # Redirect to login view if not authenticated
        request = testing.DummyRequest(root=root)
        response = application_view(root, request)
        self.assertEquals(302, response.code)
        self.assertEquals('http://example.com/login.html', response.headers['Location'])
        
        # Logged in student
        student = self._add_student()
        self.config.testing_securitypolicy(userid=student.email)
        response = application_view(root, request)
        self.assertEquals(302, response.status_int)
        url = 'http://example.com/users/%s/' % student.id
        self.assertEquals(url, response.headers['Location'])
        
        # Logged in teacher
        teacher = self._add_teacher()
        self.config.testing_securitypolicy(userid=teacher.email)
        response = application_view(root, request)
        self.assertEquals(302, response.status_int)
        self.assertEquals('http://example.com/dashboard.html', response.headers['Location'])