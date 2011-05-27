from urllib import urlencode

from paste.httpexceptions import HTTPFound, HTTPUnauthorized
from paste.request import parse_dict_querystring, parse_formvars

from repoze.who.plugins.friendlyform import FriendlyFormPlugin as BasePlugin

class FriendlyFormPlugin(BasePlugin):
    """
    Friendly form plugin that ignores case of the username.
    """
    
    # IIdentifier
    def identify(self, environ):
        """
        Override the parent's identifier to introduce a login counter
        (possibly along with a post-login page) and load the login counter into
        the ``environ``.
        
        """
        
        path_info = environ['PATH_INFO']
        script_name = environ.get('SCRIPT_NAME') or '/'
        query = parse_dict_querystring(environ)
        
        if path_info == self.login_handler_path:
            ## We are on the URL where repoze.who processes authentication. ##
            # Let's append the login counter to the query string of the
            # "came_from" URL. It will be used by the challenge below if
            # authorization is denied for this request.
            form = parse_formvars(environ)
            form.update(query)
            try:
                credentials = {
                    'login': form['login'].lower(),
                    'password': form['password']
                    }
            except KeyError:
                credentials = None
            referer = environ.get('HTTP_REFERER', script_name)
            destination = form.get('came_from', referer)
            
            if self.post_login_url:
                # There's a post-login page, so we have to replace the
                # destination with it.
                destination = self._get_full_path(self.post_login_url,
                                                  environ)
                if 'came_from' in query:
                    # There's a referrer URL defined, so we have to pass it to
                    # the post-login page as a GET variable.
                    destination = self._insert_qs_variable(destination,
                                                           'came_from',
                                                           query['came_from'])
            failed_logins = self._get_logins(environ, True)
            new_dest = self._set_logins_in_url(destination, failed_logins)
            environ['repoze.who.application'] = HTTPFound(new_dest)
            return credentials

        elif path_info == self.logout_handler_path:
            ##    We are on the URL where repoze.who logs the user out.    ##
            form = parse_formvars(environ)
            form.update(query)
            referer = environ.get('HTTP_REFERER', script_name)
            came_from = form.get('came_from', referer)
            # set in environ for self.challenge() to find later
            environ['repoze.who.application'] = HTTPUnauthorized()
            return None
            
        elif path_info == self.login_form_url or self._get_logins(environ):
            ##  We are on the URL that displays the from OR any other page  ##
            ##   where the login counter is included in the query string.   ##
            # So let's load the counter into the environ and then hide it from
            # the query string (it will cause problems in frameworks like TG2,
            # where this unexpected variable would be passed to the controller)
            environ['repoze.who.logins'] = self._get_logins(environ, True)
            # Hiding the GET variable in the environ:
            if self.login_counter_name in query:
                del query[self.login_counter_name]
                environ['QUERY_STRING'] = urlencode(query, doseq=True)


def make_plugin(login_form_url, login_handler_path, logout_handler_path,
                rememberer_name, post_login_url=None, post_logout_url=None, 
                login_counter_name=None):
    
    if login_form_url is None:
        raise ValueError(
            'must include login_form_url in configuration')
    if login_handler_path is None:
        raise ValueError(
            'login_handler_path must not be None')
    if logout_handler_path is None:
        raise ValueError(
            'logout_handler_path must not be None')
    if rememberer_name is None:
        raise ValueError(
            'must include rememberer key (name of another IIdentifier plugin)')
    plugin = FriendlyFormPlugin(login_form_url, 
                                login_handler_path, 
                                post_login_url,
                                logout_handler_path, 
                                post_logout_url, 
                                rememberer_name,
                                login_counter_name)
    return plugin