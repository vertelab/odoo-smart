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

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class res_company(osv.osv):
    _inherit = "res.company"

    def _share(self, cr, uid, ids, name, args, context=None):
        res = {}
        for company in self.browse(cr, uid, ids, context=context):
#            for invoice in self.pool.get('account.invoice').browse(cr, uid, self.pool.get('account.invoice').search(cr,uid,[company_id,'=',company.id],context=context), context=context):
#                res[company.id]['smart_cach'] =+ invoice.smart_cache,
            res[company.id]['share_capital_amount'] = 0.0
            res[company.id]['share_amount'] = 0
            res[company.id]['share_blocks_amount'] = 0
            res[company.id]['shareholders'] = 0
            for share in self.pool.get('share.share').browse(cr, uid, self.pool.get('share.share').search(cr, uid, [company_id, '=', company.id], context=context), context=context):
                res[company.id]['share_capital_amount'] += share.nominal_value
                res[company.id]['share_amount'] += 1
            for block in self.pool.get('share.block').browse(cr, uid, self.pool.get('share.block').search(cr, uid, [company_id, '=', company.id], context=context), context=context):
                res[company.id]['share_blocks_amount'] += 1
            res[company.id]['shareholders'] = len(sorted(set([share.owner_id for share in self.pool.get('share.share').browse(cr, uid, self.pool.get('share.share').search(cr, uid, [company_id, '=', company.id], context=context), context=context)])))
            res[company.id]['shareholder_ids'] = sorted(set([share.owner_id for share in self.pool.get('share.share').browse(cr, uid, self.pool.get('share.share').search(cr, uid, [company_id, '=', company.id], context=context), context=context)]))


        return res

    _columns = {
       'authorised_share_capital': fields.float('Authorised share capital', digits_compute=dp.get_precision('Account')),
       'share_capital': fields.integer('Share Capital', help="Number of shares",),
       'share_capital_amount': fields.function(_share, type="float", digits_compute=dp.get_precision('Account'), string='Share capital (amount)',
            help="Amount of share capital.",
            multi='all',),
       'share_total': fields.integer('Number of shares', help="Number of shares"),
       'share_blocks_amount': fields.function(_share, type="integer", string='Number of registered shares',
            help="Number of real shares in the system.",
            multi='all',),
#       'share_blocks': fields.function(_share, type="integer", string='Number of registered shares',
       'share_amount': fields.function(_share, type="integer", string='Number of registered shares',
            help="Number of real shares in the system.",
            multi='all',),
       'shareholders': fields.function(_share, type="integer", string='Number of shareholders',
            help="Number of real shareholders in the system.",
            multi='all',),
       'nominal_value': fields.float('Nominal value', digits_compute=dp.get_precision('Account')),
    }

    _defaults = {
        'share_capital': 0.0,
        'share_total': 0,
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

