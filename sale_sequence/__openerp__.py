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
    'name': 'Sale sequence',
    'version': '1.1',
    'author': 'Vertel AB',
    'category': 'Sale',
    'website': 'http://www.vertel.se',
    'summary': 'Sale Sequence Country',
    'description': """
     Adds country to sale order sequence  eg SESO001
        
Sponsor:
SMart EU
70 rue Emile Féron
1060 Brussels, Belgium

    """,
    
    'depends': ['sale'],
    'data': [
        'sale_sequence.xml',
       
    ],
    'installable': True,
  
    'auto_install': False,
    'sequence': 99,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
