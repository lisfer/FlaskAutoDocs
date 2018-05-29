import unittest

from flask import Flask
from flask_auto_docs import FlaskAutoDocs



def fixture_simple():
    pass


def fixture_full(person_id:int):
    """
    Function changes name and age of the person
    it its' cool: it can do amazing stuff

    and so on
    :params person_id: id of the person
    :api_param name: name of the person to be set
    :api_param age: new age for the person
    :return: true of false
        and many other interesting stuff
    """

def fixture_mixing(person_id:int):
    """
    Function changes name and age of the person
    it its' cool: it can do amazing stuff

    and so on
    :params person_id: id of the person
    :api_param name: name of the person to be set
        api_param row 2
    :params test1: test
        params row 2
    :api_param age: new age for the person
    :params test2: test
    :return: true of false
        and many other interesting stuff
    """


class FlaskAutoDocTest(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        self.fad = FlaskAutoDocs(app)
        app.route('/api')(self.fad.doc(fixture_simple))
        app.route('/api/person/<int:person_id>', methods=['POST'])(self.fad.doc(fixture_full))
        app.route('/api/person/<int:person_id>', methods=['POST'])(self.fad.doc(fixture_mixing))

    def test_empty_function(self):
        fs = self.fad.get('fixture_simple')
        assert fs['url'] == '/api'
        assert fs['description'] == ''
        assert fs['methods'] == {'HEAD', 'OPTIONS', 'GET'}
        assert fs['return'] == ''
        assert fs['params'] == {}

    def test_described_function(self):
        ff = self.fad.get('fixture_full')
        assert ff['url'] == '/api/person/<int:person_id>'
        assert ff['description'] == "Function changes name and age of the person\n    it its' cool: it can do amazing stuff\n\n    and so on"
        assert ff['methods'] == {'POST', 'OPTIONS'}
        assert ff['return'] == 'true of false\n        and many other interesting stuff'
        assert ff['params'] == {'name': 'name of the person to be set', 'age': 'new age for the person'}

    def test_mixed_function(self):
        ff = self.fad.get('fixture_mixing')
        assert ff['url'] == '/api/person/<int:person_id>'
        assert ff['description'] == "Function changes name and age of the person\n    it its' cool: it can do amazing stuff\n\n    and so on"
        assert ff['methods'] == {'POST', 'OPTIONS'}
        assert ff['return'] == 'true of false\n        and many other interesting stuff'
        assert ff['params'] == {'name': 'name of the person to be set\n        api_param row 2', 'age': 'new age for the person'}

