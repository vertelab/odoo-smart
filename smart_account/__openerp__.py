{
    'name': 'SMart Account',
    'category': 'Website',
    'summary': 'Administer your account information on-line',
    'version': '1.1',
    'description': """
SMart Account
===========

Customers

http://design.desk.smart.centralprojects.be/activity/desktop/v0.1/purchase-orders/

        """,
    'author': 'Vertel AB',
    'depends': ['website','smart_common','hr'],
    'data': [
        'views/templates.xml',
        'views/hr_view.xml',
    ],
    'demo': [ ],
    'installable': True,
    'application': True,
    'sequence': 50,
}
