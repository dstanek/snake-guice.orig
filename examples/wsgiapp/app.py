import sys
from wsgiref.simple_server import make_server
from snakeguice import Injector
from snakeguice.extras.snakeweb import Application

from modules import MainModule, URLMapperModule


def main(args):
    injector = Injector([MainModule(), URLMapperModule()])
    application = Application(injector)

    httpd = make_server('', 8000, application)
    httpd.serve_forever()


if __name__ == '__main__':
    main(sys.argv[1:])
