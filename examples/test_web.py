#!/usr/bin/env python

"""
This very ficticious example shows a cheap implementation of a web
framework built entirely using snakejuice.
"""


## start loggers.py
## Logging functionality

class Logger(object): pass
class FileLogger(Logger): pass

## start loggers.py





## start session.py
## Session in a stateful application.

from snakeguice import inject

#from loggers import Logger -- not needed in this example

class Session(object): pass
class WebSession(object):
    logger = inject(Logger)

## start session.py





## start handlers.py
## Defines handlers that are used for each request.

from snakeguice import inject

#from session import Session -- not needed in this example

class Handler(object):

    session = inject(Session)

    def handle(self, request):
        """got something!"""

class HTTPHandler(Handler): pass
class SMTPHandler(Handler): pass

## end handlers.py





## start server.py
## Basic serving functionality

from snakeguice import inject

#from handlers import Handler -- not needed in this example

class Server(object): pass

class WebServer(Server):

    handler = inject(Handler)

    def start(self):
        fake_requests = (1, 2, 3)
        for request in fake_requests:
            self.handler.handle(request)

## end server.py





## start myappmodule.py
## Defines the dependencies between classes that this application will use.

#from handlers import Handler, HTTPHandler -- not needed in this example

class MyAppModule:

    def configure(self, binder):
        binder.bind(Server).to(WebServer)
        binder.bind(Handler).to(HTTPHandler)
        binder.bind(Session).to(WebSession)
        binder.bind(Logger).to(FileLogger)

## end myappmodule.py





## start application.py
## This would be the entry point of your application.

from snakeguice import Injector

#from myappmodule import MyAppModule -- not needed in this example
#from server import Server -- not needed in this example

class Application(object):
    """Hello. I am responsible for setting up all of the application's state.
    Not only will I setup the snakeguice injector, but I may also initialize
    dataconnections or other application-wide resources.
    """
    
    def __init__(self):
        injector = Injector(MyAppModule())
        #connect_to_db()
        #read_config_files()

        self.server = injector.get_instance(Server)
        self.server.start()


## end application.py





### the actualy executed test
def test_run():
    app = Application()
    server = app.server

    # the application is done running, but lets verify the tree
    assert isinstance(server, WebServer)
    assert isinstance(server.handler, HTTPHandler)
    assert isinstance(server.handler.session, WebSession)
    assert isinstance(server.handler.session.logger, FileLogger)

