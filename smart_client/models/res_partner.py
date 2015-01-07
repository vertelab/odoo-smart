# -*- coding: utf-8 -*-
import random

from openerp import SUPERUSER_ID
from openerp.osv import osv, orm, fields
from openerp.addons.web.http import request



class res_partner(osv.Model):
    _inherit = "res.partner"

    def _get_errors(self, cr, uid, order, context=None):
        return []


class website(orm.Model):
    _inherit = 'website'

    def client_domain(self, cr, uid, ids, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return [("company_id", "=", user.company_id.id)]



