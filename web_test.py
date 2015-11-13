import sys
import json
sys.path.append('./lib')

import cherrypy
import sample


class GraphAccces(object):
    def __init__(self):
        self.graph = sample.graph

    def _cp_dispatch(self, vpath):
        if 'search' not in cherrypy.request.params:
            print('setting search')
            cherrypy.request.params['search'] = self.graph.Search()
            self.funcs = {i: getattr(cherrypy.request.params['search'], i) for i in dir(self.graph.Search) if not i.startswith('_') and i is not 'execute'}
        vpath = vpath[0].split(',')
        print(vpath)
        if vpath[0] in self.funcs:
            try:
                cherrypy.request.params['search'] = self.funcs[vpath[0]](*vpath[1:])
            except TypeError as e:
                print(e)
                cherrypy.request.params['error'] = '{}'.format(e)
        else:
            cherrypy.request.params['error'] = '{} is not a search function'.format(vpath[0])

        return self

    @cherrypy.expose
    def index(self, *args, **kwargs):
        if 'search' in cherrypy.request.params:
            result = cherrypy.request.params['search'].execute()
            print('result', result)
            reply = {'result': list(result.keys())}
            if 'data' in cherrypy.request.params:
                reply['data'] = result
            return '{}'.format(json.dumps(reply))
        if 'error' in cherrypy.request.params:
            return '{}'.format(cherrypy.request.params['error'])
        funcs = [i for i in dir(self.graph.Search) if not i.startswith('_') and i is not 'execute']
        reply = {'commands': funcs}
        return '{}'.format(json.dumps(reply, sort_keys=True, indent=4))

if __name__ == '__main__':
    cherrypy.quickstart(GraphAccces())