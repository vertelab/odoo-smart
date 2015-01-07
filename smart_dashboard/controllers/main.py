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

                
class website_dashboard(http.Controller):

    @http.route(['/dashboard'], type='http', auth="user", website=True)
    def dashboard(self, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang

        order_ids = request.registry.get('sale.order').search(cr,uid,[('company_id','=',res_user.company_id.id)],context=context)
        
        clients = []
        for c in request.registry.get('res.partner').browse(cr,uid,request.registry.get('res.partner').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context):
#        for c in request.registry['res.partner'].browse(cr,uid,companies,request.registry['res.partner'].search(cr,uid,['|',('company_id','=',False),('company_id','=',res_user.company_id.id)],context=context),context=context):
            if c.is_company:
                clients += c
            elif not c.parent_id:
                clients += c
               
        #if res_user.webterms_accepted:
        #    expenses = pool.get('hr.expense.expense').browse(cr,uid,pool.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        #else:
        expenses = False
            
        _logger.warning("Expenses %s" % expenses)
        #message_ids = (m.id for m in pool.get('mail.notification').browse(cr,uid,pool.get('mail.notification').search(cr,uid,[(res_user.partner_id.id,'in','partner_ids')])))
        #message_ids = (m.id for m in pool.get('mail.message').browse(cr,uid,pool.get('mail.message').search(cr,uid,[(res_user.partner_id.id,'in','partner_ids')])))
        # packa upp partner_ids

        values = {
            'dashboard_menu': 'active',
            'context': context,
#            'mail_message': pool.get('mail.message').browse(cr,uid,message_ids,context=context),
            'mail_message': pool.get('mail.message').browse(cr,uid,pool.get('mail.message').search(cr,uid,[]),context),
#            'mail_thread': pool.get('mail.thread').browse(cr,uid,pool.get('mail.thread').search(cr,uid,[]),context),
            'mail_mail': pool.get('mail.mail').browse(cr,uid,pool.get('mail.mail').search(cr,uid,[]),context),
            'res_user': res_user,
            'res_users': pool.get('res.users').browse(cr, uid, uid,context), # users of company_ids
            'sale_orders': request.registry.get('sale.order').browse(cr,uid,order_ids,context=context), 
            'res_partners': clients,
            'expenses': expenses,
#            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_dashboard.dashboard", values)       

    
    @http.route(['/message'], type='http', auth="user", website=True)
    def dashboard_message(self, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
       

        values = {
            'dashboard_menu': 'active',
            'context': context,
            'mail_message': pool.get('mail.message').browse(cr,uid,pool.get('mail.message').search(cr,uid,[]),context),
#            'mail_thread': pool.get('mail.thread').browse(cr,uid,pool.get('mail.thread').search(cr,uid,[]),context),
            'mail_mail': pool.get('mail.mail').browse(cr,uid,pool.get('mail.mail').search(cr,uid,[]),context),
            'res_user': pool.get('res.users').browse(cr, uid, uid,context),

        }
        return request.website.render("smart_dashboard.dashboard", values)       



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
