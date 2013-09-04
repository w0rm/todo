import web


class RESTfulController:
    '''web.py controller class that works with urls:
       r'/resourses(?:/(?P<resource_id>[0-9]+))?'
       and provides nice RESTful methods
    '''

    methods = ('list', 'get', 'create', 'update', 'delete',
               'update_collection', 'delete_collection')

    def __getattr__(self, name):
        if name in self.methods and 'headers' in web.ctx:
            raise web.badrequest()
        else:
            raise AttributeError

    def GET(self, resource_id=None):
        if resource_id is None:
            return self.list()
        else:
            return self.get(resource_id)

    def POST(self, resource_id=None):
        if resource_id is None:
            return self.create()
        else:
            raise web.badrequest()

    def PUT(self, resource_id=None):
        if resource_id is None:
            return self.update_collection()
        else:
            return self.update(resource_id)

    def DELETE(self, resource_id=None):
        if resource_id is None:
            return self.delete_collection()
        else:
            return self.delete(resource_id)
