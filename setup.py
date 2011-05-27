import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'Chameleon==1.2.12',
    'repoze.bfg>=1.3a3',
    'SQLAlchemy==0.6.4',
    'transaction',
    'repoze.tm2',
    'zope.sqlalchemy',
    'FormEncode',
    'repoze.who>=2.0a2',
    'repoze.filesafe',
    'repoze.who.plugins.sa',
    'repoze.who-friendlyform',
    'WebError',
    'PIL',
    'z3c.rml',
    'Babel',
    'nose',
    'coverage',
    'repoze.sendmail',
    'qc.statusmessage',
    'APScheduler',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='eportfolio',
      version='0.1',
      description='eportfolio',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: BFG",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='eportfolio',
      install_requires = requires,
      message_extractors = { '.': [
             ('**.py', 'chameleon_python', None ),
             ('**.pt', 'chameleon_xml', None ),
             ]},
      entry_points = """\
      [paste.app_factory]
      app = eportfolio.run:app
      [paste.paster_command]
      admin_user = eportfolio.admin_user:AddAdminUserCommand
      populate_db = eportfolio.populate_db:PopulateDBCommand
      """
      )

