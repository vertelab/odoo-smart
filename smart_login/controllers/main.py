# -*- coding: utf-8 -*-
import werkzeug


import openerp
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.web.controllers.main import ensure_db
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
import openerp.modules.registry

from openerp import SUPERUSER_ID
from openerp.addons.website.models.website import slug




import logging
_logger = logging.getLogger(__name__)


#def abort_and_redirect(url):
    #r = request.httprequest
    #response = werkzeug.utils.redirect(url, 303)
    #response = r.app.get_response(r, response, explicit_session=False)
    #werkzeug.exceptions.abort(response)

#def ensure_db(redirect='/web/database/selector'):
    ## This helper should be used in web client auth="none" routes
    ## if those routes needs a db to work with.
    ## If the heuristics does not find any database, then the users will be
    ## redirected to db selector or any url specified by `redirect` argument.
    ## If the db is taken out of a query parameter, it will be checked against
    ## `http.db_filter()` in order to ensure it's legit and thus avoid db
    ## forgering that could lead to xss attacks.
    #db = request.params.get('db')

    ## Ensure db is legit
    #if db and db not in http.db_filter([db]):
        #db = None

    #if db and not request.session.db:
        ## User asked a specific database on a new session.
        ## That mean the nodb router has been used to find the route
        ## Depending on installed module in the database, the rendering of the page
        ## may depend on data injected by the database route dispatcher.
        ## Thus, we redirect the user to the same page but with the session cookie set.
        ## This will force using the database route dispatcher...
        #r = request.httprequest
        #url_redirect = r.base_url
        #if r.query_string:
            ## Can't use werkzeug.wrappers.BaseRequest.url with encoded hashes:
            ## https://github.com/amigrave/werkzeug/commit/b4a62433f2f7678c234cdcac6247a869f90a7eb7
            #url_redirect += '?' + r.query_string
        #response = werkzeug.utils.redirect(url_redirect, 302)
        #request.session.db = db
        #abort_and_redirect(url_redirect)

    ## if db not provided, use the session one
    #if not db and request.session.db and http.db_filter([request.session.db]):
        #db = request.session.db

    ## if no database provided and no database in session, use monodb
    #if not db:
        #db = db_monodb(request.httprequest)

    ## if no db can be found til here, send to the database selector
    ## the database selector will redirect to database manager if needed
    #if not db:
        #werkzeug.exceptions.abort(werkzeug.utils.redirect(redirect, 303))

    ## always switch the session to the computed db
    #if db != request.session.db:
        #request.session.logout()
        #abort_and_redirect(request.httprequest.url)

    #request.session.db = db

#class smart_login(openerp.addons.web.controllers.main.Home):
class smart_login(http.Controller):



    @http.route('/', type='http', auth="none")
    def smart_index(self, s_action=None, db=None, **kw):
        return "Method %s Session UID %d uid %d" %(request.httprequest.method,request.session.uid,request.uid)

        ensure_db()
        return http.local_redirect('/smart/login', query=request.params, keep_hash=True)




    #@http.route('/smart', type='http', auth="none")
    #def smart_client(self, s_action=None, **kw):
        #ensure_db()
        #if request.session.uid:
            #if kw.get('redirect'):
                #return werkzeug.utils.redirect(kw.get('redirect'), 303)
            #if not request.uid:
                #request.uid = request.session.uid

            #menu_data = request.registry['ir.ui.menu'].load_menus(request.cr, request.uid, context=request.context)
            #return request.render('smart_login.webclient_bootstrap', qcontext={'menu_data': menu_data})
        #else:
            #url = '/smart/login?'
            #if request.debug:
                #url += 'debug&'
            #return """<html><head><script>
                #window.location = '%sredirect=' + encodeURIComponent(window.location);
            #</script></head></html>
            #""" % (url,)





    @http.route('/smart/login', type='http', auth="none")
    def smart_login(self, redirect=None, **kw):
        #return "Method %s Session UID %s uid %s" % (request.httprequest.method,request.session.uid,request.uid)

        ensure_db()
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)
            
        if request.httprequest.method == 'GET' and request.session.uid:
#        if request.httprequest.method == 'GET':
            return http.redirect_with_hash('/dashboard')

        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        if not redirect:
            redirect = '/dashboard?' + request.httprequest.query_string
        values['redirect'] = redirect

        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if uid is not False:
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
        return request.render('smart_login.login', values)




    @http.route('/smart/signup', type='http', auth='none', website=True)
    def smart_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                return super(AuthSignupHome, self).smart_login(*args, **kw)
            except (SignupError, AssertionError), e:
                qcontext['error'] = _(e.message)

        return request.render('smart_login.signup', qcontext)





    @http.route('/add_activity', type='http', auth='user', website=True)
    def smart_add_activity(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        _logger.warning("smart_login add_activity %s " % (self))
        res_user = pool.get('res.users').browse(cr,uid,uid,context)
        res_user.sudo().add_activity()
        res_user.sudo().add_hr_employee()
        res_user.sudo().webterms_accepted = True
        return werkzeug.utils.redirect('/dashboard')





    @http.route('/legal/webpolicy', type='http', auth='user', website=True)
    def webpolicy(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        
        values = {
            'context': context,
#            'res_user': res_user,
        }

        
        return request.website.render("smart_login.legal_%s" %  pool.get('res.users').browse(cr, uid, uid).company_id.country_id.code.lower() , values)

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
