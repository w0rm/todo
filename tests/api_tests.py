
import os
import web
import urllib
import urllib2
import json

from nose.tools import assert_in, assert_not_in, assert_equals
import nose

# Swtich into a testing environment
os.environ['WEBPY_ENV'] = 'test'

# Import app to test
from code import app


class TestBrowser(web.browser.AppBrowser):
    '''Subclassed AppBrowser to add @method param'''

    def open(self, url, data=None, headers={}, method='GET'):
        """Opens the specified url."""
        url = urllib.basejoin(self.url, url)
        req = urllib2.Request(url, data, headers)
        req.get_method = lambda: method
        print method
        return self.do_request(req)


class TestApi():

    def setup(self):
        self.b = TestBrowser(app)

    def teardown(self):
        self.b.reset()

    def test_list_todos(self):
        response = self.b.open('/api/todos')
        assert_equals(self.b.status, 200)
        assert_equals(response.headers['Content-Type'], 'application/json')
        todos = json.loads(self.b.data)
        assert_equals(isinstance(todos, list), True)

    def test_create_todo(self):
        response = self.b.open(
            '/api/todos',
            data={'title': 'Test TODO'},
            method='POST'
        )
        assert_equals(self.b.status, 200)
        assert_equals(response.headers['Content-Type'], 'application/json')
        todo = json.loads(self.b.data)
        assert_equals(isinstance(todo, dict), True)
