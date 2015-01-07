# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class hr_employee(osv.osv):
    _inherit = "hr.employee"

    _columns = {
        'withhold_tax': fields.float('Withhold Tax', digits=(2,2), help="Percentage tax to withhold"),
    }




