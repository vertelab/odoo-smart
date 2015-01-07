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
    'name': 'SMart Budget and Cash',
    'version': '1.0',
    'author': 'Vertel AB',
    'category': 'SMart',
    'website': 'http://www.vertel.se',
    'summary': 'Calculate advance Budget and Cash',
    'description': """
Calculate advance cash
======================
For a virtual company, smart_cash is their operating space for different types of payments. 
smart_cash is calculated as: "the invoiced amount" a "SMart User" can use on his/her account. 
SMartCash includes advancement of salary and excludes Expenses and Salary.

* Customer - check the available credit limit
* Company (virtual company) - check if payment-advancement is true
* Company (SMart company/country) - check if payment-advancement is true

account.invoice 
smart_budget = approved invoiced amount

res.company:
smart_budget = all account.invoice.smart_budget
prepayment: boolean


SMartBudget =  Approved Invoices - SMartShare - Approved Expenses 
SMartCash =  Advanced Invoices + Client payments - SMartShare - Paid Expenses 

** Notes in Swedish below: **

smartcash förskottera

Kunden är kreditvärdig -- kreditsumman 
Projektet är kreditvärdig -- (virt comp är kreditvärdig, default godkänd) 
Landet erbjuder kredit - förskottering, ej så är det riktiga ibet pengar

pengar tillgänglig mellan 5 - 10 dgr efter godkännandet 
antal dagar per företag

utgifter, utbetalning minskar cashbeloppet så snart den är godkänd -- se hur mycket cash 

lön betalas ut första dagen det finns pengar - cash nog 

filen cash flow

-----

listor: lägg till budget och cash-kolumn

attr virt företag, 

Sponsor:
SMart EU
70 rue Emile Féron
1060 Brussels, Belgium

    """,
    'depends': ['base','account','sale','smart_expense','smart_common'],
#    'depends': ['base','account','smart_common','smart_expense'],
    'data': [ 
        'views/company_view.xml',
        'views/account_invoice_view.xml',
        'views/account_view.xml',
        'views/templates.xml',],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
