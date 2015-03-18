# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import logging

_logger = logging.getLogger(__name__)

class smart_salary_simulator_payslip(models.Model):
    _inherit = 'hr.payslip'
    
    def simulate_payslip(self, uid, salary, values):
        user = self.env['res.users'].browse(uid)[0]
        if user.employee_ids and user.employee_ids[0].contract_ids:
            employee = user.employee_ids[0]
            contract = employee.contract_ids[0]
        else:
            employee = self.env.ref('smart_salary_simulator_se.dummy_employee')
            contract = self.env.ref('smart_salary_simulator_se.smart_contract_swe')
        
        payslip = self.create({
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
                    'amount': salary,
                }),
                
                #~ (0, _, {
                    #~ 'name': 'Invoice VAT',
                    #~ 'code': 'VAT',
                    #~ 'contract_id': contract.id,
                    #~ 'amount': values['vat'],
                #~ }),
                #~ (0, _, {
                    #~ 'name': 'Smart Share',
                    #~ 'code': 'SMARTSHARE',
                    #~ 'contract_id': contract.id,
                    #~ 'amount': values['smart_fee'],
                #~ }),
                #~ (0, _, {
                    #~ 'name': 'Expenses',
                    #~ 'code': 'EXPENSES',
                    #~ 'contract_id': contract.id,
                    #~ 'amount': values['expenses'],
                #~ }),
                #~ (0, _, {
                    #~ 'name': 'Expenses VAT',
                    #~ 'code': 'EXPVAT',
                    #~ 'contract_id': contract.id,
                    #~ 'amount': values['expenses'],
                #~ }),
                (0, _, {
                    'name': 'Year of Birth',
                    'code': 'YOB',
                    'contract_id': contract.id,
                    'amount': values['yob'],
                }),
                (0, _, {
                    'name': 'Current Year',
                    'code': 'YEAR',
                    'contract_id': contract.id,
                    'amount': fields.Date.from_string(fields.Date.today()).year,
                }),
                (0, _, {
                    'name': 'Musician',
                    'code': 'MUSICIAN',
                    'contract_id': contract.id,
                    'amount': 1 if values['musician'] == 'on' else 0,
                }),
                (0, _, {
                    'name': 'Withholding Tax Rate',
                    'code': 'WT',
                    'contract_id': contract.id,
                    'amount': values['tax'],
                }),
                
                
                ]
        })
        
        result = payslip.simulate_sheet()
        
        payslip.unlink()
        
        return result
        
    def simulate_sheet(self):
        cr, uid, context = self.env.cr, self.env.uid, self.env.context
        ids = []
        for record in self:
            ids.append(record.id)
        slip_line_pool = self.pool.get('hr.payslip.line')
        sequence_obj = self.pool.get('ir.sequence')
        for payslip in self.browse(ids):
            number = payslip.number or sequence_obj.get(cr, uid, 'salary.slip')
            #delete old payslip lines
            old_slipline_ids = slip_line_pool.search(cr, uid, [('slip_id', '=', payslip.id)], context=context)
#            old_slipline_ids
            if old_slipline_ids:
                slip_line_pool.unlink(cr, uid, old_slipline_ids, context=context)
            if payslip.contract_id:
                #set the list of contract for which the rules have to be applied
                contract_ids = [payslip.contract_id.id]
            else:
                #if we don't give the contract, then the rules to apply should be for all current contracts of the employee
                contract_ids = self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to, context=context)
            lines = [line for line in self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context)]
            #self.write(cr, uid, [payslip.id], {'line_ids': lines, 'number': number,}, context=context)
        
        lines.sort(key=lambda line: line['sequence'])    
        return lines

"""
class smart_salary_simulator_payslip(models.TransientModel):
    _name = "smart_salary_simulator.payslip"
    _description = "Simulated payslip"
    _inherit = 'hr.payslip'

    def simulate_sheet(self):
        cr, uid, context = self.env.cr, self.env.uid, self.env.context
        #ids = []
        #for record in self:
        #    ids.append(record.id)
        slip_line_pool = self.env['hr.payslip.line']
        sequence_obj = self.env['ir.sequence']
        for payslip in self:
            #payslip.number = Reference (t.ex. SLIP/001)
            number = payslip.number or sequence_obj.get('salary.slip')
            #delete old payslip lines
            old_sliplines = slip_line_pool.search([('slip_id', '=', payslip.id)])
#            old_slipline_ids
            for record in old_sliplines:
                slip_line_pool.unlink(cr, uid, [record.id], context=context)
            if payslip.contract_id:
                #set the list of contract for which the rules have to be applied
                contract_ids = [payslip.contract_id.id]
            else:
                #if we don't give the contract, then the rules to apply should be for all current contracts of the employee
                contract_ids = self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
            lines = [(0,0,line) for line in payslip.get_payslip_lines_sim(contract_ids)]
            #self.write(cr, uid, [payslip.id], {'line_ids': lines, 'number': number,}, context=context)
        return lines
        
    @api.one
    def get_payslip_lines_sim(self, contract_ids):
        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            localdict['categories'].dict[category.code] = category.code in localdict['categories'].dict and localdict['categories'].dict[category.code] + amount or amount
            return localdict

        class BrowsableObject(object):
            def __init__(self, pool, cr, uid, employee_id, dict):
                self.pool = pool
                self.cr = cr
                self.uid = uid
                self.employee_id = employee_id
                self.dict = dict

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0

        class InputLine(BrowsableObject):
"""            """a class that will be used into the python code, mainly for usability purposes"""
"""            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                result = 0.0
                self.cr.execute("SELECT sum(amount) as sum\
                            FROM smart_salary_simulator_payslip as hp, hr_payslip_input as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
                           (self.employee_id, from_date, to_date, code))
                res = self.cr.fetchone()[0]
                return res or 0.0

        class WorkedDays(BrowsableObject):
"""            """a class that will be used into the python code, mainly for usability purposes"""
"""            def _sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                result = 0.0
                self.cr.execute("SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours\
                            FROM smart_salary_simulator_payslip as hp, hr_payslip_worked_days as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done'\
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
                           (self.employee_id, from_date, to_date, code))
                return self.cr.fetchone()

            def sum(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[0] or 0.0

            def sum_hours(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[1] or 0.0

        class Payslips(BrowsableObject):
"""            """a class that will be used into the python code, mainly for usability purposes"""
"""
            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
                            FROM smart_salary_simulator_payslip as hp, hr_payslip_line as pl \
                            WHERE hp.employee_id = %s AND hp.state = 'done' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s",
                            (self.employee_id, from_date, to_date, code))
                res = self.cr.fetchone()
                return res and res[0] or 0.0

        #we keep a dict with the result because a value can be overwritten by another rule with the same code
        result_dict = {}
        rules = {}
        categories_dict = {}
        blacklist = []
        #inputs_obj = self.pool.get('hr.payslip.worked_days')
        worked_days = {}
        for worked_days_line in self.worked_days_line_ids:
            worked_days[worked_days_line.code] = worked_days_line
        inputs = {}
        for input_line in self.input_line_ids:
            inputs[input_line.code] = input_line

        categories_obj = BrowsableObject(self.pool, cr, uid, self.employee_id.id, categories_dict)
        input_obj = InputLine(self.pool, cr, uid, self.employee_id.id, inputs)
        worked_days_obj = WorkedDays(self.pool, cr, uid, self.employee_id.id, worked_days)
        payslip_obj = Payslips(self.pool, cr, uid, self.employee_id.id, self)
        rules_obj = BrowsableObject(self.pool, cr, uid, self.employee_id.id, rules)

        baselocaldict = {'categories': categories_obj, 'rules': rules_obj, 'payslip': payslip_obj, 'worked_days': worked_days_obj, 'inputs': input_obj}
        #get the ids of the structures on the contracts and their parent id as well
        structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)
        #get the rules of the structure and thier children
        rule_ids = self.pool.get('hr.payroll.structure').get_all_rules(cr, uid, structure_ids, context=context)
        #run the rules by sequence
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]

        obj_rule = self.env['hr.salary.rule'].search(, sorted='sequence')
        
        for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
            employee = contract.employee_id
            localdict = dict(baselocaldict, employee=employee, contract=contract)
            for rule in obj_rule:
                key = rule.code + '-' + str(contract.id)
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                localdict['result_rate'] = 100
                #check if the rule can be applied
                if obj_rule.satisfy_condition(cr, uid, rule.id, localdict, context=context) and rule.id not in blacklist:
                    #compute the amount of the rule
                    amount, qty, rate = obj_rule.compute_rule(cr, uid, rule.id, localdict, context=context)
                    #check if there is already a rule computed with that code
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    #set/overwrite the amount computed for this rule in the localdict
                    tot_rule = amount * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    rules[rule.code] = rule
                    #sum the amount for its salary category
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    #create/overwrite the rule in the temporary results
                    result_dict[key] = {
                        'salary_rule_id': rule.id,
                        'contract_id': contract.id,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        'condition_select': rule.condition_select,
                        'condition_python': rule.condition_python,
                        'condition_range': rule.condition_range,
                        'condition_range_min': rule.condition_range_min,
                        'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        'amount_python_compute': rule.amount_python_compute,
                        'amount_percentage': rule.amount_percentage,
                        'amount_percentage_base': rule.amount_percentage_base,
                        'register_id': rule.register_id.id,
                        'amount': amount,
                        'employee_id': contract.employee_id.id,
                        'quantity': qty,
                        'rate': rate,
                    }
                else:
                    #blacklist this rule and its children
                    blacklist += [id for id, seq in self.pool.get('hr.salary.rule')._recursive_search_of_rules(cr, uid, [rule], context=context)]

        result = [value for code, value in result_dict.items()]
        return result

"""
"""
hr.payslip.get_payslip_lines returnerar en dict som beskriver alla
hr.payslip.lines som ska genereras:

result_dict[key] = {
                        'salary_rule_id': rule.id,
                        'contract_id': contract.id,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        'condition_select': rule.condition_select,
                        'condition_python': rule.condition_python,
                        'condition_range': rule.condition_range,
                        'condition_range_min': rule.condition_range_min,
                        'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        'amount_python_compute': rule.amount_python_compute,
                        'amount_percentage': rule.amount_percentage,
                        'amount_percentage_base': rule.amount_percentage_base,
                        'register_id': rule.register_id.id,
                        'amount': amount,
                        'employee_id': contract.employee_id.id,
                        'quantity': qty,
                        'rate': rate,
                    }



key = rule.code + '-' + str(contract.id)

'struct_id': fields.many2one('hr.payroll.structure', 'Structure', readonly=True, states={'draft': [('readonly', False)]}, help='Defines the rules that have to be applied to this payslip, accordingly to the contract chosen. If you let empty the field contract, this field isn\'t mandatory anymore and thus the rules applied will be all the rules set on the structure of all contracts of the employee valid for the chosen period'),
        'name': fields.char('Payslip Name', required=False, readonly=True, states={'draft': [('readonly', False)]}),
        'number': fields.char('Reference', required=False, readonly=True, states={'draft': [('readonly', False)]}, copy=False),
        'employee_id': fields.many2one('hr.employee', 'Employee', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'date_from': fields.date('Date From', readonly=True, states={'draft': [('readonly', False)]}, required=True),
        'date_to': fields.date('Date To', readonly=True, states={'draft': [('readonly', False)]}, required=True),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('verify', 'Waiting'),
            ('done', 'Done'),
            ('cancel', 'Rejected'),
        ], 'Status', select=True, readonly=True, copy=False,
            help='* When the payslip is created the status is \'Draft\'.\
            \n* If the payslip is under verification, the status is \'Waiting\'. \
            \n* If the payslip is confirmed then status is set to \'Done\'.\
            \n* When user cancel payslip the status is \'Rejected\'.'),
        'line_ids': one2many_mod2('hr.payslip.line', 'slip_id', 'Payslip Lines', readonly=True, states={'draft':[('readonly',False)]}),
        'company_id': fields.many2one('res.company', 'Company', required=False, readonly=True, states={'draft': [('readonly', False)]}, copy=False),
        'worked_days_line_ids': fields.one2many('hr.payslip.worked_days', 'payslip_id', 'Payslip Worked Days', required=False, readonly=True, states={'draft': [('readonly', False)]}),
        'input_line_ids': fields.one2many('hr.payslip.input', 'payslip_id', 'Payslip Inputs', required=False, readonly=True, states={'draft': [('readonly', False)]}),
        'paid': fields.boolean('Made Payment Order ? ', required=False, readonly=True, states={'draft': [('readonly', False)]}, copy=False),
        'note': fields.text('Internal Note', readonly=True, states={'draft':[('readonly',False)]}),
        'contract_id': fields.many2one('hr.contract', 'Contract', required=False, readonly=True, states={'draft': [('readonly', False)]}),
        'details_by_salary_rule_category': fields.function(_get_lines_salary_rule_category, method=True, type='one2many', relation='hr.payslip.line', string='Details by Salary Rule Category'),
        'credit_note': fields.boolean('Credit Note', help="Indicates this payslip has a refund of another", readonly=True, states={'draft': [('readonly', False)]}),
        'payslip_run_id': fields.many2one('hr.payslip.run', 'Payslip Batches', readonly=True, states={'draft': [('readonly', False)]}, copy=False),
        'payslip_count': fields.function(_count_detail_payslip, type='integer', string="Payslip Computation Details"),


"""
