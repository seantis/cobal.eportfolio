Installing cobal.eportfolio
===========================

Create and activate virtualenv:

    % virtualenv --no-site-packages eportfolio
    % cd eportfolio
    % source bin/activate

Get cobal.eportfolio:

    % git clone git://github.com/seantis/cobal.eportfolio.git eportfolio

Install cobal.eportfolio:

    % python setup.py develop

Rename eportfolio.ini.example to eportfolio.ini and change settings (email, pw_reset_salt)

Create first user by setting your username and password in eportfolio/admin_user.py 
and running the following command afterwards:

    % paster admin_user eportfolio.ini

Start eportfolio:

    % paster serve eportfolio.ini