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

class website_client(http.Controller):

    @http.route(['/client/list',], type='http', auth="user", website=True)
    def client_list(self, client=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        context['lang'] = res_user.lang

        clients = []
        for c in request.registry.get('res.partner').browse(cr,uid,request.registry.get('res.partner').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context):
#        for c in request.registry['res.partner'].browse(cr,uid,companies,request.registry['res.partner'].search(cr,uid,['|',('company_id','=',False),('company_id','=',res_user.company_id.id)],context=context),context=context):
            if c.is_company:
                clients += c
            elif not c.parent_id:
                clients += c


        values = {
            'client_menu': 'active',
            'context': context,
            'res_user': res_user,
            'res_partners': clients,
#            'res_partners': request.registry.get('res.partner').browse(cr,uid,request.registry.get('res.partner').search(cr,uid,['&','|',('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_client.list", values)


    @http.route(['/client/list/all',], type='http', auth="user", website=True)
    def client_list_all(self, client=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        context['lang'] = res_user.lang


        values = {
            'client_all_menu': 'active',
            'context': context,
            'res_user': res_user,
            'res_partners': request.registry.get('res.partner').browse(cr,uid,request.registry.get('res.partner').search(cr,uid,[]),context=context),
        }
        return request.website.render("smart_client.list_all", values)




    @http.route(['/client/<model("res.partner"):partner>','/client/<model("res.partner"):partner>/delete','/client/new'], type='http', auth="user", website=True)
    def client(self, partner=False, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        context['lang'] = res_user.lang
        
        clients = []
        for c in request.registry.get('res.partner').browse(cr,uid,request.registry.get('res.partner').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context):
#        for c in request.registry['res.partner'].browse(cr,uid,companies,request.registry['res.partner'].search(cr,uid,['|',('company_id','=',False),('company_id','=',res_user.company_id.id)],context=context),context=context):
            if c.is_company:
                clients += c
            elif not c.parent_id:
                clients += c
        

        if not partner:
            partner_id = pool.get('res.partner').create(cr,uid,{
                'name': _('My first client'),
                'is_company': ('TRUE'),
                'country_id': _('21'),
#Anders: Lägg in länk till användarens country_id istället här.
                
            })
            partner = pool.get('res.partner').browse(cr,uid,partner_id)

        else:
            if re.search("delete",request.httprequest.url) is not None:
                partner.unlink()
                return werkzeug.utils.redirect('/client/list')
                
        values = {
                    'context': context,
                    'client_menu': 'active',
                    'res_user': res_user,
                    'res_partner': partner,
                    'res_countrys': pool.get('res.country').browse(cr,uid,pool.get('res.country').search(cr,uid,[],context=context),context=context),
                    'res_partners':  clients,
                    'form_post': '/client/%s?redirect=%s' % (partner.id,post.get('redirect')),
                }

        if request.httprequest.method == 'POST':

    
            partner_data = dict((field_name.replace('hr_',''), post[field_name])
                for field_name in ['name','is_company','country_id','commercial_partner_id','street','street2','zip','city','phone','mobile','email','active','vat','company_registry','ref','comment'] if post.get(field_name))
            if partner_data:
                partner.write(partner_data)

            contact_person = dict((field_name.replace('ccp_',''), post[field_name])
                for field_name in ['ccp_name','ccp_email',] if post.get(field_name))
            if contact_person:
                contact_person['parent_id'] = partner.id
                contact_person['street'] = partner.street
                contact_person['zip'] = partner.zip
                contact_person['city'] = partner.city
                contact_person['country_id'] = partner.country_id.id
                
                pool.get('res.partner').create(cr,uid,contact_person)


            values['res_partner']= pool.get('res.partner').browse(cr,uid,partner.id)
            

## Return to the form
            if post.get('redirect'):
                return werkzeug.utils.redirect(post.get('redirect'))
            else:
                return werkzeug.utils.redirect('/client/list')
        if partner.is_company:
            return request.website.render("smart_client.client_organisation", values)
        else:
            return request.website.render("smart_client.client_individual", values)



# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
