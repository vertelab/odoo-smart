from openerp import api, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class hr_payslip(osv.osv):
    _inherit = 'hr.payslip'
    
    def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, bar, foo, context):
        _logger.info(cr)
        _logger.info(uid)
        _logger.info(contract_ids)
        _logger.info(payslip_id)
        _logger.info(context)
        _logger.info(foo)
        _logger.info(bar)
        return False
        
