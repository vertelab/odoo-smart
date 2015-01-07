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
import logging
from datetime import datetime, date, timedelta
import time
from lxml import etree
import openerp.addons.decimal_precision as dp
import openerp.exceptions

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    
    def _smart_cash(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = {
 #               'smart_cash': invoice.amount_total - invoice.residual,
                'smart_budget': 0.0,
                'smart_cash': 0.0,
                'smart_cash_date': invoice.date_due or date.today().isoformat(),
#                'smart_cash_date': date(*time.strptime(invoice.date_invoice,'%Y-%m-%d')[:3]) + timedelta(days=invoice.company_id.parent_id.prepayment_days)
            }
            if type(res[invoice.id]['smart_cash_date']) == 'bool':
                res[invoice.id]['smart_cash_date'] = date.today()
            _logger.info("type smart_cash_date %s type %s " % (res[invoice.id]['smart_cash_date'],type(res[invoice.id]['smart_cash_date'])))                
            _logger.info("res smart_cash_date %s " % datetime.strptime(res[invoice.id]['smart_cash_date'],'%Y-%m-%d').date())
            #_logger.info("smart_cash_date %s today %s" % (datetime.strptime(res[invoice.id]['smart_cash_date'],'%Y-%m-%d').date(),date.today()))
            #
            # SMart Cash are accessible when 1) status are paid 2) date_due have passed 3) if the smart organisation administer prepayment after prepayment days
            #
            if invoice.company_id.parent_id.id and invoice.company_id.parent_id.prepayment and invoice.company_id.parent_id.prepayment_days > 0:
                res[invoice.id]['smart_cash_date'] = invoice.date_invoice + timedelta(days=invoice.company_id.parent_id.prepayment_days)
            _logger.info("res2 smart_cash_date %s " % datetime.strptime(res[invoice.id]['smart_cash_date'],'%Y-%m-%d').date())

            if invoice.state in ['paid']:
                    res[invoice.id]['smart_cash'] = invoice.amount_total
            else:
                if invoice.state in ['open']:
                    if date.today() >= datetime.strptime(res[invoice.id]['smart_cash_date'],'%Y-%m-%d').date():
                        _logger.info("smart_cash_date %s today %s" % (datetime.strptime(res[invoice.id]['smart_cash_date'],'%Y-%m-%d').date(),date.today()))
                        res[invoice.id]['smart_cash'] = invoice.amount_total
        return res

    _columns = {
       'smart_budget': fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Budget',
            help="Approved amount.",
            multi='all'),
       'smart_cash': fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Cash',
            help="Free invoiced amount for salary or expenses.",
            multi='all'
        ),
       'smart_cash_date': fields.function(_smart_cash, type="date", string='SMart Cash Release date',
            help="Date when this amount is released.",
            multi='all'
        ),

    }



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
