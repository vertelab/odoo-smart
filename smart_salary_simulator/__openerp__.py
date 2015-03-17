{
    'name': 'SMart Salary Simulator',
    'category': 'Website',
    'summary': 'Webpage as Salary Simulator',
    'version': '1.0',
    'description': """
SMart Account
===========

Customers

http://design.desk.smart.centralprojects.be/activity/desktop/v0.1/purchase-orders/

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
