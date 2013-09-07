# coding: utf-8

import os
import web
import nose
from nose.tools import assert_in, assert_not_in, assert_equals
from modules.json_browser import JSONAppBrowser

# Swtich into a testing environment
os.environ['WEBPY_ENV'] = 'test'

# Import app to test
from code import app


class TestApi():

    def setup(self):
        self.b = JSONAppBrowser(app)

    def teardown(self):
        self.b.reset()

    def test_list_todos(self):
        response = self.b.json_open('/api/todos')
        assert_equals(self.b.status, 200)
        assert_equals(response.headers['Content-Type'], 'application/json')
        todos = self.b.json_data
        assert_equals(isinstance(todos, list), True)

    def test_create_and_get_todo(self):
        # Create todo
        self.b.json_open(
            '/api/todos',
            data={'content': 'Test TODO'},
            method='POST'
        )
        todo = self.b.json_data
        assert_equals(todo['content'], 'Test TODO')
        self.b.json_open('/api/todos/%(id)d' % todo)
        todo2 = self.b.json_data
        assert_equals(todo2['content'], 'Test TODO')

    def test_validation_on_create(self):
         # Try to create todo
        self.b.json_open(
            '/api/todos',
            data={'content': 'Small'},
            method='POST'
        )
        assert_equals(self.b.status, 400)
        error = self.b.json_data[0]
        assert_equals(error['name'], 'content')
        assert_equals(error['note'], 'Content length must be greater than 7')

    def test_create_and_update_todo(self):
        # Create todo
        self.b.json_open(
            '/api/todos',
            data={'content': 'Test TODO'},
            method='POST'
        )
        todo = self.b.json_data
        assert_equals(todo['content'], 'Test TODO')
        assert_equals(todo['is_done'], False)
        # Update todo and ensure it was changed
        self.b.json_open(
            '/api/todos/%(id)d' % todo,
            data={'content': 'Test TODO 2', 'is_done': True},
            method='PUT'
        )
        todo2 = self.b.json_data
        assert_equals(todo2['content'], 'Test TODO 2')
        assert_equals(todo2['is_done'], True)

    def test_create_and_delete_todo(self):
        # Create todo to ensure db is not empty
        self.b.json_open(
            '/api/todos',
            data={'content': 'Test TODO'},
            method='POST'
        )
        # Select all todos
        self.b.json_open('/api/todos')
        # Delete first todo
        todo = self.b.json_data[0]
        self.b.json_open('/api/todos/%(id)d' % todo, method='DELETE')
        # Select todos again
        self.b.json_open('/api/todos')
        # Ensure deleted todo is not present in list
        todos = self.b.json_data
        assert_equals(any(t['id'] == todo['id'] for t in todos), False)

    def test_get_inexistent_todo(self):
        todo_id = 123456
        # Ensure it doesn't exist
        self.b.json_open('/api/todos/%d' % todo_id, method='DELETE')
        result = self.b.json_open('/api/todos/%d' % todo_id)
        assert_equals(self.b.status, 404)
