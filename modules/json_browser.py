# coding: utf-8
import web
import json
import urllib
import urllib2


class JSONAppBrowser(web.browser.AppBrowser):
    '''Subclassed AppBrowser to consume json api'''

    headers = {'Accept': 'application/json'}

    def json_open(self, url, data=None, headers={}, method='GET'):
        headers = headers or self.headers
        url = urllib.basejoin(self.url, url)
        req = urllib2.Request(url, json.dumps(data), headers)
        req.get_method = lambda: method  # Trick to set request method
        return self.do_request(req)

    @property
    def json_data(self):
        return json.loads(self.data)
