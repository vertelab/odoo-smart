openerp.smart_salary_simulator = function(instance, local) {
    var _t = openerp.web._t,
        _lt = openerp.web._lt;
    var QWeb = openerp.web.qweb;

    local.SalaryCalculator = instance.Widget.extend({
        className: 'SalaryCalculator',
        start: function() {
            this.$el.append("<div>Calculate salary</div>");
        },
    });
    
    #instance.web.client_actions.add('salary.calculator', 'instance.smart_salary_simulator.SalaryCalculator');
}
