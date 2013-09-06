# coding: utf-8
import web
import json


class ValidationError(web.HTTPError):
    '''`400 Bad Request` error.'''

    headers = {'Content-Type': 'application/json'}

    def __init__(self, errors, headers=None):
        status = '400 Bad Request'
        message = json.dumps(errors)
        web.HTTPError.__init__(self, status, headers or self.headers,
                               unicode(message))


class NotFoundError(web.HTTPError):
    '''`404 Not Found` error.'''

    headers = {'Content-Type': 'application/json'}

    def __init__(self, note='Not Found', headers=None):
        status = '404 Not Found'
        message = json.dumps([{'note': note}])
        web.HTTPError.__init__(self, status, headers or self.headers,
                               unicode(message))


class JSONForm(web.form.Form):
    '''Subclass web.py form to parse json input
       and raise validation errors in json format'''

    def serialize_errors(self):
        '''Serializes form's errors'''
        errors = []
        if self.note:
            errors.append({'note': self.note})
        for i in self.inputs:
            if i.note:
                errors.append({'name': i.name, 'note': i.note})
        return errors

    def validates(self, source=None, _validate=True, **kw):
        if not (source or kw):
            try:
                # Try to parse json request
                source = json.loads(web.data())
            except:
                # Assume empty request
                pass

        if super(JSONForm, self).validates(source, _validate, **kw):
            return True
        else:
            raise ValidationError(self.serialize_errors())


class Input(web.form.Input):
    '''Base input class'''


class BooleanInput(Input):
    '''Processes boolean input'''

    def __init__(self, name, *validators, **attrs):
        self.checked = attrs.pop('checked', False)
        super(BooleanInput, self).__init__(name, *validators, **attrs)

    def set_value(self, value):
        if value in ('0', 'false'):
            self.checked = False
        else:
            self.checked = bool(value)

    def get_value(self):
        return self.checked


class StringInput(Input):
    '''Processes string input'''
