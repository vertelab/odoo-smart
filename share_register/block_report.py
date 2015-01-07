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

from datetime import time, date

from openerp.osv import osv
from openerp.report import report_sxw
from openerp import api, models


class block_data(report_sxw.rml_parse,):
    _name = 'report.account.account.balance'

    def __init__(self, cr, uid, name, context=None):
        super(block_data, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'date':date,
            'get_block': self._get_block,
        })
        self.context = context

    def _get_block(self):
        if self.context.get('active_ids') and len(self.context['active_ids']) > 0:
            block_pool = self.pool.get('share.block')
            block_ids = block_pool.search(self.cr, self.uid, [('company_id', '=', self.context['active_ids'][0])])
            if block_ids:
                return block_pool.browse(self.cr, self.uid, block_ids)
        return ""

    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids
        return super(block_data, self).set_context(objects, data, new_ids, report_type=report_type)


class ParticularReport(models.AbstractModel):
    _name = 'report.share_register.report_block'
    _inherit = 'report.abstract_report'
    _template = 'share_register.report_block'
    _wrapped_report_class = block_data

