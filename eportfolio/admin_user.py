# -*- coding: utf-8 -*- 

# howot run it: paster admin_user eportfolio.ini 

import os
import transaction

from paste.deploy import appconfig
from paste.script.command import Command

from eportfolio.models import initialize_sql
from eportfolio.models import DBSession

from eportfolio.models import Teacher


class AddAdminUserCommand(Command):
    
    # Parser configuration
    summary = "--NO SUMMARY--"
    usage = "--NO USAGE--"
    group_name = "eportfolio"
    parser = Command.standard_parser(verbose=False)
    
    def command(self):
        self._setup_db()
        self._populate_db()
        transaction.commit()
    
    def _setup_db(self):
        config_uri = 'config:%s' % self.args[0]
        here_dir = os.getcwd()
        settings = appconfig(config_uri, name='eportfolio', relative_to=here_dir)
        db_string = settings.get('db_string')
        if db_string is None:
            raise ValueError("No 'db_string' value in application configuration.")
        initialize_sql(db_string)
    
    def _populate_db(self):
        
        session = DBSession()
        
        # Add a teacher
        ############### Change user name and email here ############### 
        if not session.query(Teacher).filter(Teacher.email == u"mail@example.com").all():
            admin = Teacher(first_name=u'Admin', last_name=u'User', email=u"mail@example.com", password=u'password')
            session.add(admin) 