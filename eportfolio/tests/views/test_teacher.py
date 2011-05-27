from repoze.bfg import testing

from eportfolio.tests import EPortfolioTestCase

class TestTeacherEditView(EPortfolioTestCase):
    
    def test_teacher_add_view(self):
        from eportfolio.models.app import Application
        from eportfolio.views.teacher import teacher_edit_view
        
        root = Application()
        
        request = testing.DummyRequest(root=root)
        response = teacher_edit_view(root['users'], request)
        self.failUnless('Add' in response.body)
        
        request = testing.DummyRequest(root=root)
        request.params['form.submitted'] = 1
        request.params['first_name'] = u'Buck'
        request.params['last_name'] = u'Mulligan'
        request.params['email'] = u'buck@seantis.ch'
        request.params['password'] = u''
        request.params['portrait'] = u''
        # Empty password field triggers registration mail
        teacher_edit_view(root['users'], request)
        registration_mail = self.mailer.mails[-1]
        mail_address = '%s %s <%s>' % (u'Buck', u'Mulligan', u'buck@seantis.ch')
        self.assertEquals(mail_address, registration_mail['To'])
        
    def test_teacher_edit_view(self):
        from eportfolio.models.app import Application
        from eportfolio.views.teacher import teacher_edit_view
        
        root = Application()
        teacher = self._add_teacher()
        
        request = testing.DummyRequest(root=root)
        response = teacher_edit_view(root['users'][teacher.id], request)
        self.failUnless('Edit' in response.body)
        
        request = testing.DummyRequest(root=root)
        request.params['form.submitted'] = 1
        request.params['first_name'] = u'Leopold'
        request.params['last_name'] = u'Bloom'
        request.params['email'] = u'leopold@seantis.ch'
        request.params['portrait'] = u''
        teacher_edit_view(root['users'][teacher.id], request)
        self.assertEquals(u'Leopold', teacher.first_name)
        self.assertEquals(u'Bloom', teacher.last_name)
        self.assertEquals(u'leopold@seantis.ch', teacher.email)