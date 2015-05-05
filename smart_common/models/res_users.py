# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import openerp.addons.decimal_precision as dp

from datetime import datetime, timedelta
import random
from urlparse import urljoin
import werkzeug

from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, ustr
import logging


_logger = logging.getLogger(__name__)

class res_users(models.Model):
    _inherit = 'res.users'

    state    = fields.Selection(compute="_get_state", string='Status',  selection=[('new', 'Never Connected'), ('active', 'WebUser'),('approved', 'SmartUser')],)
    approved = fields.Boolean('Approved',)
    webterms_accepted = fields.Boolean('Web Terms Accepted',)
    current_activity = fields.Many2one('res.company')
#    current_activity_members = fields.Many2many('res.users')
    activity_ids = fields.Many2many(comodel_name='res.company',relation='activity_users_rel',string='Activities')
    

    @api.one
    def _get_state(self):
        if self.approved:
            self.state = 'approved'
        elif self.login_date:
            self.state = 'active'
        else:
            self.state = 'new'

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
        
    @api.multi
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
#                    address_home = employee.address_home_id.copy()
#                    address_home.write({'street': 'my street','name': _('%s home') % user.name})
                    employee.write({'address_home_id' : user.partner_id.id})                    
                else:
                    _logger.warning("smart_login template-employee missing %s " % (template_user.name))
                    return False
            else:
                employee = user.employee_ids[0]
            return employee.id

    @api.one
    def add_activity(self):
        template_user = self.env['res.partner'].browse(self.env['ir.config_parameter'].get_param('auth_signup.template_user_id', 0),)
        assert template_user and template_user.exists(), 'Signup: invalid template user'
        
        company = template_user.company_id.copy()
        company.name = _('%s Activity') % self.name
        self.company_ids = [(6,0,[int(template_user.company_id.id),int(company.id)])]
        self.company_id = company
        self.current_activity = company



        #admin_user = self.env['res.users'].browse(1)
        #admin_user.sudo().company_ids = [(4,company.id,0)]
        

        #~ 
        #~ if user.company_id and template_user.company_id:
            #~ if user.company_id.id == template_user.company_id.id:
                #~ company = self.env['res.company'].browse(self.env['res.company'].search([('name','=', _('%s Activity') % user.name)]))
                #~ if not company:
                    #~ company = self.env['res.company'].create({
                        #~ 'name': _('%s Activity') % user.name,
                        #~ 'currency_id':             template_user.company_id.currency_id.id,
                        #~ 'country_id':              template_user.company_id.country_id.id,
                        #~ 'smart_share':             template_user.company_id.smart_share,
                        #~ 'parent_id':               template_user.company_id.parent_id.id,})
                #~ _logger.warning("res.user company %s" % (company))
                #~ if company and company.id <> user.company_id.id:    
                    #~ user.company_ids = [(6,0,[int(template_user.company_id.id),int(company.id)])]
                    #~ user.company_id = int(company.id)
                    #~ admin_user = self.env['res.users'].browse(1)
                    #~ admin_user.sudo().company_ids = [(4,company.id,0)]
        #~ else:
            #~ _logger.warning("User missing company %s or %s" % (user.id,template_user.id))    
#~ 

    def add_message(self):
        _logger.warning("server_action message %s " % ('Hello world'))
#        for user in self.pool.get('res.users').browse(cr, uid,ids):
#            _logger.warning("smart_login message %s " % (user.name))
 
                
 

    #~ def check_activity(self,cr,uid,ids,context=None):
        #~ template_user = self.pool.get('res.users').browse(cr, uid, literal_eval(self.pool.get('ir.config_parameter').get_param(cr, uid, 'auth_signup.template_user_id', 'False')),)
#~ 
        #~ assert template_user and self.exists(cr, uid, template_user.id,), 'Signup: invalid template user'
#~ 
        #~ res = {}
        #~ for user in self.pool.get('res.users').browse(cr, uid,ids):
            #~ company_id = self.pool.get('res.company').search(cr,uid,[('name','=',user.name)],limit=1)
            #~ if not company_id:
                #~ if template_user.company_id:
                 #~ #   company = template_user.company_id.copy()
#~ #                    company.write({'name': user.name,'parent_id': template_user.company_id.parent_id.id})
                    #~ company = self.pool.get('res.company').browse(cr,uid,self.pool.get('res.company').create(cr,uid,{'name': _('%s activity') % user.name,'parent_id': template_user.company_id.parent_id.id,}))
#~ 
                #~ else:
                    #~ company = self.pool.get('res.company').browse(cr,uid,self.pool.get('res.company').create(cr,uid,{'name': user.name,}))
            #~ else:
                #~ company = user.company_id
            #~ parent_id = 1
            #~ if company.parent_id:
                #~ parent_id = company.parent_id.id
            #~ 
            #~ user.write({'company_ids': [(6,0,[company.id,parent_id])],'company_id': company.id})
#~ 
#~ 
        #~ if self.company_id.id == template_user.company_id.id:
            #~ return False
        #~ else:
            #~ return True
            
