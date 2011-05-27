# -*- coding: utf-8 -*-

from repoze.bfg import testing

from eportfolio.tests import EPortfolioTestCase, AuthTktCookiePluginDummy

class PasswordResetViewTests(EPortfolioTestCase):
    
    def setUp(self):
        super(PasswordResetViewTests, self).setUp()
        self.config.add_route('', '/', factory=None)
    
    def test_view_pw_reset(self):
        from eportfolio.models.app import Application
        from eportfolio.views.pw_reset import view_pw_reset
        
        root = Application()
        
        # Call the view
        request = testing.DummyRequest(root=root)
        view_pw_reset(root, request)
        
        # No email address given
        request = testing.DummyRequest(root=root)
        request.params['form.submitted'] = 1
        response = view_pw_reset(root, request)
        self.failUnless('class="error"' in response.body)
        
        # Email address not found
        request = testing.DummyRequest(root=root)
        request.params['form.submitted'] = 1
        request.params['email'] = u'buck@mulligan.com'
        response = view_pw_reset(root, request)
        self.failUnless('class="error"' in response.body)
        self.failUnless('Username not found.' in response.body)
        
        student = self._add_student()
        student.first_name = u'Buck'
        student.last_name = u'Mulligan'
        student.email = u'buck@seantis.ch'
        request = testing.DummyRequest(root=root)
        request.params['form.submitted'] = 1
        request.params['email'] = student.email
        response = view_pw_reset(root, request)
        # Check whether mail has been sent
        retrieval_mail = self.mailer.mails[-1]
        mail_address = '%s %s <%s>' % (student.first_name, student.last_name, student.email)
        self.assertEquals(mail_address, retrieval_mail['To'])
        self.failUnless(student.password_reset_key() in retrieval_mail.get_payload(decode=True))
        
        # Try to reset with wrong key
        request = testing.DummyRequest(root=root)
        request.params['form.submitted'] = 1
        request.params['email'] = student.email
        request.params['password'] = u'123456'
        request.params['key'] = '068e16b2e986c41d19ee7bba54cf40ed0d8dfc46'
        response = view_pw_reset(root, request)
        self.failUnless('Reset Password' in response.body)
        
        # Try to set an empty password
        request = testing.DummyRequest(root=root)
        request.params['form.submitted'] = 1
        request.params['email'] = student.email
        request.params['password'] = u''
        request.params['key'] = student.password_reset_key() + 'e'
        response = view_pw_reset(root, request)
        self.failUnless('Reset Password' in response.body)
        
         # Reset with correct key
        request = testing.DummyRequest(root=root)
        request.params['form.submitted'] = 1
        request.params['email'] = student.email
        request.params['password'] = u'müller1234'
        request.params['key'] = student.password_reset_key()
        # Dummy auth plugin to check direct login.
        auth_plugin = AuthTktCookiePluginDummy()
        request.environ['repoze.who.plugins'] = dict(auth_tkt=auth_plugin)
        response = view_pw_reset(root, request)
        self.assertEquals(302, response.status_int)
        self.assertEquals('http://example.com/', response.headers['Location'])
        self.assertEquals({'repoze.who.userid': student.email}, auth_plugin.identity)