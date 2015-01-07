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
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.modules.module import get_module_resource
from openerp.osv import fields, osv
from openerp.tools.translate import _


_logger = logging.getLogger(__name__)



class ir_sequence(osv.osv):
    """ Sequence model.

    The sequence model allows to define and use so-called sequence objects.
    Such objects are used to generate unique identifiers in a transaction-safe
    way.

    """
    _name = 'ir.sequence'
    _inherit = ['ir.sequence']


    def _interpolation_dict(self):
        #_logger.debug("Self %r", self.code)
        res = super(ir_sequence, self)._interpolation_dict() 
        res['country'] = self.code 
#        res['country'] = self.code.upper() 
        return  res
        
        
    def _next(self, cr, uid, seq_ids, context=None):
        self.code = self.pool.get('res.users').browse(cr, uid, uid).company_id.country_id.code
        return super(ir_sequence, self)._next(cr, uid, seq_ids, context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
