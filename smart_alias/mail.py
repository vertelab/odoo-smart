from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class mail_alias(osv.osv):
    _inherit = 'mail.alias'

    _columns = {
            'company_id': fields.many2one('res.company', 'Company'),
    }
    
    _defaults = {
        'company_id': False,
    }
