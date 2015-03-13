# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from datetime import datetime, timedelta
import random
from urlparse import urljoin
import werkzeug

from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, ustr
from ast import literal_eval
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import logging


_logger = logging.getLogger(__name__)

class res_users(osv.Model):
    _inherit = 'res.users'

    def _get_state(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for user in self.browse(cr, uid, ids, context):
            if user.approved:
                res[user.id] = 'approved'
            elif user.login_date:
                res[user.id] = 'active'
            else:
                res[user.id] = 'new'
        return res

    _columns = {
        'state': fields.function(_get_state, string='Status',  type='selection', 
                    selection=[('new', 'Never Connected'), ('active', 'WebUser'),('approved', 'SmartUser')],), 
        'approved': fields.boolean('Approved',),
        'webterms_accepted': fields.boolean('Web Terms Accepted',),
        
    }
    
    def Xon_change_approved(self, cr, uid, ids, approved, context=None):
        for user in self.pool.get('res.users').browse(cr, uid, ids, context=context):
            #company_id = self.add_activity(cr,uid,user)
            employee_id = self.add_hr_employee(cr,uid,user)
            foo = True
        return {'value': {}}
#            val = self._change_company(cr,uid,user.id,approved,context)
#        return {'value': {'company_ids': [company_id],'company_id': company_id, } }
        return {}
        
    def _change_company(self,cr,uid,user_id,approved,context):
        user = self.pool.get('res.users').browse(cr, uid, user_id)
        template_user = self.pool.get('res.users').browse(cr, uid, literal_eval(self.pool.get('ir.config_parameter').get_param(cr, uid, 'auth_signup.template_user_id', 'False')),)
        assert template_user and self.exists(cr, uid, template_user.id,), 'Signup: invalid template user'

        company_id = self.pool.get('res.company').search(cr,uid,[('name','=',user.name)],limit=1)
        if not company_id:
            company_id = self.pool.get('res.company').create(cr,uid,{'name': user.name, 'parent_id': template_user.company_id.id})
        else:
            company_id = company_id[0]

        val={'company_ids': [template_user.company_id.id],'company_id': template_user.company_id.id, }

        return val
        
        
    def add_hr_employee(self):
        template_user = self.env['res.users'].browse(literal_eval(self.env['ir.config_parameter'].get_param('auth_signup.template_user_id', 'False')),)
        assert template_user and template_user.exists(), 'Signup: invalid template user'
        _logger.warning("smart_login add_hr_employee  %s " % (self))
        for user in self:
            _logger.warning("smart_login nmbr employee %s " % (user.employee_ids))
            _logger.warning("smart_login nmbr template employee %s " % (template_user.employee_ids))
            
            if len(user.employee_ids) == 0:
                if template_user.employee_ids and template_user.employee_ids[0]:
                    employee = self.env['hr.employee'].create({
                        'name':         user.name,
                        'company_id':   user.company_id.id,
                        'partner_id':   user.company_id.partner_id.id,
                        'country_id':   template_user.employee_ids[0].country_id.id,
                        'withhold_tax': template_user.employee_ids[0].withhold_tax,
                        'user_id':      user.id,
                    })
                    
#                    address_home = self.env['res.partner'].copy(template_user.employee_ids[0].address_home_id.id)
##                    address_home = employee.address_home_id.copy()
#                    address_home.write({'street': 'my street','name': _('%s home') % user.name})
                    employee.write({'address_home_id' : user.partner_id.id})                    
                else:
                    _logger.warning("smart_login template-employee missing %s " % (template_user.name))
                    return False
            else:
                employee = user.employee_ids[0]
            return employee.id


    def add_activity(self):
        template_user = self.env['res.users'].browse(literal_eval(self.env['ir.config_parameter'].get_param('auth_signup.template_user_id', 'False')),)
        assert template_user and template_user.exists(), 'Signup: invalid template user'
        for user in self:
            if user.company_id.id == template_user.company_id.id:
                company = self.env['res.company'].browse(self.env['res.company'].search([('name','=', _('%s Activity') % user.name)]))
                if not company:
                    company = self.env['res.company'].create({
                        'name': _('%s Activity') % user.name,
                        'currency_id':             template_user.company_id.currency_id.id,
                        'country_id':              template_user.company_id.country_id.id,
                        'smart_share':             template_user.company_id.smart_share,
                        'parent_id':               template_user.company_id.parent_id.id,})
                _logger.warning("res.user company %s" % (company))
                if company and company.id <> user.company_id.id:    
                    user.company_ids = [(6,0,[int(template_user.company_id.id),int(company.id)])]
                    user.company_id = int(company.id)
                    admin_user = self.env['res.users'].browse(1)
                    admin_user.sudo.company_ids = [(4,company.id,0)]
                    


    def add_message(self):
        _logger.warning("server_action message %s " % ('Hello world'))
#        for user in self.pool.get('res.users').browse(cr, uid,ids):
#            _logger.warning("smart_login message %s " % (user.name))
 
                
 
 
 
    def xxadd_activity(self):
#        user = self.pool.get('res.users').browse(cr, uid, user_id)
        template_user = self.env['res.users'].browse(literal_eval(self.env['ir.config_parameter'].get_param('auth_signup.template_user_id', 'False')),)
        assert template_user and template_user.exists(), 'Signup: invalid template user'
        #_logger.warning("res.user ids %s context %s" % (self,self.context))
        for user in self:
            if user.company_id.id == template_user.company_id.id:
                company_id = self.env['res.company'].copy(template_user.company_id.id,default={
                    'name': _('%s Activity') % user.name,
                    'currency_id': template_user.company_id.currency_id.id,
                    'country_id': template_user.company_id.country_id.id,
                    'parent_id': template_user.company_id.parent_id.id,})  

#                company = self.env['res.company'].browse(self.env['res.company'].create({
#                    'name': _('%s Activity') % user.name,
#                    'currency_id': template_user.company_id.currency_id.id,
#                    'country_id': template_user.company_id.country_id.id,
#                    'parent_id': template_user.company_id.parent_id.id,}))  
#               company = template_user.company_id.copy_data(default={'name': _('%s Activity') % user.name,})
                _logger.warning("res.user company %s" % (company_id))
#                company.write({'name': _('%s activity') % user.name,'parent_id': template_user.company_id.parent_id.id})
#                company = self.pool.get('res.company').browse(cr,uid,self.pool.get('res.company').create(cr,uid,{'name': _('%s activity') % user.name,'parent_id': template_user.company_id.parent_id.id,}))
#                self.env['res.users'].write(user.id,{'company_id': company.id})
                #user.company_ids = [(6,_,[company.id,template_user.parent_id.id])]
                #user.company_id.id = company.id

           #     user.write({'company_id': company_id})
                user.write({'company_ids': (6,_,[company_id,template_user.parent_id.id]),'company_id': company_id})
        
    def xadd_activity(self,cr,uid,ids,context=None):
#        user = self.pool.get('res.users').browse(cr, uid, user_id)
        template_user = self.pool.get('res.users').browse(cr, uid, literal_eval(self.pool.get('ir.config_parameter').get_param(cr, uid, 'auth_signup.template_user_id', 'False')),)
        assert template_user and self.exists(cr, uid, template_user.id,), 'Signup: invalid template user'
        _logger.warning("res.user ids %s context %s" % (ids,context))
        for user in self.pool.get('res.users').browse(cr, uid,ids):
            if user.company_id.id == template_user.company_id.id:
                company_dict = template_user.company_id.copy_data(default={'name': _('%s activity') % user.name,})
                _logger.warning("res.user company %s" % (company_dict))

#                company.write({'name': _('%s activity') % user.name,'parent_id': template_user.company_id.parent_id.id})
#                company = self.pool.get('res.company').browse(cr,uid,self.pool.get('res.company').create(cr,uid,{'name': _('%s activity') % user.name,'parent_id': template_user.company_id.parent_id.id,}))
                user.write({'company_ids': [(6,0,[company.id,template_user.parent_id.id])],'company_id': company.id})
        
        
    def check_activity(self,cr,uid,ids,context=None):
        template_user = self.pool.get('res.users').browse(cr, uid, literal_eval(self.pool.get('ir.config_parameter').get_param(cr, uid, 'auth_signup.template_user_id', 'False')),)

        assert template_user and self.exists(cr, uid, template_user.id,), 'Signup: invalid template user'

        res = {}
        for user in self.pool.get('res.users').browse(cr, uid,ids):
            company_id = self.pool.get('res.company').search(cr,uid,[('name','=',user.name)],limit=1)
            if not company_id:
                if template_user.company_id:
                 #   company = template_user.company_id.copy()
#                    company.write({'name': user.name,'parent_id': template_user.company_id.parent_id.id})
                    company = self.pool.get('res.company').browse(cr,uid,self.pool.get('res.company').create(cr,uid,{'name': _('%s activity') % user.name,'parent_id': template_user.company_id.parent_id.id,}))

                else:
                    company = self.pool.get('res.company').browse(cr,uid,self.pool.get('res.company').create(cr,uid,{'name': user.name,}))
            else:
                company = user.company_id
            parent_id = 1
            if company.parent_id:
                parent_id = company.parent_id.id
            
            user.write({'company_ids': [(6,0,[company.id,parent_id])],'company_id': company.id})


        if self.company_id.id == template_user.company_id.id:
            return False
        else:
            return True
            

        ##company_ids = [cpy.id for cpy in user.company_ids]
        ##company_ids.append(company_id)
        ##self.pool.get('res.users').write(cr,SUPERUSER_ID,user.id,{'company_ids': company_ids})
        #_logger.debug("company_ids %d %r", approved,user.groups_id)
        #groups = [grp.id for grp in user.groups_id]
 
        #grp_project = self.pool.get('res.groups').search(cr,uid,[('name', '=','Manager'),('category_id','in',self.pool.get('ir.module.category').search(cr,uid,[('name','=','Project')]))])[0]
        #grp_account = self.pool.get('res.groups').search(cr,uid,[('name', '=','Invoicing & Payments'),('category_id','in',self.pool.get('ir.module.category').search(cr,uid,[('name','=','Accounting & Finance')]))])[0]
        #grp_hr = self.pool.get('res.groups').search(cr,uid,[('name', '=','Employee'),('category_id','in',self.pool.get('ir.module.category').search(cr,uid,[('name','=','Human Resources')]))])[0]

        ##grp_project = self.pool.get('res.groups').search(cr,uid,[('name', 'in',['Manager','Invoicing & Payments','Employee']),('category_id','in',self.pool.get('ir.module.category').search(cr,uid,[('name','in',['Project','Accounting & Finance','Human Resources'])])):

        #val = {}
      
        #if not approved:
            #groups = [grp for grp in groups if not grp in [grp_project,grp_account,grp_hr]]
            #val={'company_ids': [template_user.company_id.id],'company_id': template_user.company_id.id, 'sel_groups_60_61': None, 'sel_groups_5_65_66': None, 'sel_groups_46_47_48': None,}
            ##self.pool.get('res.users').write(cr,SUPERUSER_ID,user.id,{'company_ids': company_ids})
            ##self.pool.get('res.users').write(cr,SUPERUSER_ID,user.id,{'company_id': template_user.company_id.id})
            ##self.pool.get('res.users').write(cr,SUPERUSER_ID,user.id,{'company_ids': [template_user.company_id.id]})
            
        ##else:
            ##self.pool.get('res.users').write(cr,SUPERUSER_ID,user.id,{'company_id': company_id})
            ##self.pool.get('res.users').write(cr,SUPERUSER_ID,user.id,{'company_ids': [company_id]})
            
##            for grp in  [grp_project,grp_account,grp_hr]:
##                if grp not in groups:
##                    groups.append(grp)
##            val = {'company_ids': [company_id],'company_id': company_id, 'sel_groups_60_61': 61, 'sel_groups_5_65_66': 5, 'sel_groups_46_47_48': 46, }

        ##_logger.debug("Groups %r", groups)
##        if company_id:
##            self.pool.get('res.company').unlink(cr,uid,company_id)
        #return val
