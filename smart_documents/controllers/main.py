# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

                
class website_client(http.Controller):

    @http.route(['/documents',
#        '/documents/<int:user>'
    ], type='http', auth="public", website=True)
    def salary(self, user=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = pool.get('res.users').browse(cr, uid, uid,context)
        context['lang'] = res_user.lang 

        values = {
#            'user': res_user.browse(cr, uid, res_user.search(cr, uid, [('id','=',res_user.id)], context=context)[0], context=context),
#            'partner': pool.get('res.partner').browse(cr, uid, pool.get('res.partner').search(cr, uid, [('id','=',res_user.partner_id.id)], context=context)[0], context=context),
#            'company': pool.get('res.company').browse(cr, uid, pool.get('res.company').search(cr, uid, [('id','=',res_user.company_id.id)], context=context)[0], context=context),
#            'employee': pool.get('hr.employee').browse(cr, uid, pool.get('hr.employee').search(cr, uid, [('id','in',res_user.employee_ids)], context=context)[0], context=context),
            'context': context,
        }
        return request.website.render("smart_documents.documents_%s" %  pool.get('res.users').browse(cr, uid, uid).company_id.country_id.code.lower() , values)



class QueryURL(object):
    def __init__(self, path='', **args):
        self.path = path
        self.args = args

    def __call__(self, path=None, **kw):
        if not path:
            path = self.path
        for k,v in self.args.items():
            kw.setdefault(k,v)
        l = []
        for k,v in kw.items():
            if v:
                if isinstance(v, list) or isinstance(v, set):
                    l.append(werkzeug.url_encode([(k,i) for i in v]))
                else:
                    l.append(werkzeug.url_encode([(k,v)]))
        if l:
            path += '?' + '&'.join(l)
        return path

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
