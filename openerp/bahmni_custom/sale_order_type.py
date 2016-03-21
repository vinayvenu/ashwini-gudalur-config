import logging

from datetime import datetime, timedelta
from osv import fields, osv
from tools.translate import _
from openerp import tools
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import logging
_logger = logging.getLogger(__name__)


class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"

    def _get_product_context(self, cr, uid, shop_id,prodlot_id, context=None):
        shop_obj = self.pool.get('sale.shop')
        shop = shop_obj.browse(cr, uid, shop_id)
        prod_context = {}
        if(not shop):
            return {}
        if shop:
            location_id = shop.warehouse_id and shop.warehouse_id.lot_stock_id.id
            if location_id:
                prod_context['location'] = location_id
                prod_context['prodlot_id'] = prodlot_id
                prod_context['compute_child'] = False
        return prod_context

    def _get_prodlot_context(self, cr, uid, shop_id, context=None):
        shop_obj = self.pool.get('sale.shop')
        shop = shop_obj.browse(cr, uid, shop_id)
        prodlot_context = {}
        if(not shop):
            return {}
        if shop:
            location_id = shop.warehouse_id and shop.warehouse_id.lot_stock_id.id
            if location_id:
                prodlot_context['location_id'] = location_id
                prodlot_context['search_in_child'] = False
        return prodlot_context

    def is_qty_avail_against_batches(self, cr, uid, ids,shop_id, context=None):
        res = [];
        sale_order_line=self.pool.get("sale.order.line").search(cr,uid,[('order_id','=',ids[0])])
        if len(sale_order_line) > 0:
            for sol in sale_order_line:
                _logger.error("Sol=%s",sol)
                soltemp= self.pool.get("sale.order.line").browse(cr,uid,sol)
                template = self.get_prod_template(cr,uid,sol)
                stock_prod_lot = self.pool.get('stock.production.lot')
                prod_prod = self.pool.get('product.product')
                prodlot_context = self._get_prodlot_context(cr, uid,shop_id, context=context)
                if(template.type != 'service'):
                    _logger.error("Batch Id: %s",soltemp.batch_id)
                    if soltemp.batch_id and soltemp.batch_id.id>0:
                        prod_context = self._get_product_context(cr, uid,shop_id,soltemp.batch_id.id, context=context)
                        _logger.error("prod_context: %s",prod_context)
                        prodlot = stock_prod_lot.browse(cr, uid, soltemp.batch_id.id, context=prodlot_context)
                        product_id = []
                        _logger.error("soltemp.batch_id Id: %s",soltemp.batch_id)
                        _logger.error("prodlot.product_id Id: %s",prodlot.product_id)
                        product_id.append(prodlot.product_id.id)
                        _logger.error("Prod Id: %s",product_id)
                        actual_stock = prod_prod._get_actual_stock(cr, uid, product_id, '', [], prod_context)
                        _logger.error("Prod Stock: %s",actual_stock)
                        actual_qty = actual_stock[prodlot.product_id.id]
                        if(soltemp.product_uom_qty>actual_qty):
                            res.append({'error':'Quantity Not Available','item':soltemp.name, 'Available':actual_qty, 'Requested':soltemp.product_uom_qty})
                        sales_price = prodlot.sale_price
                        mrp = prodlot.mrp
                        tax_amount=0.0;
                        if sales_price and mrp:
                            for tax in soltemp.tax_id:
                                tax_amount = tax_amount + tax.amount
                            _logger.error("Taxes = %f",tax_amount);
                        sp_incl_tax = sales_price + tax_amount
                        if(sp_incl_tax>mrp):
                            res.append({'error':'Sales Price Including Tax more than MRP','item':soltemp.name, 'Sales With Tax':sp_incl_tax, 'MRP':mrp})
                    else:
                        #batch_id missing
                        res.append({'error':'No batch number provided','item':soltemp.name})
        return res;


    def action_button_confirm(self, cr, uid, ids, context=None):
        # assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        # wf_service = netsvc.LocalService('workflow')
        # wf_service.trg_validate(uid, 'sale.order', ids[0], 'order_confirm', cr)
        sale_order_temp=self.pool.get("sale.order").browse(cr,uid,ids[0])
        if(sale_order_temp.care_setting == 'opd'):
            multicat = self.is_a_multi_cat_so(cr, uid, ids,context)
            if multicat == True :
                raise osv.except_osv(
                    _('Error!'),
                    _('You cannot have items from different departments in same quotation.'))
        errors = self.is_qty_avail_against_batches(cr, uid, ids,sale_order_temp.shop_id.id,context)
        if(len(errors)>0):
            raise osv.except_osv(
                _('Error!'),
                _('Cannot procced with sale because of the following errors. %s')
                %(errors))
        return super(sale_order, self).action_button_confirm(cr, uid, ids, context)

    def is_a_multi_cat_so(self, cr, uid, ids, context=None):
        sale_order_line=self.pool.get("sale.order.line").search(cr,uid,[('order_id','=',ids[0])])
        if len(sale_order_line) == 1:
            return False;
        else:
            if len(sale_order_line) < 1:
                return False;
            else:
                commoncatlist=self.pool.get("product.category").search(cr,uid,[('name','=','Common')])
                commoncat = commoncatlist[0];
                _logger.error("common_cat===%s",commoncat)
                not_a_common_sol = self.get_not_a_common_sale_order_line(cr,uid,sale_order_line,commoncat)
                if not not_a_common_sol:
                    return False
                else:
                    catIds = self.get_array_of_category_ids(cr,uid,not_a_common_sol)
                    catIds.append(commoncat);
                    _logger.error("not_common_cat===%s",catIds)
                for sol in sale_order_line:
                        _logger.error("Sol=%s",sol)
                        template = self.get_prod_template(cr,uid,sol)
                        if template.categ_id.id not in catIds:
                            return True
            return False;


    def get_prod_template(self, cr,uid,sol):
        soltemp= self.pool.get("sale.order.line").browse(cr,uid,sol)
        product = self.pool.get("product.product").browse(cr,uid,soltemp.product_id.id)
        template = self.pool.get("product.template").browse(cr,uid,product.product_tmpl_id.id)
        return template;

    def get_not_a_common_sale_order_line(self, cr,uid,sale_order_lines,common_cat):
        # get the common's id
        for sol in sale_order_lines:
            template = self.get_prod_template(cr,uid,sol)
            if template.categ_id.id!=common_cat:
                return sol;



    def get_array_of_category_ids(self, cr,uid,sol):
        res=[]
        template = self.get_prod_template(cr,uid,sol)
        _logger.error("Template=%s",template)
        cr.execute("""select category_id from syncjob_department_category_mapping where department_name=
                      (select department_name from syncjob_department_category_mapping where category_id="""+str(template.categ_id.id)+")")
        rows = cr.fetchall()
        for row in rows:
            res.append(row[0])
        return res;

    _columns={
        'care_setting': fields.selection([('opd', 'OPD'),('ipd', 'IPD')], 'Care Setting',required='True'),
    }

sale_order()


class sale_order_line(osv.osv):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    def batch_id_change(self, cr, uid, ids, batch_id, product_id, context=None):
        if not product_id:
            return {}
        if not batch_id:
            prod_obj = self.pool.get('product.product').browse(cr, uid, product_id)
            return {'value': {'price_unit': prod_obj.list_price}}
        context = context or {}
        stock_prod_lot = self.pool.get('stock.production.lot')
        sale_price = 0.0
        life_date=None
        for prodlot in stock_prod_lot.browse(cr, uid, [batch_id], context=context):
            sale_price =  prodlot.sale_price
            life_date = prodlot.life_date and datetime.strptime(prodlot.life_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
            _logger.error("Life Date From DB= %s",life_date)
            _logger.error("Life Date From DB= %s",type(life_date))
            _logger.error("Life Date From DB= %s",life_date.strftime('%d/%m/%Y'))
            life_date = life_date.strftime('%d/%m/%Y') if (type(life_date) == datetime) else None
            _logger.error("Life Date = %s",life_date)
        return {'value' : {'price_unit': sale_price ,'expiry_date':life_date}}

sale_order_line()