# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools.float_utils import float_round as round

import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class hr_employee(models.Model):
    _inherit = "hr.employee"

    withhold_tax = fields.Float('Withhold Tax', digits=(2,2), help="Percentage tax to withhold"),
    education = fields.Selection([('basic', 'Basic'), ('bachelor', 'Partner'), ('postgrad', 'Post Graduate'), ('unknown', 'Unknown')], string='Education Level', help="Level of completed edcation",)
    marital = fields.Selection([('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced'), ('partner', 'Partner'), ('separated', 'Separated'), ('unknown', 'Unknown')], string='Marital Status')
    
