# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

import re

import logging
_logger = logging.getLogger(__name__)

class smart_common(http.Controller):
    @http.route('/', type='http', auth="none")
    def index_none(self, s_action=None, db=None, **kw):
        return "None"
        return werkzeug.utils.redirect('/order/none')

    @http.route('/', type='http', auth="user")
    def index_user(self, s_action=None, db=None, **kw):
        return "user"
        return http.local_redirect('/order/list', query=request.params, keep_hash=True)

    @http.route('/', type='http', auth="public")
    def index_pubic(self, s_action=None, db=None, **kw):
        return "public"


    @http.route(['/kalle',], type='http', auth="user", website=True)
    def common_kalle(self, client=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        return "Kalle"
        
        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        context['lang'] = res_user.lang


        values = {
            'client_menu': 'active',
            'context': context,
            'res_user': res_user,
            'res_partners': request.registry.get('res.partner').browse(cr,uid,request.registry.get('res.partner').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_client.list", values)
        
        
        
    def write_form(odoo_model,fieldname_prefix='',**post):
        formdata = dict((field_name.replace(fieldname_prefix,''), post[field_name])
            for field_name in iter(odoo_model.fields_get()) if post.get(field_name))
        if formdata:
            odoo_model.write(formdata)
        return True
#
