# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

from ast import literal_eval

import logging
_logger = logging.getLogger(__name__)

                
class website_account(http.Controller):

    @http.route(['/account',
        '/account/<model("res.users"):account>'
    ], type='http', auth="user", website=True)
    def account(self, account=False, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        if not account:
            account = pool.get('res.users').browse(cr,uid,uid)
        context['lang'] = account.lang
            
#        if not (account.employee_ids and account.employee_id[0]):
#            account.add_hr_employee(account.id)
#            res_user.add_activity(cr,uid,[res_user.id],context=context)
            
        values = {
            'account_menu': 'active',
            'context': context,
            'form_post': '/account/%s/post' % account.id,
#            'form_post': '/account/%s/' % account.id,
            'res_country': pool.get('res.country').browse(cr, uid, pool.get('res.country').search(cr, uid, [], order="code",context=context), context=context),
            'res_lang': pool.get('res.lang').browse(cr, uid, pool.get('res.lang').search(cr, uid, [('active','=',True)], context=context), context=context),
            'res_bank': pool.get('res.bank').browse(cr, uid, pool.get('res.bank').search(cr, uid, [], context=context), context=context),
            'res_user': account,
        }
        return request.website.render("smart_account.my_account", values)

    @http.route(['/account/<model("res.users"):account>/post'], type='http', auth="user", methods=['POST'], website=True)
    def account_post(self, account=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        _logger.warning("This is my account post %s" % (post.get('name')))

        userdata = dict((field_name, post[field_name])
            for field_name in ['name','lang'] if post.get(field_name))
        if userdata:
            account.write(userdata)
            
        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
            
        partnerdata = dict((field_name, post[field_name])
            for field_name in [
            'phone',
            'mobile',
            'email',
            'street',
            'zip',
            'city',
            'country_id',
            'smart_bank_account_type',
            'smart_bank_name',
            'smart_bank_acc_no', 
            'smart_bank_branch',
            'smart_bank_code',
            'smart_bank_acc_iban',
            'smart_bank_acc_bic',
            'smart_work_roles',
            'dropbox_link',
#            'smart_place_of_birth',
            'category_id',           
            ] if post.get(field_name))
            
        if partnerdata:
            account.partner_id.write(partnerdata)

        #legaldata = dict((field_name.replace('legal_',''), post[field_name])
            #for field_name in ['legal_street','legal_zip','legal_city'] if post.get(field_name))

        hrdata = dict((field_name.replace('hr_',''), post[field_name])
#            for field_name in ['passport_id','legal_city','street','phone','mobile'] if post.get(field_name))
            for field_name in [
            'birthday',
            'country_id',
            'education',            
            'identification_id',
            'job_id',
            'gender',
            'hr_country_id'
            'marital',
            'passport_id',
            'otherid',
            'withhold_tax',
            ] if post.get(field_name))
        if hrdata:
            _logger.warning("This is my hrdata post %s" % (hrdata))
            _logger.warning("This is my contracts %s" % (account.employee_ids))
            account.employee_ids[0].write(hrdata)
        else:
            _logger.warning("This is a emptyhrdata %s" % (hrdata))
        
        
        #bankdata = dict((field_name, post[field_name])
            #for field_name in ['bank','acc_number','iban','bank_bic',] if post.get(field_name))
        #if bankdata and account.company_id.bank_ids:
            #account.company_id.bank_ids[0].write(bankdata)
        #elif bankdata:
            #bankdata['state']='bank'
            #if not bankdata.get('acc_number'):
                #bankdata['acc_number'] = ' '
            #bankdata['company_id'] = account.company_id.id
            #bank_id = pool.get('res.partner.bank').create(cr,uid,bankdata)
            #account.write({'bank_ids': [(6,0,[bank_id])]}) 
            
#            account.company_id.bank_ids[0].write(bankdata)
        
        #request.registry['res.users'].write(cr,uid,user,userdata)
        values = {
            'message': "Saved!",
#            'error': "Test error",
            'account_menu': 'active',
            'res_user': account,
            'form_post': '/account/%s/post' % account.id,
            'res_lang': pool.get('res.lang').browse(cr, uid, pool.get('res.lang').search(cr, uid, [('active','=',True)], context=context), context=context),
            'res_country': pool.get('res.country').browse(cr, uid, pool.get('res.country').search(cr, uid, [], order="code",context=context), context=context),
            'res_bank': pool.get('res.bank').browse(cr, uid, pool.get('res.bank').search(cr, uid, [], context=context), context=context),
            'context': context,

        }
        return request.website.render("smart_account.my_account", values)        
     

    @http.route(['/account/list',], type='http', auth="public", website=True)
    def account_list(self, order=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        values = {
            'context': context,        
            'account_all_menu': 'active',
            'res_users':  request.registry['res.users'].browse(cr, uid, request.registry['res.users'].search(cr, uid,[], context=context),context=context),
        }
        return request.website.render("smart_account.list", values)
# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
