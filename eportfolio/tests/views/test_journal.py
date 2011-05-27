from os.path import join, dirname

from repoze.bfg import testing

from eportfolio.tests import EPortfolioTestCase

class TestJournalView(EPortfolioTestCase):
    
    def test_journal_add_view(self):
        from eportfolio.models.app import Application
        from eportfolio.views.journal import journal_add_view
        
        root = Application()
        
        project = self._add_project()
        student = self._add_student()
        project.students.append(student)
        
        # Student is logged in
        self.config.testing_securitypolicy(userid=student.email)
        request = testing.DummyRequest(root=root)
        request.POST['text'] = u'My first journal entry!'
        request.POST['image'] = u''
        request.POST['form.submitted'] = 1
        response = journal_add_view(project, request)
        self.assertEquals(1, project.journal_entries.count())
        entry = project.journal_entries[0]
        self.assertEquals(u'My first journal entry!', entry.text)
        self.assertEquals(student, entry.user)
        # Check redirection
        self.assertEquals(302, response.status_int)
        url = 'http://example.com/users/%s/' % student.id
        self.assertEquals(url, response.headers['Location'])
        
        teacher = self._add_teacher()
        project.teachers.append(teacher)
        # Teacher is logged in
        self.config.testing_securitypolicy(userid=teacher.email)
        request = testing.DummyRequest(root=root)
        request.POST['text'] = u"Teacher's journal entry!"
        request.POST['image'] = u''
        request.POST['form.submitted'] = 1
        response = journal_add_view(project, request)
        self.assertEquals(1, teacher.journal_entries.count())
        # Check redirection
        self.assertEquals(302, response.status_int)
        url = 'http://example.com/projects/%s/' % project.id
        self.assertEquals(url, response.headers['Location'])
        
    def test_journal_add_view_image(self):
        from eportfolio.models.app import Application
        from eportfolio.views.journal import journal_add_view
        from cgi import MiniFieldStorage
        
        root = Application()
        
        project = self._add_project()
        student = self._add_student()
        project.students.append(student)
        
        # 'upload_directory' setting has to be set
        self.config.add_settings(upload_directory=join(dirname(__file__), 'data'))
        
        # Dummy repoze.filesafe data manager
        from repoze.filesafe.testing import setupDummyDataManager, cleanupDummyDataManager
        setupDummyDataManager()
        
        # Image file to upload
        image_path = join(dirname(__file__), 'data', 'image.jpg')
        fd = open(image_path, 'rb')
        storage = MiniFieldStorage('image', 'image.jpg')
        storage.file = fd
        storage.filename = 'image.jpg'
        
        # Student is logged in
        self.config.testing_securitypolicy(userid=student.email)
        request = testing.DummyRequest(root=root)
        request.POST['text'] = u'Entry with an image'
        request.POST['image'] = storage
        request.POST['form.submitted'] = 1
        journal_add_view(project, request)
        self.assertEquals(1, project.journal_entries.count())
        entry = project.journal_entries[0]
        self.assertEqual('image/jpeg', entry.image.content_type)
        
        cleanupDummyDataManager()
        
    def test_journal_add_view_indicators(self):
        from eportfolio.models.app import Application
        from eportfolio.views.journal import journal_add_view
        renderer = self.config.testing_add_template('templates/journal_add.pt')
        
        root = Application()
        
        project = self._add_project()
        student = self._add_student()
        project.students.append(student)
        indicator_set = self._add_indicator_set()
        indicator1 = self._add_indicator(title=u'First indicator', indicator_set=indicator_set)
        indicator2 = self._add_indicator(title=u'Second indicator', indicator_set=indicator_set)
        # Competences have to be added to project over objectives
        objective = self._add_objective(project=project)
        objective.competences.append(indicator_set.competence)
        
        # Student is logged in
        self.config.testing_securitypolicy(userid=student.email)
        
        request = testing.DummyRequest(root=root)
        journal_add_view(project, request)
        indicator_sets = renderer.indicator_sets
        self.assertEquals(1, len(indicator_sets))
        self.assertEquals(indicator_set.title, indicator_sets[0]['title'])
        self.assertEquals(2, len(indicator_sets[0]['indicators']))
        self.assertEquals(str(indicator1.id), indicator_sets[0]['indicators'][0]['id'])
        self.assertEquals(str(indicator2.id), indicator_sets[0]['indicators'][1]['id'])
        
        request = testing.DummyRequest(root=root)
        request.POST['text'] = u'My first journal entry!'
        request.POST['image'] = u''
        request.POST['indicators'] = [ str(indicator1.id), ]
        request.POST['form.submitted'] = 1
        journal_add_view(project, request)
        
        self.assertEquals(1, student.journal_entries.count())
        self.assertEquals(1, project.journal_entries.count())
        entry = student.journal_entries.first()
        self.assertEquals([indicator1], entry.indicators.all())
        
        # Indicator can be tagged only once, thus it's not in the list anymore.
        request = testing.DummyRequest(root=root)
        journal_add_view(project, request)
        indicator_sets = renderer.indicator_sets
        self.assertEquals(1, len(indicator_sets[0]['indicators']))
        