# coding: utf-8
import web
from modules.json_controller import JSONController
from modules.json_form import (JSONForm, NotFoundError,
                               BooleanInput, StringInput)


class Todos(JSONController):

    Form = JSONForm(
        BooleanInput('is_done'),
        StringInput('content'),
    )

    def list(self):
        '''Select todos from database'''
        return web.ctx.db.select('todos').list()

    def get(self, todo_id):
        '''Select todo by id'''
        todo = web.ctx.db.select('todos', where="id = $todo_id",
                                 vars=locals()).list()
        if todo:
            return todo[0]
        else:
            raise NotFoundError()

    def create(self):
        '''Create new todo'''
        form = self.Form()
        if form.validates():
            todo_id = web.ctx.db.insert('todos', **form.d)
            return self.get(todo_id)

    def update(self, todo_id):
        '''Update todo by id and redirect to its url'''
        form = self.Form()
        if form.validates():
            todo = self.get(todo_id)
            web.ctx.db.update('todos', where='id = $todo_id',
                              vars=locals(), **form.d)
            todo.update(**form.d)
            return todo

    def delete(self, todo_id):
        '''Delete todo by id'''
        todo = self.get(todo_id)
        web.ctx.db.delete('todos', where='id = $todo_id', vars=locals())
        return {}
