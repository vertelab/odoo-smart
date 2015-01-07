# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2014 Vertel AB (<http://vertel.se>).
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

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class res_company(osv.osv):
    _inherit = "res.company"
    
    def _smart_cash(self, cr, uid, ids, name, args, context=None):
        res = {}
        for company in self.browse(cr, uid, ids, context=context):  
            res[company.id] = {
                'smart_cash': 0.0,
                'smart_budget': 0.0,
                'sale_order_sum_cash': 0.0, 
                'sale_order_sum_budget': 0.0,
                'expense_sum_cash': 0.0, 
                'expense_sum_budget': 0.0,
                'smart_amount': 0.0,
                'activity_amount_cash': 0.0,
                'activity_amount_budget': 0.0,
#                'smart_cash_date': invoice.date_due or date.today().isoformat(),
#                'smart_cash_date': date(*time.strptime(invoice.date_invoice,'%Y-%m-%d')[:3]) + timedelta(days=invoice.company_id.parent_id.prepayment_days)
            }
#            res[company.id]['smart_cash'] = 0.0
#            for move in self.pool.get('account.move').browse(cr, uid, self.pool.get('account.move').search(cr,uid,[('company_id','=',company.id)],context=context), context=context):
#            for move in self.pool.get('account.move').browse(cr, uid, self.pool.get('account.move').search(cr,uid,[],context=context), context=context):
#                res[company.id]['smart_cash'] =+ move.smart_cash
#                res[company.id]['smart_budget'] =+ move.smart_budget


#SMart Cash                
            for order in self.pool.get('sale.order').browse(cr, uid, self.pool.get('sale.order').search(cr,uid,['&',('company_id','=',company.id),('state','in',('progress','manual','done'))],context=context), context=context):
#            for order in company.order_cash():
#                res[company.id]['smart_cash'] = res[company.id]['smart_cash'] + order.amount_total 
                res[company.id]['smart_cash'] = res[company.id]['smart_cash'] + order.amount_untaxed 
                res[company.id]['sale_order_sum_cash'] += order.amount_untaxed 

            res[company.id]['activity_amount_cash'] =  res[company.id]['sale_order_sum_cash'] * (1 - (company.smart_share / 100))
            res[company.id]['smart_amount_cash']    =  res[company.id]['sale_order_sum_cash'] * (company.smart_share / 100)

#SMart Budget        
            for order in self.pool.get('sale.order').browse(cr, uid, self.pool.get('sale.order').search(cr,uid,['&',('company_id','=',company.id),('state','in',('sent','waiting_date'))],context=context), context=context):
#            for order in company.order_budget():
#                res[company.id]['smart_budget'] = res[company.id]['smart_budget'] + order.amount_total
                res[company.id]['smart_budget'] = res[company.id]['smart_budget'] + order.amount_untaxed
                res[company.id]['sale_order_sum_budget'] += order.amount_untaxed 

            res[company.id]['smart_amount_budget']  =  res[company.id]['sale_order_sum_budget'] * (company.smart_share / 100)
            res[company.id]['activity_amount_budget'] =  res[company.id]['sale_order_sum_budget'] * (1 - (company.smart_share / 100))


           #('draft', 'Draft Quotation'),
            #('sent', 'Quotation Sent'),
            #('cancel', 'Cancelled'),
            #('waiting_date', 'Waiting Schedule'),
            #('progress', 'Sales Order'),
            #('manual', 'Sale to Invoice'),
            #('shipping_except', 'Shipping Exception'),
            #('invoice_except', 'Invoice Exception'),
            #('done', 'Done'),

#SMart Cash
            for expense in self.pool.get('hr.expense.expense').browse(cr, uid, self.pool.get('hr.expense.expense').search(cr,uid,['&',('company_id','=',company.id),('state','in',('accepted','done','paid'))],context=context), context=context):
                _logger.warning("This is my expense.amount_untaxed next line")
                try:                    
                    _logger.warning("This is my expense.amount_untaxed %s (cash)" % (expense.amount_untaxed))
                    res[company.id]['smart_cash']        -= float(expense.amount_untaxed or 0.0)
                    res[company.id]['expense_sum_cash']  -= float(expense.amount_untaxed or 0.0)
                except Exception, e:
                    _logger.warning("There are no expense.amount_untaxed %s (cash)  %s" % (expense.id,e))
                    res[company.id]['smart_cash']        -= 666
                    res[company.id]['expense_sum_cash']  -= 666
                    
#SMart Budget                            
            for expense in self.pool.get('hr.expense.expense').browse(cr, uid, self.pool.get('hr.expense.expense').search(cr,uid,['&',('company_id','=',company.id),('state','in',('confirm',))],context=context), context=context):
                try:                    
                    _logger.warning("This is my expense.amount_untaxed %s (budget)" % (expense.amount_untaxed))
                    res[company.id]['smart_budget']       -= float(expense.amount_untaxed or 0.0)
                    res[company.id]['expense_sum_budget'] -= float(expense.amount_untaxed or 0.0)
                except Exception, e:
                    _logger.warning("There are no expense.amount_untaxed %s (budget)  %s" % (expense.id,e))
                    res[company.id]['smart_budget']       -= 666
                    res[company.id]['expense_sum_budget'] -= 666



#            ('draft', 'New'),
#            ('cancelled', 'Refused'),
#            ('confirm', 'Waiting Approval'),
#            ('accepted', 'Approved'),
#            ('done', 'Waiting Payment'),
#            ('paid', 'Paid'),
            
#Totals
            res[company.id]['smart_cash'] = round(res[company.id]['smart_cash'] - res[company.id]['smart_amount_cash'],0)
            res[company.id]['smart_budget'] = round(res[company.id]['smart_budget']  - res[company.id]['smart_amount_budget'],0)

            
                 
            #res[company.id]['smart_cash'] = 0.0
        return res

    _columns = {
       'smart_budget': fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Budget',multi='all',help="Approved invoiced amount.",),
#       'smart_cash': fields.function(smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Budget',
#            help="Approved invoiced amount.",
#            multi='all',),
       'smart_cash': fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Cash',
            help="Free invoiced amount for salary or expenses.",
            multi='all',),
        'prepayment': fields.boolean('Prepayment',help="SMart User: this virtual company can have prepayment smart_cash, SMart Company: this country applies prepayment"),
        'prepayment_days': fields.integer('Prepayment Days',help="Leadtime in days before invoiced amount becomes smart_cash (global)"),
        'smart_share': fields.float('SMarts Share',digits_compute=dp.get_precision('Account')),
        'sale_order_sum_cash': fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Order sum cash',multi='all',help="Approved invoiced amount.",),
        'sale_order_sum_budget':fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Order sum budget',multi='all',help="Approved invoiced amount.",),
        'smart_amount_cash':fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Amount cash',multi='all',help="Approved invoiced amount.",),
        'smart_amount_budget':fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Amount budget',multi='all',help="Approved invoiced amount.",),
        'activity_amount_cash':fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart activity amount cash',multi='all',help="Approved invoiced amount.",),
        'activity_amount_budget':fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart activity amount budget',multi='all',help="Approved invoiced amount.",),
        'expense_sum_cash':fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart expense sum cash',multi='all',help="Approved invoiced amount.",),
        'expense_sum_budget':fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart expense sum budget',multi='all',help="Approved invoiced amount.",),
    }

    _defaults = {
        'prepayment': True,
        'smart_cash': 0.0,
        'smart_budget': 0.0,
    }

    @api.one
    def expense_cash(self):
        return self.env['hr.expense.expense'].browse(self.env['hr.expense.expense'].search(['&',('company_id','=',self.id),('state','in',('accepted','done','paid'))],context=context), context=context)
    @api.one
    def expense_budget(self):
        return self.env['hr.expense.expense'].browse(self.env['hr.expense.expense'].search(['&',('company_id','=',self.id),('state','in',('confirm'))],context=context), context=context)
    @api.one
    def order_cash(self):
        return self.env['sale.order'].browse(self.env['sale.order'].search(['&',('company_id','=',self.id),('state','in',('progress','manual','done'))],context=context), context=context)
    @api.one
    def order_budget(self):
        return self.env['sale.order'].browse(self.env['sale.order'].search(['&',('company_id','=',self.id),('state','in',('sent','waiting_date'))],context=context), context=context)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
