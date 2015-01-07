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

                
class website_activity(http.Controller):


    @http.route([
    '/activity',
    '/activity/<model("res.company"):activity>',
    '/activity/<model("res.company"):activity>/member/<model("res.users"):member>/delete',
    '/activity/new',
    ], type='http', auth="user", website=True)
#    def activity(self, activity=0, search='', **post):
    def activity(self, activity=False, member=False,**post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        if not activity:
            res_user = request.registry.get('res.users').browse(cr,uid,uid)
            activity = res_user.company_id

        if re.search("delete",request.httprequest.url) is not None:
            member.company_ids = [(3,activity.id,0)]
            return werkzeug.utils.redirect('/activity')
        
        _logger.warning("This is the path %s " % request.httprequest.path)


        if request.httprequest.method == 'POST' and activity:
            _logger.warning("This is order post %s /activity/nn %s" % (post,activity.fields_get().keys()))
        
#                hrdata = dict((field_name.replace('hr_',''), post[field_name])
#                for field_name in ['phone','mobile','street','zip','city','country_id','smart_bank_account_type','smart_bank_name','smart_bank_acc_no', 'smart_bank_acc_iban','smart_bank_acc_bic'] if post.get(field_name))

            if post.get('user_id'):  # Add member
                activity.user_ids = [(4,int(post.get('user_id')),_)]
#                for user in pool.get('res.users').browse(cr,uid,post.get('user_id')):
#                    companies = []
#                    activity.user_ids = [(4,user.id,_)]
#                    _logger.warning("This is the company_ids %s " % activity.user_ids)
                    
                    #for company in user.company_ids:
                    #    companies.append(company)
                    #companies.append(activity)
                    #user.company_ids = companies
                    #user.sudo().write({'company_ids': [(4,activity.id,_)]})
#                    user.sudo().write({'company_id': activity.id,'company_ids': [(4,activity.id,_)]})
                #user.write({'company_ids': [(4,[activity.id,user.company_id.id],_)]})
#                pool.get('res.users').write(cr,uid,post.get('user_id'),{'company_ids': [(4,[activity.id,],0)]})
#                pool.get('res.users').write(cr,uid,post.get('user_id'),{'company_ids': (4,activity.id,_)})


            activitydata = dict((field_name, post[field_name])
                for field_name in iter(activity.fields_get()) if post.get(field_name))
            if activitydata:
                activity.write(activitydata)

        members = pool.get('res.users').browse(cr,uid,pool.get('res.users').search(cr,uid,[])).filtered(lambda u: activity in u.company_ids)

        values = {
            'activity_menu': 'active',
            'res_company': activity,
            'form_post': '/activity/%s' % activity.id,
            'members': members,
            'res_users': pool.get('res.users').browse(cr,uid,pool.get('res.users').search(cr,uid,[])) - members,
        }

        if not activity:
            values['error'] = _('No activity choosen or missing read rights on this activity')

        return request.website.render("smart_activity.activity", values)       
       

    #@http.route([
    #'/activity/<model("res.company"):activity>/edit',
    #'/activity/<model("res.company"):activity>/adduser'
    #], type='http', auth="user", methods=['POST'], website=True)
##    def activity(self, activity=0, search='', **post):
    #def activity(self, activity=False, **post):
        #cr, uid, context, pool = request.cr, request.uid, request.context, request.registry


        #values = {
            #'activity_menu': 'active',
            #'res_company': activity,
        #}

        #if not activity:
            #values['error'] = _('No activity choosen or missing read rights on this activity')

        #return request.website.render("smart_activity.activity", values)       
       




    @http.route(['/activity/list'], type='http', auth="public", website=True)
    def activity_list(self, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)        

        values = {
            'activity_menu': 'active',
            'res_user': res_user,
#            'res.companys': request.registry.get('res.company').browse(cr,uid,request.registry.get('res.company'),
            'res_companys': res_user.company_ids,
        }
        return request.website.render("smart_activity.list", values)       

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
