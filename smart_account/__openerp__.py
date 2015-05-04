{
    'name': 'SMart Account',
    'category': 'Website',
    'summary': 'Administer your account information on-line',
    'version': '1.2',
    'description': """
SMart Account
===========

Customers

http://design.desk.smart.centralprojects.be/activity/desktop/v0.1/purchase-orders/

        """,
    'author': 'Vertel AB',
    'depends': ['smart_common'],
    'data': [
        'views/templates.xml',
        'views/hr_view.xml',
    ],
    'demo': [ ],
    'installable': True,
    'application': True,
    'sequence': 50,
}
