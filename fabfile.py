import os
from fabric.api import task, local
from code import db


@task
def setup():
    '''Recreates database schema'''
    try:
        os.remove('db.sqlite')
    except OSError:
        pass
    schema_commands = open('schema.sql', 'r').read().split(';')
    for cmd in schema_commands:
        if cmd.strip():
            db.query(cmd)


@task
def server(port='8080'):
    '''Runs server'''
    local('python code.py %s' % port)


@task
def test():
    '''Runs tests'''
    local('nosetests')
