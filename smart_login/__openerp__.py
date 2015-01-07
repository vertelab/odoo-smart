{
    'name': 'SMart Login',
    'category': 'Website',
    'summary': 'Login and logout for SMart-users',
    'version': '1.0',
    'description': """
SMart Login
===========

login, logout, signup, reset password



        """,
    'author': 'Vertel AB',
    'depends': ['website','smart_common','hr','smart_dashboard'],
#    'depends': ['website','smart_common','smart_cash','smart_expense','smart_account'],
    'data': [
        'views/templates.xml',
        'models/res_users_action.xml',
#        'views/res_users_view.xml',
    ],
    'demo': [ ],
    'installable': True,
    'application': True,
    'sequence': 50,
}
