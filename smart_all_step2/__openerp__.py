# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2014 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'SMart All Step 2',
    'version': '1.3',
    'author': 'Vertel AB',
    'category': 'Base',
    'website': 'http://www.vertel.se',

    'description': """ Depends and install all modules that SMart EU needs. Use this module with --load-parameter to the server """,
#    'depends': ["virtual_company","smart_cash","account_report","account_invoice_submitted","ir_sequence_country","l10n_se","sale_sequence","web_smartux"],
#    'depends': ["account","sale","project","hr_expense","smart_multicompany","smart_common","smart_account","smart_salary_simulator","smart_client","smart_order","smart_project","smart_activity","smart_dashboard"],
    'depends': ["account","sale","project","hr_expense","smart_common","smart_account","smart_salary_simulator","smart_client","smart_order","smart_project","smart_dashboard","smart_alias",],

    'data': [],
    'installable': True,
    'auto_install': False,
    'application': True,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
