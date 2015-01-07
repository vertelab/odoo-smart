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
    'name': 'Account invoice submitted',
    'version': '1.1',
    'author': 'Vertel AB',
    'category': 'Sale',
    'website': 'http://www.vertel.se',
    'summary': 'Adds a new step in the invoice workflow',
    'description': """
     Adds a new step in the invoice workflow, submitted by a smart user to be accepted by an advicor
        
Sponsor:
SMart EU
70 rue Emile Feron
1060 Brussels, Belgium

    """,
    
    'depends': ['account'],
    'data': [
#        'account_invoice_workflow.xml',
        'account_invoice_view.xml',
       
    ],
    'installable': True,
  
    'auto_install': False,
    'sequence': 1,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
