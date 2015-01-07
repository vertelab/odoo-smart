# -*- coding: utf-8 -*-
import random

from openerp import SUPERUSER_ID
from openerp.osv import osv, orm, fields
from openerp.addons.web.http import request

class sale_order(osv.Model):
    _inherit = "sale.order"

    _columns = {
        'project_id': fields.many2one('project.project',"Project",),
        'description': fields.text("Description",),
    }


class account_tax(osv.Model):
    _inherit = "account.tax"

    _columns = {
        'active_web': fields.boolean('Active Web'),
    }


