# -*- coding: utf-8 -*-
import random

from openerp import SUPERUSER_ID
from openerp.osv import osv, orm, fields
from openerp.addons.web.http import request

class account_analytic_account(model.Model):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"


    @api.one
    def _compute_total_amount(self):
        pass

    @api.one
    def _compute_sale_order_sum_cash(self):
        
        pass

#    @api.multi
#    @api.depends('sale.order.amount_total','sale.order.amount_untaxed')
#    def _amounts_cash(self):
#        for account in self:
#            orders = self.pool.get('sale.order').browse(self.pool.get('sale.order').search(['&',('analytic_account_id','=',account.id),('state','in',('progress','manual','done'))]))
#            account.amount_untaxed = sum(o.amount_untaxed for o in orders)
#            account.amount = sum(o.amount_untaxed for o in orders)
            #account.amount_untaxed_cash = sum(o.amount_untaxed for o in orders)
            #account.amount_taxes_cash = sum(o.amount_tax for o in orders)
            #account.amount_total_cash = sum(o.amount_total for o in orders)
            orders = self.pool.get('sale.order').browse(self.pool.get('sale.order').search(['&',('analytic_account_id','=',account.id),('state','in',('sent','waiting_date'))]))
            #account.amount_untaxed_budget = sum(o.amount_untaxed for o in orders)
            #account.amount_taxes_budget = sum(o.amount_tax for o in orders)
            #account.amount_total_budget = sum(o.amount_total for o in orders)

#    @api.multi
#    @api.depends('sale.order.amount_total','sale.order.amount_untaxed')
#    def _expenses(self):
#        for eaccount in self:
#            expenses = self.pool.get('hr.expense.line').browse(self.pool.get('hr.expense.line').search(['&',('analytic_account_id','=',account.id),('state','in',('progress','manual','done'))]))
#            expenses = self.pool.get('hr.expense.line').browse(self.pool.get('hr.expense.line').search([('analytic_account_id','=',account.id),]))
            #account.expense_untaxed_cash = sum(e.amount_untaxed for e in expenses)
            #account.expense_taxes_cash = sum(e.amount_tax for e in expenses)
            #account.expense_total_cash = sum(e.amount_total for e in expenses)

    #expense_untaxed = fields.Float(compute='_expense')
    
