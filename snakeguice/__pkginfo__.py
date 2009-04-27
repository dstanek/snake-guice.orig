"""snake-guice packaging information"""
# pylint: disable-msg=C0103,W0622

libname = 'snake-guice'
modname = 'snakeguice'
packages = ['snakeguice']

version = '0.2.1dev'

license = 'MIT'
copyright = 'Copyright (c) 2008 David Stanek (dstanek@dstanek.com)'

short_desc = 'A simple, lightweight Python dependency injection framework'
long_desc = """\
 snake-guice is a simple, lightweight Python dependency injection
 framework based on google-guice. The Guice way to do things is quite a
 bit different than the current breed of XML IoC containers."""

author = 'David Stanek'
author_email = 'dstanek@dstanek.com'

url = 'http://code.google.com/p/snake-guice'
download_url = 'http://code.google.com/p/snake-guice/downloads/list'
mailing_list = 'http://groups.google.com/group/snake-guice'

classifiers =  [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
]
