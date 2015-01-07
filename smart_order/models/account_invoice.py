# -*- coding: utf-8 -*-
import random

from openerp import SUPERUSER_ID
from openerp.osv import osv, orm, fields
from openerp.addons.web.http import request



class account_invoice(osv.Model):
    _inherit = "account.invoice"

    def _get_errors(self, cr, uid, order, context=None):
        return []

    def _get_website_data(self, cr, uid, order, context):
        return {
            'partner': order.partner_id.id,
            'order': order
        }

    def _find_order_line(self, cr, uid, ids, product_id=None, line_id=None, context=None, **kwargs):
        for so in self.browse(cr, uid, ids, context=context):
            domain = [('order_id', '=', so.id), ('product_id', '=', product_id)]
            if line_id:
                domain += [('id', '=', line_id)]
            return self.pool.get('sale.order.line').search(cr, SUPERUSER_ID, domain, context=context)


class website(orm.Model):
    _inherit = 'website'

    _columns = {
        'pricelist_id': fields.related('user_id','partner_id','property_product_pricelist',
            type='many2one', relation='product.pricelist', string='Default Pricelist'),
        'currency_id': fields.related('pricelist_id','currency_id',
            type='many2one', relation='res.currency', string='Default Currency'),
    }

    def order_domain(self, cr, uid, ids, context=None):
        return [("company_id", "=", 1)]

    def order_get_order(self, cr, uid, ids, force_create=False, code=None, update_pricelist=None, context=None):
        sale_order_obj = self.pool['account_invoice']
        sale_order_id = request.session.get('account_invoice_id')
        sale_order = None
        # create so if needed
        if not sale_order_id and (force_create or code):  
            # TODO cache partner_id session
            partner = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id

            for w in self.browse(cr, uid, ids):
                values = {
                    'user_id': w.user_id.id,
                    'partner_id': partner.id,
                    'pricelist_id': partner.property_product_pricelist.id,
                    'section_id': self.pool.get('ir.model.data').get_object_reference(cr, uid, 'website', 'salesteam_website_sales')[1],
                }
                sale_order_id = sale_order_obj.create(cr, SUPERUSER_ID, values, context=context)
                values = sale_order_obj.onchange_partner_id(cr, SUPERUSER_ID, [], partner.id, context=context)['value']
                sale_order_obj.write(cr, SUPERUSER_ID, [sale_order_id], values, context=context)
                request.session['account_invoice_id'] = sale_order_id
        if sale_order_id:
            # TODO cache partner_id session
            partner = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id

            sale_order = sale_order_obj.browse(cr, SUPERUSER_ID, sale_order_id, context=context)
            if not sale_order.exists():
                request.session['account_invoice_id'] = None
                return None

            # check for change of pricelist with a coupon
            if code and code != sale_order.pricelist_id.code:
                pricelist_ids = self.pool['product.pricelist'].search(cr, SUPERUSER_ID, [('code', '=', code)], context=context)
                if pricelist_ids:
                    pricelist_id = pricelist_ids[0]
                    request.session['sale_order_code_pricelist_id'] = pricelist_id
                    update_pricelist = True
                request.session['sale_order_code_pricelist_id'] = False

            pricelist_id = request.session.get('sale_order_code_pricelist_id') or partner.property_product_pricelist.id

            # check for change of partner_id ie after signup
            if sale_order.partner_id.id != partner.id and request.website.partner_id.id != partner.id:
                flag_pricelist = False
                if pricelist_id != sale_order.pricelist_id.id:
                    flag_pricelist = True
                fiscal_position = sale_order.fiscal_position and sale_order.fiscal_position.id or False

                values = sale_order_obj.onchange_partner_id(cr, SUPERUSER_ID, [sale_order_id], partner.id, context=context)['value']
                if values.get('fiscal_position'):
                    order_lines = map(int,sale_order.order_line)
                    values.update(sale_order_obj.onchange_fiscal_position(cr, SUPERUSER_ID, [],
                        values['fiscal_position'], [[6, 0, order_lines]], context=context)['value'])

                values['partner_id'] = partner.id
                sale_order_obj.write(cr, SUPERUSER_ID, [sale_order_id], values, context=context)

                if flag_pricelist or values.get('fiscal_position') != fiscal_position:
                    update_pricelist = True

            # update the pricelist
            if update_pricelist:
                values = {'pricelist_id': pricelist_id}
                values.update(sale_order.onchange_pricelist_id(pricelist_id, None)['value'])
                sale_order.write(values)
                for line in sale_order.order_line:
                    sale_order._cart_update(product_id=line.product_id.id, add_qty=0)

            # update browse record
            if (code and code != sale_order.pricelist_id.code) or sale_order.partner_id.id !=  partner.id:
                sale_order = sale_order_obj.browse(cr, SUPERUSER_ID, sale_order.id, context=context)

        return sale_order

    def sale_reset(self, cr, uid, ids, context=None):
        request.session.update({
            'account_invoice_id': False,
            'sale_transaction_id': False,
            'sale_order_code_pricelist_id': False,
        })


