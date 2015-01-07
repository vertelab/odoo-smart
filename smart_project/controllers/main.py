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

    @http.route(['/project/list'], type='http', auth="user", website=True)
    def project_list(self, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        context['lang'] = res_user.lang
                
        analytic_ids = pool.get('account.analytic.account').search(cr,uid,['|',('company_id','=',False),('company_id','=',res_user.company_id.id)])                
        values = {
            'context': context,
            'project_menu': 'active',
            'res_user': res_user,
            'projects': pool.get('project.project').browse(cr,uid,pool.get('project.project').search(cr,uid,[('analytic_account_id','in',analytic_ids)],context=context),context=context),
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
            'form_post': '/project/%s' % project.id,
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

       

#Kanske kan detta vara till någon hjälp?
#https://code.launchpad.net/~camptocamp/oerpscenario/fix-property-assignment/+merge/153804
#I slutet på den här sidan finns det en kod som jag tror ligger i närheten av vad som går fel.





# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
