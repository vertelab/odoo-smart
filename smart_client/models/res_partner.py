# -*- coding: utf-8 -*-
import random

from openerp import SUPERUSER_ID
from openerp.addons.web.http import request
from openerp import models, fields, api, _


class res_partner(models.Model):
    _inherit = "res.partner"
    
    def _client_contact_counter(self):
        for partner in self:
            partner.client_contact_counter = len(partner.child_ids)

    client_contact_counter = fields.Integer(compute='_client_contact_counter')



