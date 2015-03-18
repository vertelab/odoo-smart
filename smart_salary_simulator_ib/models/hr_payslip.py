class smart_salary_simulator_payslip(model.TransientModel):
    _name = "smart_salary_simulator.payslip"
    _description = "Simulated payslip"
    _inherit = 'hr.payslip'

    def simulate_sheet(self, cr, uid, ids, employee, contract, context=None):
        
        self.create({
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
        
        
        slip_line_pool = self.pool.get('hr.payslip.line')
        sequence_obj = self.pool.get('ir.sequence')
        for payslip in self.browse(cr, uid, ids, context=context):
            #payslip.number = Reference (t.ex. SLIP/001)
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
            lines = [(0,0,line) for line in self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context)]
            #self.write(cr, uid, [payslip.id], {'line_ids': lines, 'number': number,}, context=context)
        return lines

"""
hr.payslip.get_payslip_lines returnerar en dict som besrkiver alla
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
"""
