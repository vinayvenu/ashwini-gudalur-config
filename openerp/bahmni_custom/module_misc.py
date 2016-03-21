from __future__ import division
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    _order = "id"
    _columns={
        'tin_number':fields.char(string='TIN'),
    }
res_partner()

class stock_move_split_lines_exten(osv.osv_memory):
    _name = "stock.move.split.lines"
    _description = "Stock move Split lines"
    _inherit = "stock.move.split.lines"

    def _get_product_mrp(self, cr, uid, context=None):
        context = context or {}
        tax_amount = 0
        stock_move_id = context.get('stock_move', None)
        stock_move = stock_move_id and self.pool.get('stock.move').browse(cr, uid, stock_move_id, context=context)
        return (stock_move and stock_move.purchase_line_id and stock_move.purchase_line_id.mrp) or 0.0

    def onchange_cost_price(self, cr, uid, ids, cost_price, context=None):
        cost_price = cost_price or 0.0
        product_uom = self._get_product_uom(cr, uid, context=context)
        mrp = self._get_product_mrp(cr, uid, context=context)
        return {'value': {'sale_price': self._calculate_sale_price(cost_price, product_uom,mrp)}}

    def _calculate_sale_price(self, cost_price, product_uom, mrp):
        cost_price = cost_price or 0.0
        product_uom_factor = product_uom.factor if(product_uom is not None) else 1.0
        cost_price_per_unit = cost_price * product_uom_factor
        margin_percent = 200.0
        sp_incl_tax = cost_price + (cost_price * 2)
        #Assuming 5% tax
        if(sp_incl_tax>mrp):
            sp_incl_tax = mrp;
        actual_sp = sp_incl_tax/1.05;
            #remove the rounding...
        actual_sp = actual_sp - 0.01;
        return actual_sp

    def _calculate_default_sale_price(self, cr, uid, context=None):
        cost_price = self._get_default_cost_price(cr, uid, context=context) or 0.0
        product_uom = self._get_product_uom(cr, uid, context=context)
        mrp = self._get_product_mrp(cr, uid, context=context)
        return self._calculate_sale_price(cost_price, product_uom,mrp)

    _columns = {
        'name': fields.char('Batch Number', size=64),
        'prodlot_id': fields.many2one('stock.production.lot', 'Batch Number'),
        }
    _defaults = {
        'mrp': _get_product_mrp,
        'sale_price': _calculate_default_sale_price
    }

stock_move_split_lines_exten()


class split_in_production_lot_with_price_exten(osv.osv_memory):
    _name = "stock.move.split"
    _inherit = "stock.move.split"
    _description = "Split in Batch Numbers"

    def split(self, cr, uid, ids, move_ids, context=None):
        """ To split stock moves into serial numbers
        :param move_ids: the ID or list of IDs of stock move we want to split
        """
        if context is None:
            context = {}
        assert context.get('active_model') == 'stock.move', \
            'Incorrect use of the stock move split wizard'
        move_obj = self.pool.get('stock.move')
        for data in self.browse(cr, uid, ids, context=context):
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                move_qty = move.product_qty
                quantity_rest = move.product_qty
                uos_qty_rest = move.product_uos_qty
                new_move = []
                if data.use_exist:
                    lines = [l for l in data.line_exist_ids if l]
                else:
                    lines = [l for l in data.line_ids if l]
                total_move_qty = 0.0
                for line in lines:
                    sp_with_tax = line.sale_price +(0.05*line.sale_price)
                    if sp_with_tax>line.mrp :
                        raise osv.except_osv(_('Processing Error!'), _('Batch number %s of %s has : Sales Price + Tax more that mrp :(%f+5%%) %f > %f)!') \
                                             % (line.name, move.product_id.name, line.sale_price, sp_with_tax, line.mrp))
        return super(split_in_production_lot_with_price_exten, self).split(cr, uid, ids, move_ids, context)
split_in_production_lot_with_price_exten()


class stock_production_lot(osv.osv):

    _name = 'stock.production.lot'
    _inherit = 'stock.production.lot'

    def write(self, cr, uid, ids, values, context=None):
        _logger.error("Values 1n = %s",values)
        sales_price = values.get('sale_price')
        mrp = values.get('mrp')
        if sales_price and mrp:
            sp_incl_tax = sales_price + (sales_price * .05)
            #Assuming 5% tax
            if(sp_incl_tax>mrp):
                raise osv.except_osv(_('Processing Error!'), _('Batch number has : Sales Price + Tax more that mrp :(%f+5%%) %f > %f)!') \
                                     % (sales_price, sp_incl_tax, mrp))
        return super(stock_production_lot, self).write(cr, uid, ids, values, context)

    def create(self, cr, uid, values, context=None):
        _logger.error("Values = %s",values)
        sales_price = values.get('sale_price')
        mrp = values.get('mrp')
        if sales_price and mrp:
            sp_incl_tax = sales_price + (sales_price * .05)
            #Assuming 5% tax
            if(sp_incl_tax>mrp):
                raise osv.except_osv(_('Processing Error!'), _('Batch number has : Sales Price + Tax more that mrp :(%f+5%%) %f > %f)!') \
                                     % (sales_price, sp_incl_tax, mrp))
        return super(stock_production_lot, self).create(cr, uid, values, context)

    _columns = {
            'sale_price':fields.float('Sale Price',digits=(4,2)),
            'mrp':fields.float('MRP',digits=(4,2)),
            'cost_price':fields.float('Cost Price',digits=(4,2)),
            'name': fields.char('Batch Number', size=64)
            }

stock_production_lot()