# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

import re

from openerp.osv import fields


import logging
_logger = logging.getLogger(__name__)

  
class website_order(http.Controller):

    @http.route(['/cash/list',], type='http', auth="user", website=True)
    def cash_list(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang

        order_cash = pool.get('sale.order').browse(cr, uid, pool.get('sale.order').search(cr,uid,['&',('company_id','=',res_user.company_id.id),('state','in',('progress','manual','done'))],context=context), context=context)

        order_sum = 0.0
        for o in order_cash:
            order_sum += o.amount_untaxed

        expense_cash = pool.get('hr.expense.expense').browse(cr, uid, pool.get('hr.expense.expense').search(cr,uid,['&',('company_id','=',res_user.company_id.id),('state','in',('accepted','done','paid'))],context=context), context=context)

        expense_sum = 0.0
        for e in expense_cash:
#            expense_sum -= e.amount
            try:
                expense_sum -= e.amount_untaxed
            except Exception, ex:
                _logger.warning("Having trouble with e.amount_untaxed %s (%s) " % (ex,e))
                
        values = {
            'context': context,
            'cash_menu': 'active',            
            'res_user': res_user,
            'sale_orders': order_cash,
#            'sale_orders_sum': order_sum,
            'expenses': expense_cash,
#            'expenses_sum': expense_sum,
            'smart_share': res_user.company_id.smart_share,
#            'smarts_amount'   : order_sum * (res_user.company_id.smart_share / 100),
#            'activitys_amount': order_sum * (1 - (res_user.company_id.smart_share / 100)),
        }
        return request.website.render("smart_cash.list",values)
 
 
 
    @http.route(['/budget/list',], type='http', auth="user", website=True)
    def budget_list(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang

        order_budget = pool.get('sale.order').browse(cr, uid, pool.get('sale.order').search(cr,uid,['&',('company_id','=',res_user.company_id.id),('state','in',('sent','waiting_date'))],context=context), context=context)


        order_sum = 0
        for o in order_budget:
#            order_sum += o.amount_total
            order_sum += o.amount_untaxed

        expense_budget = pool.get('hr.expense.expense').browse(cr, uid, pool.get('hr.expense.expense').search(cr,uid,['&',('company_id','=',res_user.company_id.id),('state','in',('confirm',))],context=context), context=context)

        expense_sum = 0
        for e in expense_budget:
            expense_sum -= e.amount 

        values = {
            'context': context,
            'budget_menu': 'active',            
            'res_user': res_user,
            'sale_orders': order_budget,
#           'sale_orders_sum': order_sum * (1 - (res_user.company_id.smart_share / 100)),
            'expenses': expense_budget,
#           'expenses_sum': expense_sum,
            'smart_share': res_user.company_id.smart_share,
#            'smarts_amount': order_sum * (res_user.company_id.smart_share / 100),
#            'activitys_amount': order_sum * (1 - (res_user.company_id.smart_share / 100)),
        }
        return request.website.render("smart_cash.list",values)

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
