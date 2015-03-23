# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerp
from openerp import models, fields, api, _, tools



class res_partner(models.Model):
    _inherit = "res.partner"

    smart_bank_account_type = fields.Char(string='Bank Account Type',size=60,)
    smart_bank_name         = fields.Char(string='Bank name',size=60,)
    smart_bank_branch       = fields.Char(string='Branch name',size=60,)
    smart_bank_code         = fields.Char(string='Bank code',size=60,)
    smart_bank_acc_no       = fields.Char(string='Account No',size=60,)
    smart_bank_acc_iban     = fields.Char(string='IBAN',size=60,)
    smart_bank_acc_bic      = fields.Char(string='BIC / SWIFT',size=60,)
    smart_work_roles        = fields.Char(string='Your workroles',size=100,)
    dropbox_link            = fields.Char(string='Your documents',size=100,)
    smart_place_of_birth    = fields.Char(string='Place of Birth',size=100,)
    
    
    
class website(models.Model):
    _inherit = 'website'

    #~ company = fields.Many2one('res.company', string="Company",default=lambda self: self.env['ir.model.data'].xmlid_to_res_id(openerp.SUPERUSER_ID, 'base.public_user'))
    smart_company = fields.Many2one('res.company', string="Company",default=1)
