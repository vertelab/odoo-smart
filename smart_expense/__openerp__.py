{
    'name': 'SMart Expense',
    'category': 'Website',
    'summary': 'Create your Expense notes on-line',
    'version': '0.1',
    'description': """
SMart Expense
===========


        """,
    'author': 'Vertel AB',
    'depends': ['website', 'hr_expense','account','project',],
    'data': [
        'views/templates.xml',
        'views/product_view.xml',
    ],
    'demo': [ ],
    'installable': True,
    'application': False,
    'sequence': 80,
}
