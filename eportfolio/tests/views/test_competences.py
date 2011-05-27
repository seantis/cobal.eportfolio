import datetime
from repoze.bfg import testing

from eportfolio.tests import EPortfolioTestCase

class TestProjectsView(EPortfolioTestCase):
    
    def test_competences_container(self):
        from eportfolio.models.app import Application
        from eportfolio.views.container import remove_item
        
        root = Application()
        
        # Add competence
        meta_competence = self._add_meta_competence()
        competence = self._add_competence(meta_competence=meta_competence)
        self.assertEquals(1, len(root['competences']))
        # Remove competence
        request = testing.DummyRequest(root=root)
        request.POST['item'] = competence.id
        response = remove_item(root['competences'], request)
        self.assertEquals(200, response.status_int)
        self.assertEquals('success', response.body)
        self.assertEquals(0, len(root['competences']))
        