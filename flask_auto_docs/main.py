import os
import re

from flask import render_template


class FlaskAutoDocs:

    RE_GET_RETURN = re.compile(r'(?<=:return:)\s*(.*)', re.DOTALL)
    RE_GET_DESCRIPTION = re.compile(r'\s+(?P<data>.+?)?\s+(?=:params|:api_param|:return|$)', re.DOTALL)
    RE_GET_API_PARAMS = re.compile(
        r'(?<=:api_param) ((?P<p_name>.+?): (?P<p_descr>.+?))\s+(?=:params|:api_param|:return|$)', re.DOTALL)

    def __init__(self, flask_app):
        self._data = dict()
        self.flask_app = flask_app
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.flask_app.jinja_loader.searchpath.append(template_path)

    def doc(self, func):
        self._data[func.__name__] = func
        return func

    @classmethod
    def default_description(self):
        return {'description': '', 'url':'', 'methods': set(), 'return': '', 'params': dict()}

    def get(self, name):
        f_descr = self.default_description()
        func = self._data.get(name)

        if not func:
            return f_descr

        if func.__doc__:
            f_descr['description'] = self._get_description(func.__doc__)
            f_descr['return'] = self._get_return(func.__doc__)
            f_descr['params'] = self._get_params(func.__doc__)

        f_descr['url'] = self._get_url(func)
        f_descr['methods'] = self._get_methods(func)
        return f_descr

    def _get_route_rule(self, name):
        return self.flask_app.url_map._rules_by_endpoint.get(name)

    def _get_url(self, func):
        rule = self._get_route_rule(func.__name__)
        return rule[0].rule if rule else ''

    def _get_methods(self, func):
        rule = self._get_route_rule(func.__name__)
        return rule[0].methods if rule else ''

    @classmethod
    def _get_description(cls, docstring):
        data = cls.RE_GET_DESCRIPTION.search(docstring) or ''
        return data.groups('data')[0] if data else ''

    @classmethod
    def _get_return(cls, docstring):
        return (cls.RE_GET_RETURN.findall(docstring)[0] or '').strip()

    @classmethod
    def _get_params(cls, docstring):
        data = {m.group('p_name'): m.group('p_descr') for m in cls.RE_GET_API_PARAMS.finditer(docstring)}
        return data

    def html(self):
        return render_template('flask_auto_docs.html', endpoints=[self.get(name) for name in self._data])
