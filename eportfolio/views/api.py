import re
import htmlentitydefs

from repoze.bfg.threadlocal import get_current_registry

from repoze.bfg.url import model_url
from repoze.bfg.security import effective_principals, has_permission
from repoze.bfg.chameleon_zpt import get_template

from eportfolio.utils import authenticated_user
from eportfolio.views.interfaces import IGlobalMenu, ILocalMenu

class TemplateAPI(object):
    
    def __init__(self, request):
        self.request = request
        self.main_template = get_template('templates/master.pt')
        self.journal_entries = get_template('templates/journal_entries.pt')
        self.application_url = request.application_url
        self.root = request.root
        
    def model_url(self, context, *elements, **kw):
        return model_url(context, self.request, *elements, **kw)
        
    def root_url(self):
        return model_url(self.root, self.request)
        
    def static_url(self, path):
        return self.model_url(self.request.root) + 'static/' + path
        
    def authenticated_user(self):
        return authenticated_user(self.request)
        
    def has_permission(self, permission, context=None):
        if not context:
            context = self.request.context
        return has_permission(permission, context, self.request)
        
    def groups(self):
        groups = [ principal for principal in effective_principals(self.request) if 'group:' in principal]
        return groups
        
    def global_menu(self):
        menu = get_current_registry().queryAdapter(self.request, IGlobalMenu)
        if menu:
            return menu.render()
        return ''
        
    def local_menu(self):
        menu = get_current_registry().queryMultiAdapter((self.request.context, self.request), ILocalMenu)
        if menu:
            return menu.render()
        return ''
        
    def statusmessage(self):
        msgs = self.request.environ.get('qc.statusmessage', [])
        if len(msgs):
            return msgs
        else:
            return None
    
    def filter_html(self, text):
       """Removes HTML or XML character references 
          and entities from a text string.
       @param text The HTML (or XML) source text.
       @return The plain text, as a Unicode string, if necessary.
       from Fredrik Lundh
       2008-01-03: input only unicode characters string.
       http://effbot.org/zone/re-sub.htm#unescape-html
       """
       def fixup(m):
          text = m.group(0)
          if text[:2] == "&#":
             # character reference
             try:
                if text[:3] == "&#x":
                   return unichr(int(text[3:-1], 16))
                else:
                   return unichr(int(text[2:-1]))
             except ValueError:
                print "Value Error"
                pass
          else:
             # named entity
             try:
                if text[1:-1] in ("amp","gt","lt"):
                    return text
                else:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
             except KeyError:
                print "keyerror"
                pass
          return text # leave as is
       return re.sub("&#?\w+;", fixup, text) 