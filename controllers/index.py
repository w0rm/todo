from template import render


class Index:

    def GET(self, path=None):
        return render.index()
