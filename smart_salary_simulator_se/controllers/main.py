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
        request.context['lang'] = user.lang
        if request.httprequest.method == 'POST':
            values = {
                'salarysimulator_menu': 'active',        
                'context': request.context,
                'res_user': env['res.users'].browse(env.uid)[0],
                'salary': float(post.get('salary-amount') or 0),
                'yob': int(post.get('salary-birth-year') or 0),
                'tax': float(post.get('salary-tax-prct') or 0),
                'expenses': float(post.get('salary-expense') or 0),
                'vat': float(post.get('salary-vat-prct') or 0),
                'musician': post.get('salary-musician') or 'off',
                'smart_fee': float(post.get('salary-smart-fee') or 0),
                'res_user': user,
                'context': request.context,
            }
            if post.get('sender') == 'form':
                _logger.info(post)
                invoice_lines = [
                    {
                        'name': 'Total amount inclusive VAT',
                        'amount': values['salary'],
                    },
                    {
                        'name': 'VAT ( %)',
                        'amount': - values['salary'] * (1 - 100/ (100 + values['vat'])),
                    },
                    {
                        'name': 'Total amount exclusive VAT',
                        'amount': values['salary'] - values['salary'] * (1 - 100/ (100 + values['vat'])),
                    },
                    {
                        'name': "SMartSe's share 6.5%",
                        'amount': - values['smart_fee'] / 100 * (values['salary'] - values['salary'] * (1 - 100/ (100 + values['vat']))),
                    },
                    {
                        'name': "Amount on your SMart-Account",
                        'amount': values['salary'] - values['salary'] * (1 - 100/ (100 + values['vat'])) - values['smart_fee'] / 100 * (values['salary'] - values['salary'] * (1 - 100/ (100 + values['vat']))),
                    },
                ]
                
                expenses_lines = [
                    {
                        'name': 'Expenses',
                        'amount': values['expenses'],
                    }
                ]
                payslip = env['hr.payslip']
                salary_lines = payslip.sudo().simulate_payslip(env.uid, invoice_lines[4]['amount'] - values['expenses'], values)
                
                
                values['net'] = 0.0
                values['net_result'] = 0.0
                for line in salary_lines:
                    if line['code'] == 'NET':
                        values['net'] = float(line['quantity']) * line['amount'] * line['rate'] / 100
                        values['net_result'] = values['net'] + values['expenses']
                values['salary_lines'] = salary_lines
                values['invoice_lines'] = invoice_lines
                values['expenses_lines'] = expenses_lines
                return request.website.render("smart_salary_simulator_se.result_se", values)
            elif post.get('sender') == 'result':
                return request.website.render("smart_salary_simulator_se.simulator_form_se", values)
        else:
            if user.sudo().employee_ids and user.sudo().employee_ids[0].contract_ids:
                employee = user.employee_ids[0]
                contract = employee.sudo().contract_ids[0]
                values = {
                    'salary': (employee.company_id and employee.company_id.smart_cash) or contract.sudo().wage,
                    'yob': 1990,
                    'tax': 30.0,
                }
            else:
                employee = env.ref('smart_salary_simulator_se.dummy_employee')
                contract = env.ref('smart_salary_simulator_se.smart_contract_swe')
                values = {
                    'salary': contract.sudo().wage,
                    'yob': (employee.sudo().birthday and fields.Date.from_string(employee.sudo().birthday).year) or 1990,
                    'tax': 30.0,
                }
            values['salarysimulator_menu'] = 'active'
            values['expenses'] = 0
            values['vat'] = 25
            values['musician'] = 1
            values['smart_fee'] = 6.5
            values['res_user'] = user
            values['context'] = request.context
            return request.website.render("smart_salary_simulator_se.simulator_form_se", values)
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

    #~ @http.route(['/salary/simulator/get_lines'], type='json', auth="public", website=True)
    #~ def get_lines(self, contract_id=None, salary=1000.0, **post):
        #~ _logger.info(contract_id)
        #~ env = request.env
        #~ if not contract_id:
            #~ return [{'result':'<div class="foobargazonksvinollon">No contract found</div>'}]
        #~ contract = env['hr.contract'].browse(int(contract_id))[0]
        #~ wage = contract.wage or 0.0
        #~ contract.wage = float(salary)
        #~ payslip = env['hr.payslip'].create({
        #~ 'struct_id': contract.struct_id.id,
        #~ 'employee_id': contract.employee_id.id,
        #~ 'date_from': fields.Date.today(),
        #~ 'date_to': fields.Date.today(),
        #~ 'state': 'draft',
        #~ 'contract_id': contract.id,
        #~ })
        #~ lines = payslip.simulate_sheet()
        #~ payslip.unlink()
        #~ contract.wage = wage
        #~ 
        #~ lines_list = []
        #~ for line in lines:
            #~ lines_list.append([line['name'], float(line['quantity']) * line['amount'] * line['rate'] / 100])
        #~ 
        #~ return {'lines': lines_list}
    
    #~ @http.route(['/salary/sim/calc'], type='http', auth="user", website=True)
    #~ def salary_simulation_frame(self, order=False):
        #~ cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        #~ 
        #~ res_user = request.registry.get('res.users').browse(cr,uid,uid)
        #~ values = {}
        #~ 
        #~ return request.website.render("smart_salary_simulator.sim_frame_%s" %  pool.get('res.users').browse(cr, uid, uid).company_id.country_id.code.lower() , values)
#~ 
    #~ @http.route(['/salary/sim',
#~ #        '/salary/<int:user>'
    #~ ], type='http', auth="public", website=True)
    #~ def salary(self, user=0, search='', **post):
        #~ cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
#~ 
        #~ res_user = request.registry.get('res.users').browse(cr,uid,uid)
        #~ context['lang'] = res_user.lang
#~ 
        #~ values = {
            #~ 'salarysimulator_menu': 'active',        
            #~ 'context': context,
            #~ 'res_user': res_user,
        #~ }
        #~ return request.website.render("smart_salary_simulator.simulator_%s" %  pool.get('res.users').browse(cr, uid, uid).company_id.country_id.code.lower() , values)


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
