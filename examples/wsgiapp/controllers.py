from os import path
from mako.template import Template
from webob import Response
import formencode
from snakeguice import inject, annotate

from forms import MyForm


class BaseController(object):

    @inject(template_dir=str)
    @annotate(template_dir='base template directory')
    def __init__(self, template_dir):
        self._template_dir = template_dir

    def _load_template(self, filename):
        filename = path.join(self._template_dir, filename)
        return Template(filename=filename)


class HomeController(BaseController):

    def index(self, request):
        kwargs = dict(name='', email='', errors={})
        template = self._load_template('templates/index.mako')
        return Response(template.render(**kwargs))

    def form(self, request):
        errors = {}
        try:
            formdata = MyForm().to_python(request.POST)
        except formencode.Invalid, e:
            errors = e.unpack_errors()

        if errors:
            kwargs = dict(name=request.POST.get('name', ''),
                          email=request.POST.get('email', ''), errors=errors)
            template = self._load_template('templates/index.mako')
            return Response(template.render(**kwargs))
        else:
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            past_experience = request.POST.get('past_experience') == 'on'
            kwargs = dict(name=name, past_experience=past_experience)
            template = self._load_template('templates/thanks.mako')
            return Response(template.render(**kwargs))
