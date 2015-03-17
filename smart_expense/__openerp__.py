{
    'name': 'SMart Expense',
    'category': 'Website',
    'summary': 'Create your Expense notes on-line',
    'version': '0.2',
    'description': """
SMart Expense
===========


        """,
    'author': 'Vertel AB',
    'depends': ['website', 'hr_expense','account','project',],
    'data': [
        'views/templates.xml',
        'views/product_view.xml',
        'views/templates_expense_forms.xml',        
    ],
    'demo': [ ],
    'installable': True,
    'application': False,
    'sequence': 80,
}
