import uuid
import sha

from zope.interface import implements

from sqlalchemy import Unicode
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import synonym, relation

from repoze.who.plugins.sql import default_password_compare

from repoze.bfg.threadlocal import get_current_registry
from repoze.bfg.settings import get_settings
from repoze.bfg import chameleon_text

from eportfolio.interfaces import IUser, IFiles, IMailService

from eportfolio.models import Base, UUID, DBSession
from eportfolio.models import DomainObject
from eportfolio.models import File
from eportfolio.models.container import Container

class User(DomainObject, Base):
    
    implements(IUser)
    
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    discriminator = Column('type', Unicode(50))
    __mapper_args__ = {'polymorphic_on': discriminator}
    
    first_name = Column(Unicode(255))
    last_name = Column(Unicode(255))
    email = Column(Unicode(255), unique=True)
    password = Column(Unicode(255))
    portrait_id = Column(UUID, ForeignKey(File.id))
    
    def _user_name(self):
        return self.email
        
    user_name = synonym('email', descriptor=property(_user_name))
    
    portrait = relation(File, backref='user', uselist=False, 
                        cascade='all,delete,delete-orphan', single_parent=True)
    
    def validate_password(self, password):
        return default_password_compare(password, self.password)
        
    def send_password_reset(self, reset_url):
        # Send password e-mail to user if password field is empty
        key = self.password_reset_key()
        reset_url = '%s?key=%s' % (reset_url, key)
        mail_text = chameleon_text.render_template('eportfolio:views/templates/pw_reset_mail.txt',
                                                   reset_url=reset_url,
                                                   first_name=self.first_name,
                                                   last_name=self.last_name)

        mail_service = get_current_registry().getUtility(IMailService)

        mail_service.send('%s %s <%s>' % (self.first_name, self.last_name, self.email),
            u'COBAL e-Portfolio Passwort',
            mail_text)
            
    def password_reset_key(self):
        settings = get_settings()
        salt = settings.get('pw_reset_salt', '')
        k = self.first_name + self.password + self.email + str(self.portrait_id) + salt
        return sha.sha(k.encode('utf-8')).hexdigest()
        
    @property
    def __name__(self):
        return str(self.id)
        
    @property
    def groups(self):
        return ()
        
    def __getitem__(self, key):
        if key == 'projects':
            session = DBSession()
            container = Container(self.projects)
            container.__parent__ = self
            container.__name__ = u'projects'
            return container
        
        if key == 'files':
            session = DBSession()
            container = Container(session.query(File), IFiles)
            container.__parent__ = self
            container.__name__ = u'files'
            return container
        
        raise KeyError(key)