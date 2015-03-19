{
    'name': 'SMart Salary Simulator - ib',
    'category': 'Website',
    'summary': 'Webpage as Salary Simulator - IB',
    'version': '1.0',
    'description': """
SMart Account
===========


        """,
    'author': 'Vertel AB',
    'depends': ['website','smart_common', 'hr_payroll'],
    'data': [
        'views/templates.xml',
        'views/sim_se_template.xml',
        'salary_calculator.xml',
        'data/data.xml',
    ],
    'demo': [ ],
    'installable': True,
    'application': True,
    'sequence': 60,
}
