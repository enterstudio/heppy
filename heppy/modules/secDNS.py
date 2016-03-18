from collections import OrderedDict

from ..Module import Module

class secDNS(Module):
    opmap = {
        'infData':      'descend',
        'maxSigLife':   'set',
    }

### RESPONSE parsing

    def parse_dsData(self, response, tag):
        response.set('keyTag',      response.find_text(tag, 'secDNS:keyTag'))
        response.set('digestAlg',   response.find_text(tag, 'secDNS:alg'))
        response.set('digestType',  response.find_text(tag, 'secDNS:digestType'))
        response.set('digest',      response.find_text(tag, 'secDNS:digest'))

    def parse_keyData(self, response, tag):
        response.set('flags',       response.find_text(tag, 'secDNS:flags'))
        response.set('protocol',    response.find_text(tag, 'secDNS:protocol'))
        response.set('keyAlg',      response.find_text(tag, 'secDNS:alg'))
        response.set('pubKey',      response.find_text(tag, 'secDNS:pubKey'))

### REQUEST rendering

    def render_create(self, request):
        ext = self.render_extension(request, 'create')
        self.render_allData(request, ext, request)

    def render_update(self, request):
        ext = self.render_extension(request, 'update')
        for k in ('add', 'rem', 'chg'):
            if request.get(k):
                command = request.sub(ext, 'secDNS:' + k)
                self.render_allData(request, command, request.get(k))

    def render_allData(self, request, parent, values):
        if values.get('all')=='true':
            request.sub(parent, 'secDNS:all', {}, 'true')
            return
        if values.get('maxSigLife'):
            request.sub(parent, 'secDNS:maxSigLife', {}, values.get('maxSigLife'))
        if values.get('digest'):
            self.render_dsData(request, parent, values)
        else:
            self.render_keyData(request, parent, values)

    def render_dsData(self, request, parent, values):
        data = request.sub(parent, 'secDNS:dsData')
        request.sub(data, 'secDNS:keyTag',      {}, values.get('keyTag'))
        request.sub(data, 'secDNS:alg',         {}, values.get('digestAlg'))
        request.sub(data, 'secDNS:digestType',  {}, values.get('digestType'))
        request.sub(data, 'secDNS:digest',      {}, values.get('digest'))
        self.render_keyData(request, data, values)

    def render_keyData(self, request, parent, values):
        if not values.get('pubKey'):
            return
        data = request.sub(parent, 'secDNS:keyData')
        request.sub(data, 'secDNS:flags',       {}, values.get('flags'))
        request.sub(data, 'secDNS:protocol',    {}, values.get('protocol'))
        request.sub(data, 'secDNS:alg',         {}, values.get('keyAlg'))
        request.sub(data, 'secDNS:pubKey',      {}, values.get('pubKey'))

