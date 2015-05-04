{
    'name': 'SMart Order',
    'category': 'Website',
    'summary': 'Create your invoices on-line',
    'version': '1.2',
    'description': """
SMart Order
===========

http://design.desk.smart.centralprojects.be/activity/desktop/v0.1/purchase-orders/

        """,
    'author': 'Vertel AB',
    'depends': ['smart_common', 'sale','account','project','base_iban'],
    'data': [
        'views/templates.xml',
        'views/account_view.xml',
        'views/sale_view.xml',        
    ],
    'demo': [ ],
    'installable': True,
    'application': False,
    'sequence': 80,
}
