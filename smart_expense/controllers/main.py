# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

import re

from openerp.osv import fields


import logging
_logger = logging.getLogger(__name__)

        
class website_expense(http.Controller):

    @http.route(['/expense/list','/expense'], type='http', auth="user", website=True)
    def expense_list(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
        
        values = {
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_expense.list",values)


    @http.route(['/expense/list/all'], type='http', auth="user", website=True)
    def expense_list_all(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
        
        values = {
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[]),context=context),
        }
        return request.website.render("smart_expense.list",values)


    @http.route(['/expense/<model("hr.expense.expense"):expense>','/expense/new',
    '/expense/<model("hr.expense.expense"):expense>/cancel',
    '/expense/<model("hr.expense.expense"):expense>/line/<model("hr.expense.line"):expense_line>/delete',
#    '/expense/new/category/<model("product.template"):category>',
#Fredriks försök att lägga till en url för att redigera en expense-line
    '/expense/<model("hr.expense.expense"):expense>/line/<model("hr.expense.line"):expense_line>/category/<model("product.product"):category>',
#slut
    '/expense/<model("hr.expense.expense"):expense>/category/<model("product.product"):category>',
    '/expense/<model("hr.expense.expense"):expense>/category/list',
    ], type='http', auth="user", website=True)
    def expense(self, expense=False,category=False,template=False,expense_line=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        context['lang'] = res_user.lang

        if not expense:
            context['form_action'] = '/expense/new'
        else:
            context['form_action'] = '/expense/%s' % expense.id 
            
        if expense and re.search("cancel",request.httprequest.url) is not None:
            expense.unlink()
            return werkzeug.utils.redirect('/expense/list')

        analytic_ids = pool.get('account.analytic.account').search(cr,uid,['|',('company_id','=',False),('company_id','=',res_user.company_id.id)])                


        values = {
            'product': category,
            'expense_line': expense_line,
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expense': expense,
            'form_action': context['form_action'],
            'context': context,
#Fredriks försök att fixa supplier-listan
             'supplier': request.env['res.partner'].search([('supplier','=',True)]),
#            'clients_global':  request.registry['res.partner'].browse(cr,uid,request.registry['res.partner'].search(cr,uid,[('company_id','=',False)],context=context),context=context),
#            'clients_local':  request.registry['res.partner'].browse(cr,uid,request.registry['res.partner'].search(cr,uid,[('company_id','=',res_user.company_id.id)],context=context),context=context),
            'recipients':  pool.get('res.users').browse(cr,uid,pool.get('res.users').search(cr,uid,[],context=context),context=context),
            'products': pool.get('product.template').browse(cr,uid,pool.get('product.template').search(cr,uid,['&',('hr_expense_ok','=',True),('default_code','>','')],context=context),context=context),
            'projects': pool.get('project.project').browse(cr,uid,pool.get('project.project').search(cr,uid,[('analytic_account_id','in',analytic_ids)],context=context),context=context),
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
#            'cat_travel': False,
            'cat_travel': self.expense_get_category('Travel'),
            'cat_office': self.expense_get_category('Office Supplies'),
            'cat_meal':self.expense_get_category('Meal and Hotel'),
            'cat_personal':self.expense_get_category('Personal Material'),
            'cat_rent':self.expense_get_category('Rent'),
            'cat_fixed':self.expense_get_category('Fixed'),
            'cat_other':self.expense_get_category('Other Expenses'),
        }

        if request.httprequest.method == 'POST':
            _logger.warning("This is expense post %s " % (post))

            if post.get('delete') == True:
                expense.unlink()
                return werkzeug.utils.redirect('/expense/')
#                return werkzeug.utils.redirect('/expense/list')

# Expense Workflow Submit button = cancel (or others)
            for signal in [transition.signal for transition in request.registry['workflow.transition'].browse(cr,uid,request.registry['workflow.transition'].search(cr,uid,[('signal','>','')])) if post.get(transition.signal)]:
                try:
                    request.session.exec_workflow('hr.expense.expense', expense.id, signal)
                except Exception, ex: 
                    values['error'] = "Error: %s" % ex
                return werkzeug.utils.redirect('/expense/list')

# Expense data
            expense_data = dict((field_name.replace('hr_',''), post[field_name])
                for field_name in ['amount','date','date_confirm','date_valid','department_id','employee_id','journal_id','name','note','state','user_id','user_valid',] if post.get(field_name))
            if expense and expense_data:
                expense.write(expense_data)
            elif expense_data:
                expense = pool.get('hr.expense.expense').create(cr,uid,expense_data)
                values['form_action'] = '/expense/%s' % expense  # Id
                values['expense'] = pool.get('hr.expense.expense').browse(cr,uid,expense)
                
                                
            if not expense:
                values['error'] = _('Something went wrong with the form (no expense)')
#                return request.website.render('smart_expense.overview', values)
                return request.website.render('smart_expense.list', values)

## Expense Lines
            expense_line = dict((field_name.replace('line_',''), post[field_name])
                for field_name in [
                'line_analytic_account',
                'line_date_value',
#                'line_description',
                'line_distance',
                'line_starting_point',
                'line_justification',
                'line_name',
                'line_product_id',
                'line_ref',
                'line_sequence',
                'line_to',
                'line_unit_amount',
                'line_unit_amount_untaxed',
                'line_unit_quantity',
                'line_uom_id',
                ] if post.get(field_name))
            if expense and post.get('new_line'): # Submit button named new_line
                expense_line['expense_id'] = expense.id
                #if not expense_line.get('user_id',False): 
                    #expense_line['user_id'] = res_user.id                
                #if not expense_line.get('employee_id',False): 
                    #expense_line['employee_id'] = res_user.employee_ids[0].id                
                #if not expense_line.get('company_id',False): 
                    #expense_line['company_id'] = res_user.company_id.id                
                #if not expense_line.get('currency_id',False): 
                    #expense_line['currency_id'] = res_user.company_id.currency_id.id
                if not expense_line.get('name',False): 
                    expense_line['name'] = " "
                if not expense_line.get('unit_quantity',False): 
                    expense_line['unit_quantity'] = 1.0
                if expense_line.get('product_id',False): 
                    expense_line['product_id'] = int(expense_line['product_id'])
#                self.env['hr.expense.line'].create(expense_line)
                pool.get('hr.expense.line').create(cr,uid,expense_line)
                
            elif expense:
                for line in post.keys():
                    if line.startswith('line_id_'):
                        r = re.match("line_id_(\d+)",line)
                        row = str(r.groups(1)[0])
                        expense_line = pool.get('hr.expense.line').browse(cr,uid,int(post.get('line_id_' + row)),context=context)
                        expense_line_data = dict((field_name.replace('line_','').replace('_%s' % int(post.get('line_id_' + row)),''), post[field_name])
                            for field_name in [
                            'line_analytic_account_%s' % int(post.get('line_id_' + row)),
                            'line_date_value_%s' % int(post.get('line_id_' + row)),
#                            'line_description_%s' % int(post.get('line_id_' + row)),
                            'line_distance_%s' % int(post.get('line_id_' + row)),
                            'line_starting_point_%s' % int(post.get('line_id_' + row)),
                            'line_justification_%s' % int(post.get('line_id_' + row)),
                            'line_name_%s' % int(post.get('line_id_' + row)),
                            'line_product_id_%s' % int(post.get('line_id_' + row)),
                            'line_ref_%s' % int(post.get('line_id_' + row)),
                            'line_sequence_%s' % int(post.get('line_id_' + row)),
                            'line_to_%s' % int(post.get('line_id_' + row)),
                            'line_unit_amount_%s' % int(post.get('line_id_' + row)),
                            'line_unit_amount_untaxed_%s' % int(post.get('line_id_' + row)),
                            'line_unit_quantity_%s' % int(post.get('line_id_' + row)),
                            'line_uom_id_%s' % int(post.get('line_id_' + row)),
                            'line_analytic_account',
                            'line_date_value',
            #                'line_description',
                            'line_distance',
                            'line_starting_point',
                            'line_justification',
                            'line_name',
                            'line_product_id',
                            'line_ref',
                            'line_sequence',
                            'line_to',
                            'line_unit_amount',
                            'line_unit_amount_untaxed',
                            'line_unit_quantity',
                            'line_uom_id',
                            ] if post.get(field_name))
                        expense_line.write(expense_line_data)


## Return to the form
            if post.get('redirect'):
                return werkzeug.utils.redirect(post.get('redirect'))
            else:
                if post.get('save_and_add_expense_line'):
                    return request.website.render('smart_expense.category_list', values)
                else:
                    return request.website.render('smart_expense.overview', values)

        else:  # Not POST
            
            if category and category.expense_template_id: 
                _logger.warning("Choose template %s %s" % (category.name,category.expense_template_id.xml_id))
                return request.website.render('%s' % category.expense_template_id.xml_id, values)
            if category: 
                return request.website.render('smart_expense.expense_receipt', values)
            if re.search("category/list",request.httprequest.url) is not None:
                return request.website.render('smart_expense.category_list', values)
            if expense_line and re.search("delete",request.httprequest.url) is not None:
                expense_line.unlink()
            if not expense:
                #return werkzeug.utils.redirect('http://google.se')
                return request.website.render('smart_expense.overview', values)

            return request.website.render('smart_expense.overview', values)


## Expense States

#draft + confirm = confirm
#confirm + refuse = refused
#confirm + validate = accepted
#confirm + draft = draft            
#accepted + done = done
#accepted + refuse = refused
#refused + draft = draft






    def expense_get_category(self,category):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry 
#        product_category = pool.get('product.template').get_object_reference(cr, uid, 'product', category)[1]
        try:
            categ_id = pool.get('product.category').search(cr,uid,[('name','=',category)],context=context)[0]
        except Exception, e:
            _logger.exception("No category %s (%s)" % (category,e))
            categ_id = 1
        return pool.get('product.product').browse(cr,uid,pool.get('product.product').search(cr,uid,['&',('hr_expense_ok','=',True),('categ_id','=',categ_id)],context=context),context=context)


## Expense Overview

    @http.route(['/expense/overview'], type='http', auth="user", website=True)
    def expense_overview(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
        
        values = {
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_expense.overview",values)


#Fredriks tillägg


## Expense Category

    @http.route(['/expense/line/category'], type='http', auth="user", website=True)
    def expense_categrory(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
        
        values = {
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_expense.category_list",values)


    @http.route(['/expense/line/car'], type='http', auth="user", website=True)
    def expense_line_car(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
        
        values = {
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_expense.expense_line_car",values)

    @http.route(['/expense/line/public/transport'], type='http', auth="user", website=True)
    def expense_line_public_transport(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
        
        values = {
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_expense.expense_line_public_transport",values)

    @http.route(['/expense/line/receipt'], type='http', auth="user", website=True)
    def expense_line_receipt(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
        
        values = {
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
        }
        return request.website.render("smart_expense.expense_receipt",values)


    @http.route(['/expense/line/invoice'], type='http', auth="user", website=True)
    def expense_line_invoice(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
        
        values = {
            'context': context,
            'expense_menu': 'active',
            'res_user': res_user,
            'expenses': request.registry.get('hr.expense.expense').browse(cr,uid,request.registry.get('hr.expense.expense').search(cr,uid,[('company_id','=',res_user.company_id.id)]),context=context),
            'clients_global':  request.registry['res.partner'].browse(cr,uid,request.registry['res.partner'].search(cr,uid,[('company_id','=',False)],context=context),context=context),
            'clients_local':  request.registry['res.partner'].browse(cr,uid,request.registry['res.partner'].search(cr,uid,[('company_id','=',res_user.company_id.id)],context=context),context=context),

        }
        return request.website.render("smart_expense.expense_invoice",values)




# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
