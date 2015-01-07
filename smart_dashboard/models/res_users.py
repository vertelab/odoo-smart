# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from datetime import datetime, timedelta
import random
from urlparse import urljoin
import werkzeug

from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, ustr
from ast import literal_eval
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import logging


_logger = logging.getLogger(__name__)

class res_users(osv.Model):
    _inherit = 'res.users'

    def _get_state(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for user in self.browse(cr, uid, ids, context):
            if user.approved:
                res[user.id] = 'approved'
            elif user.login_date:
                res[user.id] = 'active'
            else:
                res[user.id] = 'new'
        return res

    _columns = {
        'state': fields.function(_get_state, string='Status',  type='selection', 
                    selection=[('new', 'Never Connected'), ('active', 'WebUser'),('approved', 'SmartUser')],), 
        'approved': fields.boolean('Approved',),
        'webterms_accepted': fields.boolean('Web Terms Accepted',),
        
    }