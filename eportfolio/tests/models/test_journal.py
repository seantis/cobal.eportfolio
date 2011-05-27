from eportfolio.tests import EPortfolioTestCase

class TestJournalEntry(EPortfolioTestCase):
    
    def test_acl(self):
        from eportfolio.models import Student
        from eportfolio.models import JournalEntry
        
        from eportfolio.security.journal import JournalEntryPermissions
        self.config.registry.registerAdapter(JournalEntryPermissions)
        
        student = Student(email=u'buck@seantis.ch')
        
        entry = JournalEntry()
        entry.user = student
        
        # Only the author of the journal entry can edit it.
        acl = [
            ('Allow', u'buck@seantis.ch', 'edit'),
            ('Deny', 'system.Everyone', 'edit'),
            ('Allow', u'buck@seantis.ch', 'remove'), 
        ]
        
        self.assertEquals(acl, entry.__acl__)