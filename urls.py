'''
This module defines application url structure
'''

urls = (

    # Todos REST api
    r'/api/todos(?:/(?P<todo_id>[0-9]+))?', 'controllers.todos.Todos',

    # Website
    '/', 'controllers.index.Index',

)
