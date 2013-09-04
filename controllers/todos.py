import json
import web
from modules.restful_controller import RESTfulController


class Todos(RESTfulController):

    def list(self):
        '''Select todos from database and return json'''
        todos = []
        web.header('Content-Type', 'application/json')
        return json.dumps(todos)

    def get(self, todo_id):
        '''Select todo by id and return json'''
        todo = dict(id=todo_id)
        web.header('Content-Type', 'application/json')
        return json.dumps(todo)

    def create(self):
        '''Create new todo and redirect to its url'''
        raise web.seeother('/api/todos/5')

    def update(self, todo_id):
        '''Update todo by id and redirect to its url'''
        raise web.seeother('/api/todos/%s' % todo_id)

    def delete(self, todo_id):
        '''Delete todo by id'''
        pass
