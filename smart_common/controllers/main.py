# -*- coding: utf-8 -*-

import werkzeug


import openerp
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.web.controllers.main import ensure_db
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
import openerp.modules.registry

from openerp import SUPERUSER_ID
from openerp.addons.website.models.website import slug




import logging
_logger = logging.getLogger(__name__)


class smart_common(http.Controller):

    @http.route(['/dashboard'], type='http', auth="user", website=True)
    def dashboard(self, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        _logger.warning("Dashboard %s" % request.uid)

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
        return request.website.render("smart_common.dashboard", values)       

    
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
        return request.website.render("smart_common.dashboard", values)       




    @http.route('/smart/login', type='http', auth="none")
    def smart_login(self, redirect=None, **kw):
        #return "Method %s Session UID %s uid %s" % (request.httprequest.method,request.session.uid,request.uid)

        ensure_db()
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)
            
        if request.httprequest.method == 'GET' and request.session.uid:
#        if request.httprequest.method == 'GET':
            return http.redirect_with_hash('/dashboard')

        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        if not redirect:
            redirect = '/dashboard?' + request.httprequest.query_string
        values['redirect'] = redirect

        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if uid is not False:
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
        return request.render('smart_common.login', values)




    @http.route('/smart/signup', type='http', auth='none', website=True)
    def smart_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                return super(AuthSignupHome, self).smart_login(*args, **kw)
            except (SignupError, AssertionError), e:
                qcontext['error'] = _(e.message)

        return request.render('smart_common.signup', qcontext)





    @http.route('/add_activity', type='http', auth='user', website=True)
    def smart_add_activity(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        _logger.warning("smart_login add_activity %s " % (self))
        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        res_user.sudo().add_activity()
        res_user.sudo().add_hr_employee()
        res_user.sudo().webterms_accepted = True
        return werkzeug.utils.redirect('/dashboard')





    @http.route('/legal/webpolicy', type='http', auth='user', website=True)
    def webpolicy(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        values = {
            'context': context,
#            'res_user': res_user,
        }
        
        return request.website.render("smart_common.legal_%s" %  pool.get('res.users').browse(cr, uid, uid).company_id.country_id.code.lower() , values)

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
