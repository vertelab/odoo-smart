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
    'name': 'Share Register',
    'version': '2.1',
    'author': 'Vertel AB',
    'category': 'base',
    'website': 'http://www.vertel.se',
    'summary': 'Registry with share blocks, shareholders, stakeholders and partowners on blocks.)',
    'description': """
Share Registry
==============

Sponsor:
KE-Group

    """,
    'depends': ['base_setup', 'base', 'mail', 'account', 'report','contacts','sale'],
    'data': [
        'company_view.xml',
        'res_partner_view.xml',
        'share_register_view.xml',
        'views/report_block.xml',
        'views/layouts.xml',
        'block_report.xml',
#        'demo/multi_company_demo_fredrik2.xml',
#        'demo/res.partner.csv',
#        'demo/res.company.csv',
#        'demo/share.block.csv',
#        'demo/share.share.csv'
            ],
    'installable': True,
    'application': True,
    'auto_install': False,
#    'demo': ['demo/res.partner.csv','demo/res.company.csv','demo/share.block.csv','demo/share.share.csv','demo_after/res.partner.csv']
    'demo': [
        'demo/multi_company_demo_fredrik2.xml',
#        'demo/res.partner.csv',
#        'demo/res.company.csv',
#        'demo/share.block.csv',
#        'demo/share.share.csv'
]

}

#
# Wishlist for next version
# Hide Shares for partners is not Company
# Track visibility for Field type boleean,


# # How to create the company list
# Step 1
# Import a list of Partners
#
# File partners.csv
# id	name
# __export__.res_partner_10	KE Group Holding
# __export__.res_partner_11	Bright Water Fish AB
# __export__.res_partner_12	Dunusi S.A.
# __export__.res_partner_13	Brock Investments Ltd.
# __export__.res_partner_14	Gamma Knife Center Ecuador S.A.
# __export__.res_partner_15	Affoit Investments Ltd.
# __export__.res_partner_16	South Harting Enterprice Corp.
# __export__.res_partner_17	Grand Maria Explorations
# __export__.res_partner_18	Tingen Ltd.
# __export__.res_partner_19	Gamma Knife Holdings Ltd.
# __export__.res_partner_20	United Sun Systems International
# __export__.res_partner_21	WaveRoller Inc.
# __export__.res_partner_22	North Sea Diving Ltd.
# __export__.res_partner_23	Tillington Investments Ltd.
# __export__.res_partner_24	Management Services Ltd.
# __export__.res_partner_25	Barham Ltd.
# __export__.res_partner_26	Tunnin Ltd
# __export__.res_partner_27	Munnio Ltd
# __export__.res_partner_28	Diluvien Ltd
# __export__.res_partner_29	Itgamma S.A.
# __export__.res_partner_3	KE-Group Test
#
# Step 2
# Then Import a list of Companies
#
# File cmpanies.csv
# id	partner_id/id	name
# __export__.res_company_10	__export__.res_partner_10	KE Group Holding
# __export__.res_company_11	__export__.res_partner_11	Bright Water Fish AB
# __export__.res_company_12	__export__.res_partner_12	Dunusi S.A.
# __export__.res_company_13	__export__.res_partner_13	Brock Investments Ltd.
# __export__.res_company_14	__export__.res_partner_14	Gamma Knife Center Ecuador S.A.
# __export__.res_company_15	__export__.res_partner_15	Affoit Investments Ltd.
# __export__.res_company_16	__export__.res_partner_16	South Harting Enterprice Corp.
# __export__.res_company_17	__export__.res_partner_17	Grand Maria Explorations
# __export__.res_company_18	__export__.res_partner_18	Tingen Ltd.
# __export__.res_company_19	__export__.res_partner_19	Gamma Knife Holdings Ltd.
# __export__.res_company_20	__export__.res_partner_20	United Sun Systems International
# __export__.res_company_21	__export__.res_partner_21	WaveRoller Inc.
# __export__.res_company_22	__export__.res_partner_22	North Sea Diving Ltd.
# __export__.res_company_23	__export__.res_partner_23	Tillington Investments Ltd.
# __export__.res_company_24	__export__.res_partner_24	Management Services Ltd.
# __export__.res_company_25	__export__.res_partner_25	Barham Ltd.
# __export__.res_company_26	__export__.res_partner_26	Tunnin Ltd
# __export__.res_company_27	__export__.res_partner_27	Munnio Ltd
# __export__.res_company_28	__export__.res_partner_28	Diluvien Ltd
# __export__.res_company_29	__export__.res_partner_29	Itgamma S.A.
# __export__.res_company_3	__export__.res_partner_3	KE-Group Test




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
