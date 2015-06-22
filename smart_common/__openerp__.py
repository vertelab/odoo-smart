{
    'name': 'SMart Common',
    'category': 'Website',
    'summary': 'Common design elemens for SMart forms and lists',
    'version': '1.4',
    'description': """
SMart Order
===========

http://design.desk.smart.centralprojects.be/activity/desktop/v0.1/purchase-orders/

        """,
    'author': 'Vertel AB',
    'depends': ['website', 'web','hr','hr_expense','sale'],
    'data': [
        'views/templates.xml',
        'views/res_users_view.xml',
        'views/res_company_view.xml',
        'data/res_users_action.xml',
        'data/base_language.xml',
        'security/smart_groups.xml',
        'security/smart_rules.xml',
        'security/ir.model.access.csv', 
    ],
    'demo': [ ],
    'installable': True,
    'application': False,
}
