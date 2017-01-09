from distutils.core import setup

setup(name='configen',
      version='1.0',
      description='Generate config by templates and database query',
      author='Martin Miksanik',
      author_email='miksanik@gmail.com',
      url='https://github.com/euroska/configen',
      packages=['configen'],
      install_requires=[
          'jinja2',
          'sqlalchemy',
          'psycopg2',
          'pyyaml'
      ],
      scripts= ['bin/configen'],
)
