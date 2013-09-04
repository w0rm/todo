# coding: utf-8

import web
import json


class APIForm(web.form.Form):
    '''Subclass web.py form to return
       validation errors in json format'''

    def serialize_errors(self):
        '''Serializes form's errors'''
        errors = []
        if self.note:
            errors.append({'note': self.note})
        for i in self.inputs:
            if i.note:
                errors.append(dict(
                    name=i.name,
                    description=i.description,
                    note=i.note,
                ))
        return {'errors': errors}

    def validation_error(self):
        '''Returns validation error'''
        return web.HTTPError(
            '400 Bad Request',
            {'Content-Type': 'application/json'},
            json.dumps(self.serialize_errors())
        )
