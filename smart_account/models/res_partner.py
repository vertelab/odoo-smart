# -*- coding: utf-8 -*-
import random

from openerp import SUPERUSER_ID
from openerp.osv import osv, orm, fields
from openerp.addons.web.http import request



class res_partner(osv.Model):
    _inherit = "res.partner"

    _columns = {
        'smart_bank_account_type': fields.char('Bank Account Type',size=60,),
        'smart_bank_name': fields.char('Bank name',size=60,),
        'smart_bank_acc_no': fields.char('Account No',size=60,),
        'smart_bank_acc_iban': fields.char('IBAN',size=60,),
        'smart_bank_acc_bic': fields.char('BIC / SWIFT',size=60,),
        'dropbox_link': fields.char('Your documents',size=100,),
    }


class website(orm.Model):
    _inherit = 'website'

    def account_domain(self, cr, uid, ids, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return [("company_id", "=", user.company_id.id)]



