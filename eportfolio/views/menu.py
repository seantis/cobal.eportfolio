from zope.interface import Interface, implements
from zope.component import adapts

from repoze.bfg.threadlocal import get_current_registry
from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url
from repoze.bfg.interfaces import IRequest
from repoze.bfg.i18n import TranslationStringFactory

from eportfolio.utils import authenticated_user
from eportfolio.interfaces import IStudent, IProject, ITeacher, IUser
from eportfolio.views.interfaces import IGlobalMenu, ILocalMenu
from eportfolio.views.interfaces import IGlobalMenuEntry, ILocalMenuEntry 

_ = TranslationStringFactory('eportfolio')

class GlobalMenu(object):
    
    implements(IGlobalMenu)
    adapts(IRequest)
    
    def __init__(self, request):
        self.request = request
        
    @property
    def entries(self):
        user = authenticated_user(self.request)
        entries = get_current_registry().getAdapters((user, self.request), IGlobalMenuEntry)
        entries = [ entry[1] for entry in entries ]
        entries = [ entry for entry in entries if entry.condition ]
        entries = sorted(entries, key=lambda entry: entry.weight)
        return entries
        
    def render(self):
        return render_template("templates/global_menu.pt",
                               entries=self.entries)

class LocalMenu(object):
    
    implements(ILocalMenu)
    adapts(Interface, Interface)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    @property
    def entries(self):
        context = self.context
        user = authenticated_user(self.request)
        entries = get_current_registry().getAdapters((context, user, self.request), ILocalMenuEntry)
        entries = [ entry[1] for entry in entries ]
        while not entries and context is not None:
            context = context.__parent__
            entries = get_current_registry().getAdapters((context, user, self.request), ILocalMenuEntry)
            entries = [ entry[1] for entry in entries ]
        
        entries = [ entry for entry in entries if entry.condition ]
        entries = sorted(entries, key=lambda entry: entry.weight)
        return entries
        
    def render(self):
        return render_template("templates/local_menu.pt",
                               entries=self.entries)
           
# Global menu entries
                               
class MenuEntry(object):
    """
    Base class for menu entries.
    """
    
    url = ''
    title = ''
    weight = 0
    condition = True
    active = False
    
    @property
    def active(self):
        return self.url in self.request.path_url
    

class GlobalMenuEntry(MenuEntry):
    """
    Base class for global menu entries.
    """
    
    implements(IGlobalMenuEntry)
    adapts(IUser, IRequest)
    
    def __init__(self, user, request):
        self.user = user
        self.request = request
                               
class StudentHomeEntry(GlobalMenuEntry):
    
    title = _('Home')
    active = False
    adapts(IStudent, IRequest)
    weight = 10
    
    @property
    def url(self):
        return model_url(self.user, self.request)
        
class TeacherHomeEntry(GlobalMenuEntry):
    
    title = _('Home')
    active = False
    adapts(ITeacher, IRequest)
    weight = 10
    
    @property
    def url(self):
        return model_url(self.request.root, self.request, 'dashboard.html')
        
class ProjectsEntry(GlobalMenuEntry):
    
    title = _('Projects')
    adapts(ITeacher, IRequest)
    weight = 20
    
    @property
    def url(self):
        return model_url(self.request.root, self.request, 'projects')
        
class UsersEntry(GlobalMenuEntry):
    
    title = _('Users')
    adapts(ITeacher, IRequest)
    weight = 30
    
    @property
    def url(self):
        return model_url(self.request.root, self.request, 'users')
        
class CompetencesEntry(GlobalMenuEntry):
    
    title = _('Competences')
    adapts(ITeacher, IRequest)
    weight = 40
    
    @property
    def url(self):
        return model_url(self.request.root, self.request, 'competences')

#
# Local menu entries
#

class LocalMenuEntry(MenuEntry):
    """
    Base class for local menu entries.
    """
    
    implements(ILocalMenuEntry)
    
    def __init__(self, context, user, request):
        self.context = context
        self.user = user
        self.request = request

# Student

class ActivityEntry(LocalMenuEntry):
    
    adapts(IStudent, IStudent, IRequest)
    title = _('Activity')
    weight = 10
    
    @property
    def url(self):
        return model_url(self.context, self.request)
        
    @property
    def active(self):
        return self.url.rstrip('/') == self.request.path_url.rstrip('/')

class ProfileEntry(LocalMenuEntry):
    
    adapts(IStudent, IUser, IRequest)
    title = _('Profile')
    weight = 20
    
    @property
    def url(self):
        return model_url(self.context, self.request, 'edit.html')
        
class ApplicationEntry(LocalMenuEntry):
    
    adapts(IStudent, IUser, IRequest)
    title = _('Job Application')
    weight = 30
    
    @property
    def url(self):
        return model_url(self.context, self.request, 'application.html')
        
class StudentCompetencesEntry(LocalMenuEntry):
    
    adapts(IStudent, IUser, IRequest)
    title = _('Competences')
    weight = 40
    
    @property
    def url(self):
        return model_url(self.context, self.request, 'stats.html')
        
class StudentProjectsEntry(LocalMenuEntry):

    adapts(IStudent, IUser, IRequest)
    title = _('Projects')
    weight = 50

    @property
    def url(self):
        return model_url(self.context, self.request, 'projects_info.html')  
        
# Project

class ActivitiesEntry(LocalMenuEntry):
    
    adapts(IProject, ITeacher, IRequest)
    title = _('Activities')
    weight = 10
    
    @property
    def url(self):
        return model_url(self.context, self.request)
    
    @property
    def active(self):
        return self.url.rstrip('/') == self.request.path_url.rstrip('/')

class MembersEntry(LocalMenuEntry):
    
    adapts(IProject, ITeacher, IRequest)
    title = _('Members')
    weight = 20
    
    @property
    def url(self):
        return model_url(self.context, self.request, 'members.html')
        
class ObjectivesEntry(LocalMenuEntry):
    
    adapts(IProject, ITeacher, IRequest)
    title = _('Objectives')
    weight = 30
    
    @property
    def url(self):
        return model_url(self.context, self.request, 'objectives')
    