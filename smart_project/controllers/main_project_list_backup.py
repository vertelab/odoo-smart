Original - returns: 



    @http.route(['/project/list'], type='http', auth="public", website=True)
    def project_list(self, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        domain = request.website.order_domain()

        res_user = request.registry.get('res.users').browse(cr,uid,uid)
        
        #return "|".join(str(c.name) for c in res_user.company_ids)
#        analytic_account_ids = request.registry.get('account.analytic.account').search(cr,uid,['company_id','in','[c.id for c in res_user.company_ids]'])
        analytic_account_ids = pool.get('account.analytic.account').search(cr,uid,['company_id','=',res_user.company_id.id])
        
        values = {
            'project_menu': 'active',
            'res_user': res_user,
            'projects': request.registry.get('project.project').browse(cr,uid,request.registry.get('project.project').search(cr,uid,['analytic_account_id','child_of',analytic_account_ids])),
        }
        return request.website.render("smart_project.list", values)       






Based on Client

Returns: 
"'NoneType' object has no attribute 'project_id'" while evaluating
'sale_order.project_id'



    @http.route(['/project/list',], type='http', auth="public", website=True)
    def project_list(self, project=0, search='', **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

#        domain = request.website.project_domain()

        keep = QueryURL('/project/', project=project and int(project), )

        project_obj = pool.get('res.user')

#        project_count = project_obj.search_count(cr, uid, domain, context=context)
#        client_ids = client_obj.search(cr, uid, domain, limit=10, context=context)
#        project_ids = project_obj.search(cr, uid, domain, context=context)
#        projects = project_obj.browse(cr, uid, client_ids, context=context)


        values = {
            'project_menu': 'active',
            'project': project,
#            'res_users': projects,
            'keep': keep,
        }
        return request.website.render("smart_project.list", values)
