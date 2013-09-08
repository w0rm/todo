from template import render


class Index:

    def GET(self):
        return render.index()
