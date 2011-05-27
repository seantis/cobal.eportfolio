import sha

import formencode
from formencode import htmlfill
from webob import Response
from webob.exc import HTTPFound

from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.url import model_url

from eportfolio.views import statusmessage
from eportfolio.views.api import TemplateAPI     

from eportfolio.models import DBSession, get_root
from eportfolio.models import User

class UsernameFound(formencode.FancyValidator):
  def _to_python(self, value, state):
      session = DBSession()
      if not session.query(User).filter_by(email=value).all():
          raise formencode.Invalid('Username not found.', value, state)
      return value

class PWResetRequestSchema(formencode.Schema):
    allow_extra_fields = True
    email = formencode.All(formencode.validators.Email(not_empty=True), UsernameFound())
    
class PWResetSchema(PWResetRequestSchema):
    password = formencode.validators.String(not_empty=True)
    
def view_pw_reset(context, request):
    
    # Second step: User is visiting reset url
    if 'key' in request.params:
        key = request.params['key']
        
        if 'form.submitted' in request.params:
            try:
                # FormEncode validation
                schema = PWResetSchema()
                form_result = schema.to_python(request.params)
            except formencode.validators.Invalid, why:
                form = render_template('templates/password_reset.pt', request=request, api=TemplateAPI(request))
                # FormEncode fills template with error messages
                form = htmlfill.render(form, defaults=request.params, errors=why.error_dict)
                return Response(form)
            else:
                session = DBSession()
                user = session.query(User).filter_by(email=form_result['email']).one()
                if key == user.password_reset_key():
                    user.password = '{SHA}%s' % sha.new(form_result['password'].encode('utf-8')).hexdigest()
                    # Login directly
                    headers = []
                    plugins = request.environ.get('repoze.who.plugins', {})
                    identifier = plugins.get('auth_tkt')
                    if identifier:
                        identity = {'repoze.who.userid': form_result['email']}
                        headers = identifier.remember(request.environ, identity)
                    request.environ['repoze.who.userid'] = form_result['email']
                    return HTTPFound(location = model_url(context, request), headers=headers)
                else:
                    statusmessage.show(request, u"Retrieve request not valid.", u"error")
        
        return render_template_to_response('templates/password_reset.pt', request=request, api=TemplateAPI(request))
    
    # First step: Create and send reset url
    if 'form.submitted' in request.params:
        try:
            # FormEncode validation
            schema = PWResetRequestSchema()
            form_result = schema.to_python(request.params)
        except formencode.validators.Invalid, why:
            form = render_template('templates/password_retrieve.pt', request = request, api=TemplateAPI(request),)
            # FormEncode fills template with error messages
            form = htmlfill.render(form, defaults=request.params, errors=why.error_dict)
            return Response(form)
        else:
            session = DBSession()
            user = session.query(User).filter_by(email=form_result['email']).one()
            reset_url = model_url(get_root(request), request, 'retrieve_password.html')
            user.send_password_reset(reset_url)
                       
            statusmessage.show(request, u'Password retrieval e-mail sent.')
            return HTTPFound(location = model_url(context, request))
    
    return render_template_to_response('templates/password_retrieve.pt', request=request, api=TemplateAPI(request))
