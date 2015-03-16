# -*- coding: utf-8 -*-
import werkzeug

from openerp import http, fields, _
from openerp.http import request

import logging

_logger = logging.getLogger(__name__)

                
class website_client(http.Controller):
    
    @http.route(['/salary/simulator'], type='http', auth="public", website=True)
    def salary_simulation(self, **post):
        env = request.env
        
        user = env['res.users'].browse(env.uid)[0]
        if user.employee_ids and user.employee_ids[0].contract_ids:
            employee = user.employee_ids[0]
            contract = employee.contract_ids[0]
        else:
            employee = env.ref('smart_salary_simulator.dummy_employee')
            contract = env.ref('smart_salary_simulator.smart_contract_musician')
        _logger.info(employee.name)
        if request.httprequest.method == 'POST':
            values = {
                'salary': float(post.get('salary-amount') or 0),
                'yob': int(post.get('salary-birth-year') or 0),
                'tax': float(post.get('salary-tax-prct') or 0),
                'expenses': float(post.get('salary-expense') or 0),
            }
            if post.get('sender') == 'form':
                payslip = env['hr.payslip'].create({
                    'struct_id': contract.struct_id.id,
                    'employee_id': employee.id,
                    'date_from': fields.Date.today(),
                    'date_to': fields.Date.today(),
                    'state': 'draft',
                    'contract_id': contract.id,
                    'input_line_ids': [
                        (0, _, {
                            'name': 'Salary Base',
                            'code': 'SALARY',
                            'contract_id': contract.id,
                            'amount': values['salary'],
                        }),
                        (0, _, {
                            'name': 'Year of Birth',
                            'code': 'YOB',
                            'contract_id': contract.id,
                            'amount': values['yob'],
                        }),
                        (0, _, {
                            'name': 'Withholding Tax Rate',
                            'code': 'WT',
                            'contract_id': contract.id,
                            'amount': values['tax'],
                        }),
                        (0, _, {
                            'name': 'Expenses',
                            'code': 'EXPENSES',
                            'contract_id': contract.id,
                            'amount': values['expenses'],
                        }),
                        (0, _, {
                            'name': 'Current Year',
                            'code': 'YEAR',
                            'contract_id': contract.id,
                            'amount': fields.Date.from_string(fields.Date.today()).year,
                        }),
                        ]
                })
                lines = payslip.simulate_sheet()
                #payslip.unlink()
                values['lines'] = lines
                
                for line in lines:
                    if line['code'] == 'NET':
                        values['net'] = float(line['quantity']) * line['amount'] * line['rate'] / 100
                return request.website.render("smart_salary_simulator.result_se", values)
            elif post.get('sender') == 'result':
                return request.website.render("smart_salary_simulator.simulator_form_se", values)
        else:
            
            #TODO: Get tax from wherever
            
            values = {
                'salary': contract.wage or 1000,
                'yob': (employee.birthday and fields.Date.from_string(employee.birthday).year) or 1990,
                'tax': 30.0,
                'expenses': 0,
            }
            return request.website.render("smart_salary_simulator.simulator_form_se", values)
        """
        env = request.env
        if user and user.employee_ids and user.employee_ids[0].contract_id:
            employee = user.employee_ids[0]
        else:
            employee = env['hr.employee'].search([['id', '=', 13]])[0]
            #TODO: Get default employee with ref
        
        contracts = env['hr.contract'].search([['employee_id', '=', employee.id]])
        contract_list = []
        use_default = True
        for c in contracts:
            contract_list.append([c.id, c.name, False])
            if post and c.id == post.get('selected_contract'):
                contract = c
                contract_list[-1][2] = True
                use_default = False
        if use_default:
            contract = contracts[0]
            contract_list[0][2] = True

        payslip = env['hr.payslip'].create({
        'struct_id': contract.struct_id.id,
        'employee_id': employee.id,
        'date_from': fields.Date.today(),
        'date_to': fields.Date.today(),
        'state': 'draft',
        'contract_id': contract.id,
        })
        
        if post:
            contract.wage = base_amount = post.get('salary')
        else:
            contract.wage = base_amount = 1000
        
        lines = payslip.simulate_sheet()
        payslip.unlink()
        lines_list = []
        for line in lines:
            lines_list.append([line['name'], float(line['quantity']) * line['amount'] * line['rate'] / 100])

        values = {
        'contracts': contract_list,
        'base_amount': base_amount,
        'lines': lines_list,
        }
        
        
        return request.website.render("smart_salary_simulator.sim_%s" %  request.env['res.users'].browse(request.uid).company_id.country_id.code.lower() , values)
        """

    @http.route(['/salary/simulator/get_lines'], type='json', auth="public", website=True)
    def get_lines(self, contract_id=None, salary=1000.0, **post):
        _logger.info(contract_id)
        env = request.env
        if not contract_id:
            return [{'result':'<div class="foobargazonksvinollon">No contract found</div>'}]
        contract = env['hr.contract'].browse(int(contract_id))[0]
        wage = contract.wage or 0.0
        contract.wage = float(salary)
        payslip = env['hr.payslip'].create({
        'struct_id': contract.struct_id.id,
        'employee_id': contract.employee_id.id,
        'date_from': fields.Date.today(),
        'date_to': fields.Date.today(),
        'state': 'draft',
        'contract_id': contract.id,
        })
        lines = payslip.simulate_sheet()
        payslip.unlink()
        contract.wage = wage
        
        lines_list = []
        for line in lines:
            lines_list.append([line['name'], float(line['quantity']) * line['amount'] * line['rate'] / 100])
        
        return {'lines': lines_list}
    
    @http.route(['/salary/sim/calc'], type='http', auth="user", website=True)
    def salary_simulation_frame(self, order=False):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        values = {}
        
        return request.website.render("smart_salary_simulator.sim_frame_%s" %  pool.get('res.users').browse(cr, uid, uid).company_id.country_id.code.lower() , values)

    @http.route(['/salary/sim',
#        '/salary/<int:user>'
    ], type='http', auth="public", website=True)
    def salary(self, user=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang

        values = {
            'salarysimulator_menu': 'active',        
            'context': context,
            'res_user': res_user,
        }
        return request.website.render("smart_salary_simulator.simulator_%s" %  pool.get('res.users').browse(cr, uid, uid).company_id.country_id.code.lower() , values)


#~ class QueryURL(object):
    #~ def __init__(self, path='', **args):
        #~ self.path = path
        #~ self.args = args
#~ 
    #~ def __call__(self, path=None, **kw):
        #~ if not path:
            #~ path = self.path
        #~ for k,v in self.args.items():
            #~ kw.setdefault(k,v)
        #~ l = []
        #~ for k,v in kw.items():
            #~ if v:
                #~ if isinstance(v, list) or isinstance(v, set):
                    #~ l.append(werkzeug.url_encode([(k,i) for i in v]))
                #~ else:
                    #~ l.append(werkzeug.url_encode([(k,v)]))
        #~ if l:
            #~ path += '?' + '&'.join(l)
        #~ return path

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
