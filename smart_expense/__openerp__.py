{
    'name': 'SMart Expense',
    'category': 'Website',
    'summary': 'Create your Expense notes on-line',
    'version': '0.3',
    'description': """
SMart Expense
===========


        """,
    'author': 'Vertel AB',
    'depends': ['smart_common', 'hr_expense','account','project',],
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
