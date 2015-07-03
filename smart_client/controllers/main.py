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

    @http.route(['/client/list','/client/list/<string:search>'], type='http', auth="user", website=True)
    def client_list(self, client=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        context['lang'] = res_user.lang

        clients = request.registry.get('res.partner').browse(cr,uid,request.registry.get('res.partner').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context).filtered(lambda r: r.is_company or not r.parent_id)
                                                                                                                                                                                            # Companies or individuals
            
        if search:
            clients = clients.filtered(lambda r: (
                    search in (r.name or '') 
                or  search in (r.comment or '') 
                or  search in (r.email or '') 
                or  search in (r.phone or '') 
                or  search in (r.street or '') 
                or  search in (r.country_id.name or '')
                ))
            _logger.info('Search %s %s' % (search,clients))

        values = {
            'client_menu': 'active',
            'context': context,
            'search': search,
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
        

        if partner and re.search("delete",request.httprequest.url) is not None:
            partner.unlink()
            return werkzeug.utils.redirect('/client/list')
                
        if post.get('redirect'):
            form_post = "/client/%s?redirect=%s" % ('new' if not partner else partner.id, post.get('redirect'))
        else:
            form_post = "/client/%s" % ('new' if not partner else partner.id)
            
        values = {
                    'context': context,
                    'client_menu': 'active',
                    'res_user': res_user,
                    'res_partner': partner or [],
                    'res_countrys': pool.get('res.country').browse(cr,uid,pool.get('res.country').search(cr,uid,[],order="code",context=context),context=context),
                    'res_partners':  clients,
                    'form_post': form_post,
                    'vat_error': '',
                    'error': '',
                    'message': '',
                }
 
        if request.httprequest.method == 'POST':
            #_logger.info('fields get %s' % partner.fields_get().keys())
            partner_data = dict((field_name.replace('hr_',''), post[field_name])
#                for field_name in ['name','is_company','country_id','commercial_partner_id','street','street2','zip','city','phone','mobile','email','active','vat','company_registry','ref','comment'] if post.get(field_name))
                #for field_name in ['name', 'firstname','lastname','is_company','country_id','commercial_partner_id','street','street2','zip','city','phone','mobile','email','active','vat','company_registry','ref','comment'] if post.get(field_name))
                for field_name in partner.fields_get().keys() if post.get(field_name))
            
            if partner_data.get('is_company', False):
                partner_data['is_company'] = (partner_data['is_company'] == 'True')
            if not partner and partner_data:
                partner_id = pool.get('res.partner').create(cr,uid,{
                    'name': _('My first client'),
                    'is_company': True,
                    'country_id': request.env.ref('base.main_company').sudo().country_id.id,
                })
                partner = pool.get('res.partner').browse(cr,uid,partner_id)
                if post.get('redirect'):
                    values['form_post'] = "/client/%s?redirect=%s" % (partner.id or 'new', post.get('redirect'))
                else:
                    values['form_post'] = "/client/%s" % (partner.id or 'new')

                
            if partner_data:
                if partner_data.get('vat'):
                    vat_country, vat_number = partner._split_vat(partner_data['vat'])
                    _logger.info('VAT %s %s' % (vat_country, vat_number))
                    if not partner.simple_vat_check(vat_country,vat_number):
                        values['vat_error'] = _("Importing VAT Number [%s%s] is not valid !" % (vat_country, vat_number))
                        values['error'] = _("Form is not complete !")
                        partner_data['vat'] = ''  # Save all other data                
                    # full check partner.vies_vat_check
                        return request.website.render("smart_client.client_client", values)
                _logger.info('is company partner data %s' % partner_data.get('is_company', 'none'))              
                partner.write(partner_data)
                if not values.get('error'):
                    values['message'] = _("Client is saved")  
                    
            contact_person = dict((field_name.replace('ccp_',''), post[field_name])
                for field_name in ['ccp_name','ccp_mobile','ccp_email',] if post.get(field_name))
            if contact_person:
                contact_person['parent_id'] = partner.id
                contact_person['street'] = partner.street
                contact_person['zip'] = partner.zip
                contact_person['city'] = partner.city
#The Mobilenumber does not save on a client contact person.
#                contact_person['mobile'] = partner.mobile
                contact_person['country_id'] = partner.country_id.id
                
                pool.get('res.partner').create(cr,uid,contact_person)


            values['res_partner']= pool.get('res.partner').browse(cr,uid,partner.id)
            

# Return to the form
            if post.get('redirect'):
                _logger.info('Redirect %s' % (post.get('redirect')))
                return werkzeug.utils.redirect(post.get('redirect'))
            else:
                return werkzeug.utils.redirect('/client/list')
        # if partner.is_company:
        #     return request.website.render("smart_client.client_organisation", values)
        # else:
        #     return request.website.render("smart_client.client_individual", values)
        return request.website.render("smart_client.client_client", values)

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
