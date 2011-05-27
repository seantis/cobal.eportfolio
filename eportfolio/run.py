from apscheduler.scheduler import Scheduler
from repoze.bfg.configuration import Configurator

from eportfolio.models import get_root
from eportfolio.models import initialize_sql
from eportfolio.models.file import removal_extension

import patches

def app(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    zcml_file = settings.get('configure_zcml', 'configure.zcml')
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    initialize_sql(db_string)
    config = Configurator(root_factory=get_root, settings=settings)
    config.begin()
    config.load_zcml(zcml_file)
    config.end()
    # Ugly hack to configure the MapperExtension with the settings.
    removal_extension.path = settings.get('upload_directory')
    
    scheduler = Scheduler()
    # Send out queued mails
    from eportfolio.utilities.mail_delivery import trigger_queued_delivery
    scheduler.add_interval_job(trigger_queued_delivery, seconds=30)
    scheduler.start()
    
    return config.make_wsgi_app()

