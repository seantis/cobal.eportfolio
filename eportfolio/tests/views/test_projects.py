import datetime
from repoze.bfg import testing

from eportfolio.tests import EPortfolioTestCase

class TestProjectsView(EPortfolioTestCase):
    
    def test_projects_view(self):
        from eportfolio.models.app import Application
        from eportfolio.views.projects import projects_view
        
        root = Application()
        
        # No projects yet
        request = testing.DummyRequest(root=root)
        response = projects_view(root['projects'], request)
        self.assertEquals([], response['current_projects'])
        self.assertEquals([], response['past_projects'])
        
        # Add an active project
        current_project = self._add_project()
        current_project.start_date = datetime.date.today() - datetime.timedelta(days=10)
        current_project.end_date = datetime.date.today() + datetime.timedelta(days=10)
        response = projects_view(root['projects'], request)
        self.assertEquals([current_project], response['current_projects'])
        self.assertEquals([], response['past_projects'])
        
        # Add a past project
        past_project = self._add_project()
        past_project.start_date = datetime.date.today() - datetime.timedelta(days=30)
        past_project.end_date = datetime.date.today() - datetime.timedelta(days=20)
        response = projects_view(root['projects'], request)
        self.assertEquals([current_project], response['current_projects'])
        self.assertEquals([past_project], response['past_projects'])
        
        # Check whether projects are traversal wrapped
        self.failUnless(response['current_projects'][0].__parent__)
        self.assertEquals(str(current_project.id), response['current_projects'][0].__name__)
        self.failUnless(response['past_projects'][0].__parent__)
        self.assertEquals(str(past_project.id), response['past_projects'][0].__name__)
        
    def test_projects_container(self):
        from eportfolio.models.app import Application
        from eportfolio.views.container import remove_item
        
        root = Application()
        
        # Try to remove not existing project
        request = testing.DummyRequest(root=root)
        request.POST['item'] = 'test'
        response = remove_item(root['projects'], request)
        self.assertEquals(400, response.status_int)
        
        # Add project
        project = self._add_project()
        self.assertEquals(1, len(root['projects']))
        request.POST['item'] = project.id
        response = remove_item(root['projects'], request)
        self.assertEquals(200, response.status_int)
        self.assertEquals(0, len(root['projects']))
        