# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

import re

import logging
_logger = logging.getLogger(__name__)

                
class website_project(http.Controller):

    @http.route(['/project/list','/project/list/<string:search>'], type='http', auth="user", website=True)
    def project_list(self, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
                
        analytic_ids = pool.get('account.analytic.account').search(cr,uid,['|',('company_id','=',False),('company_id','=',res_user.company_id.id)])
        projects = pool.get('project.project').browse(cr,uid,pool.get('project.project').search(cr,uid,[('analytic_account_id','in',analytic_ids)],context=context),context=context)
        
        
        
        if search:
            projects = projects.filtered(lambda r: (
                    search in (r.name or '') 
                or  search in (r.state or '') 
                or  search in (r.analytic_account_id.partner_id.name or '') 
                or  search in (r.analytic_account_id.partner_id.email or '') 
                or  search in (r.analytic_account_id.partner_id.phone or '') 
                or  search in (r.analytic_account_id.partner_id.street or '') 
                or  search in (r.analytic_account_id.partner_id.country_id.name or '')
                ))
        _logger.info('Search %s %s' % (search,projects))
        
        values = {
            'context': context,
            'project_menu': 'active',
            'search': search,
            'res_user': res_user,
            'projects': projects,
        }
        return request.website.render("smart_project.list", values)       


    @http.route(['/project/list/all'], type='http', auth="user", website=True)
    def project_list_all(self, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
                
        analytic_ids = pool.get('account.analytic.account').search(cr,uid,['|',('company_id','=',False),('company_id','=',res_user.company_id.id)])                
        values = {
            'context': context,
            'project_all_menu': 'active',
            'res_user': res_user,
            'projects': pool.get('project.project').browse(cr,uid,pool.get('project.project').search(cr,uid,[]),context=context),
        }
        return request.website.render("smart_project.list_all", values)       



    @http.route(['/project/<model("project.project"):project>','/project/new','/project/<model("project.project"):project>/delete'], type='http', auth="user", website=True)
    def project(self, project=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        context['lang'] = res_user.lang

        _logger.warning("This is project post %s" % (post))

        if not project:
            project_id = pool.get('project.project').create(cr,uid,{
                'name': _('Your project name'),
            })
            project = pool.get('project.project').browse(cr,uid,project_id)

        else:
            if re.search("delete",request.httprequest.url) is not None:
                project.unlink()
                return werkzeug.utils.redirect('/project/list')
                
#        analytic_ids = pool.get('account.analytic.account').search(cr,uid,['|',('company_id','=',False),('company_id','=',res_user.company_id.id)])                
        values = {
            'context': context,
            'project_menu': 'active',
            'res_user': res_user,
            'project': project,
            'post': post,
            'form_post': '/project/%s?redirect=%s' % (project.id,post.get('redirect')),
        }

        if request.httprequest.method == 'POST':

            if post.get('name'):
                project.write({'name': post.get('name')})
                return werkzeug.utils.redirect('/project/list')
                                
# Create buttons in template for this
            if post.get('active'):
                project.write({'active': post.get('active')})

            values['project']= pool.get('project.project').browse(cr,uid,project.id)

## Return to the form
            if post.get('redirect'):
                return werkzeug.utils.redirect(post.get('redirect'))


        return request.website.render("smart_project.project", values)  

    @http.route(['/project/<model("project.project"):project>/overview',], type='http', auth="user", website=True)
    def project_overview(self, project=False, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        _logger.warning('Overview: %s' % project)

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang

#        order = pool.get('sale.order').browse(cr, uid, pool.get('sale.order').search(cr,uid,['&','&',('company_id','=',res_user.company_id.id),('state','in',('progress','manual','done')),('project_id','=',project.id)],context=context), context=context)
        order = pool.get('sale.order').browse(cr, uid, pool.get('sale.order').search(cr,uid,['&',('state','in',('draft','sent','open','manual','progress','done')),('project_id','=',project.id)],context=context), context=context)
        _logger.warning('Order: %s' % order)
        
        class BrowsableObject(object):
            def __init__(self,):
                self.dict = {}

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0

        order_sum = BrowsableObject()
        for o in order:
            order_sum.amount_untaxed      += o.amount_untaxed
            order_sum.amount_tax          += o.amount_tax
            order_sum.amount_total        += o.amount_total
            order_sum.amount_undiscounted += o.amount_undiscounted
            order_sum.planned_untaxed     += o.amount_untaxed if o.state in ('draft','sent','open','manual','progress','done') else 0.0
            order_sum.approved_untaxed    += o.amount_untaxed if o.state in ('open','manual','progress','done') else 0.0


        order_lines = pool.get('sale.order.line').browse(cr, uid, pool.get('sale.order.line').search(cr,uid,[('order_id','in',[o.id for o in order])],context=context), context=context)
        _logger.warning('Order_lines %s' % order_lines)
# sale.order.line

#		    <t t-if="o.order_id.state == 'draft'"><span class="draft">Draft </span></t>
#			<t t-if="o.order_id.state == 'sent'"><span class="sent">Sent to Client</span></t>
#			<t t-if="o.order_id.state == 'open'"><span class="sent">Open</span></t>
#   		<t t-if="o.order_id.state == 'manual'"><span class="approved">Submitted</span></t>
#   		<t t-if="o.order_id.state == 'progress'"><span class="invoiced">Invoiced</span></t>
#   		<t t-if="o.order_id.state == 'done'"><span class="paid">Paid</span></t>
#			<t t-if="o.order_id.state == 'cancel'"><span class="sent">Cancelled</span></t>		
 

 

        expense_line = pool.get('hr.expense.line').browse(cr, uid, pool.get('hr.expense.line').search(cr,uid,[('analytic_account','=',project.analytic_account_id.id)]))

# Select by project_id (analytic account)

        expense_sum = BrowsableObject()
        for e in expense_line:
            expense_sum.amount_untaxed  -= e.amount_untaxed
            expense_sum.amount_tax      -= e.amount_tax
            expense_sum.total_amount    -= e.total_amount
            expense_sum.planned_untaxed -= e.amount_untaxed if e.expense_id.state in ('draft','sent','confirm','accepted','done') else 0.0
            expense_sum.approved_untaxed-= e.amount_untaxed if e.expense_id.state in ('confirm','accepted','done') else 0.0
             
            
#draft','sent','open','manual'
        return request.website.render("smart_project.project_overview",{
            'context': context,
            'project_menu': 'active',
            'project': project,            
            'res_user': res_user,
            'sale_orders': order,
            'sale_order_lines': order_lines,
            'sale_orders_sum': order_sum,
            'expense_lines': expense_line,
            'expense_line_sum': expense_sum,
        }
        )
 

    @http.route(['/project/<model("project.project"):project>/cash',], type='http', auth="user", website=True)
    def project_cash(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang

        order_cash = pool.get('sale.order').browse(cr, uid, pool.get('sale.order').search(cr,uid,['&',('company_id','=',res_user.company_id.id),('state','in',('progress','manual','done'))],context=context), context=context)

        order_sum = 0.0
        for o in order_cash:
            order_sum += o.amount_untaxed

        expense_cash = pool.get('hr.expense.expense').browse(cr, uid, pool.get('hr.expense.expense').search(cr,uid,['&',('company_id','=',res_user.company_id.id),('state','in',('done','paid'))],context=context), context=context)

        expense_sum = 0.0
        for e in expense_cash:
#            expense_sum -= e.amount
            try:
                expense_sum -= e.amount_untaxed
            except Exception, ex:
                _logger.warning("Having trouble with e.amount_untaxed %s (%s) " % (ex,e))
                
        values = {
            'context': context,
            'cash_menu': 'active',            
            'res_user': res_user,
            'sale_orders': order_cash,
#            'sale_orders_sum': order_sum,
            'expenses': expense_cash,
#            'expenses_sum': expense_sum,
            'smart_share': res_user.company_id.smart_share,
#            'smarts_amount'   : order_sum * (res_user.company_id.smart_share / 100),
#            'activitys_amount': order_sum * (1 - (res_user.company_id.smart_share / 100)),
        }
        return request.website.render("smart_cash.list",values)
 
 
    @http.route(['/project/<model("project.project"):project>/budget',], type='http', auth="user", website=True)
    def project_budget(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang

        order_budget = pool.get('sale.order').browse(cr, uid, pool.get('sale.order').search(cr,uid,['&',('company_id','=',res_user.company_id.id),('state','in',('sent','waiting_date'))],context=context), context=context)


        order_sum = 0
        for o in order_budget:
#            order_sum += o.amount_total
            order_sum += o.amount_untaxed

        expense_budget = pool.get('hr.expense.expense').browse(cr, uid, pool.get('hr.expense.expense').search(cr,uid,['&',('company_id','=',res_user.company_id.id),('state','in',('accepted','confirm',))],context=context), context=context)

        expense_sum = 0
        for e in expense_budget:
            expense_sum -= e.amount 

        values = {
            'context': context,
            'budget_menu': 'active',            
            'res_user': res_user,
            'sale_orders': order_budget,
#           'sale_orders_sum': order_sum * (1 - (res_user.company_id.smart_share / 100)),
            'expenses': expense_budget,
#           'expenses_sum': expense_sum,
            'smart_share': res_user.company_id.smart_share,
#            'smarts_amount': order_sum * (res_user.company_id.smart_share / 100),
#            'activitys_amount': order_sum * (1 - (res_user.company_id.smart_share / 100)),
        }
        return request.website.render("smart_cash.list",values)



#Kanske kan detta vara till någon hjälp?
#https://code.launchpad.net/~camptocamp/oerpscenario/fix-property-assignment/+merge/153804
#I slutet på den här sidan finns det en kod som jag tror ligger i närheten av vad som går fel.





# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
