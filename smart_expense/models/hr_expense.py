# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp


import logging
_logger = logging.getLogger(__name__)


class hr_expense_line(osv.osv):
    _inherit = "hr.expense.line"

    def _untaxed(self, cr, uid, ids, name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):  
            res[line.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
            }
            if line.unit_amount_untaxed == 0:
                for c in self.pool.get('account.tax').compute_all(cr, uid, line.product_id.product_tmpl_id.taxes_id, line.unit_amount, line.unit_quantity, line.product_id, line.expense_id.user_id.partner_id)['taxes']:
                    res[line.id]['amount_tax'] += c.get('amount', 0.0)
            else:
                res[line.id]['amount_tax'] = line.total_amount - (line.unit_amount_untaxed * line.unit_quantity)
            res[line.id]['amount_untaxed'] = float(line.total_amount - res[line.id]['amount_tax'])
            _logger.warning("function _untaxed This is my expense res %s" % (res))

        return res


    _columns = {
        'justification': fields.char('Justification for this expense', ),
        'from': fields.char('From', ),
        'to': fields.char('To', ),
        'distance': fields.integer('Distance, km', ),        
        'amount_untaxed': fields.function(_untaxed, type="float", digits_compute=dp.get_precision('Account'), string='Untaxed',multi='all',help="Expense amount without tax.",),
        'amount_tax': fields.function(_untaxed,     type="float", digits_compute=dp.get_precision('Account'), string='Tax',    multi='all',help="Expense tax.",),
        'unit_amount_untaxed': fields.float('Unit Price without tax', digits_compute=dp.get_precision('Product Price')),
        }
        

class hr_expense_expense(osv.osv):
    _inherit = "hr.expense.expense"

    def _untaxed(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for expense in self.browse(cr, uid, ids, context=context):
            res[expense.id] = {
                    'amount_untaxed': 0.0,
                    'amount_tax': 0.0,
            }
            for line in expense.line_ids:
                res[expense.id]['amount_untaxed'] = float(res[expense.id]['amount_untaxed'] + line.amount_untaxed)
                res[expense.id]['amount_tax']     = float(res[expense.id]['amount_tax'] + line.amount_tax)
        return res
            
    _columns = {
        'amount_untaxed': fields.function(_untaxed, string='Untaxed Amount', type="float",digits_compute=dp.get_precision('Account'), multi='all'),
        'amount_tax': fields.function(_untaxed, string='Tax Amount',         type="float",digits_compute=dp.get_precision('Account'), multi='all'),
    }
    


class product_template(osv.osv):
    _inherit = "product.template"

    _columns = {
        'template_xml': fields.text('Template XML',),
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
