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
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round


import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class account_move(osv.osv):
    _inherit = "account.move"
    
    def _smart_cash(self, cr, uid, ids, name, args, context=None):
        res = {}
        for move in self.browse(cr, uid, ids, context=context):
            res[move.id] = {
 #               'smart_cash': invoice.amount_total - invoice.residual,
                'smart_cash': move.balance,
                'smart_budget': move.amount,
                'smart_cash_date': date.today().isoformat(),
#                'smart_cash_date': date(*time.strptime(invoice.date_invoice,'%Y-%m-%d')[:3]) + timedelta(days=invoice.company_id.parent_id.prepayment_days)
            }
            if type(res[move.id]['smart_cash_date']) == 'bool':
                res[move.id]['smart_cash_date'] = date.today()
#            _logger.info("type smart_cash_date %s type %s " % (res[move.id]['smart_cash_date'],type(res[move.id]['smart_cash_date'])))                
#            _logger.info("res smart_cash_date %s " % datetime.strptime(res[move.id]['smart_cash_date'],'%Y-%m-%d').date())
            #_logger.info("smart_cash_date %s today %s" % (datetime.strptime(res[move.id]['smart_cash_date'],'%Y-%m-%d').date(),date.today()))
            #
            # SMart Cash are accessible when 1) status are paid 2) date_due have passed 3) if the smart organisation administer prepayment after prepayment days
            #
            if move.company_id.parent_id.id and move.company_id.parent_id.prepayment and move.company_id.parent_id.prepayment_days > 0:
                res[move.id]['smart_cash_date'] = move.date + timedelta(days=move.company_id.parent_id.prepayment_days)
#            _logger.info("res2 smart_cash_date %s " % datetime.strptime(res[move.id]['smart_cash_date'],'%Y-%m-%d').date())

            if move.state in ['posted']:
                    res[move.id]['smart_cash'] = move.amount
            else:
                if move.state in ['open',]:
                    if date.today() >= datetime.strptime(res[move.id]['smart_cash_date'],'%Y-%m-%d').date():
                        _logger.info("smart_cash_date %s today %s" % (datetime.strptime(res[move.id]['smart_cash_date'],'%Y-%m-%d').date(),date.today()))
                        res[move.id]['smart_cash'] = move.amount
            if move.journal_id.code in ['EXJ']:
                res[move.id]['smart_cash'] = res[move.id]['smart_cash'] * -1
                
        return res

    _columns = {
       'smart_budget': fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Budget',
            help="Approved amount.",
            multi='all'
        ),

       'smart_cash': fields.function(_smart_cash, type="float", digits_compute=dp.get_precision('Account'), string='SMart Cash',
            help="Available amount for salary or expenses.",
            multi='all'
        ),
       'smart_cash_date': fields.function(_smart_cash, type="date", string='SMart Cash Release date',
            help="Date when this amount is released.",
            multi='all'
        ),

    }



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
