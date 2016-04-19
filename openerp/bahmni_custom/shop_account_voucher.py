import time
from lxml import etree

from openerp import netsvc
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
import logging
_logger = logging.getLogger(__name__)


class account_voucher(osv.osv):

    def getYesOrNo(self, name):
        if(name):
            return 'Yes' if name.lower()=='True'.lower() else 'No'
        return ''

    def _get_partner_attribute_Tribe_details(self, cr, uid, ids, name, args, context=None):
        res = {}
        for account_voucher in self.browse(cr, uid, ids):
            partner_obj = self.pool.get("res.partner")
            _logger.error("Partner Id",account_voucher.partner_id)
            if account_voucher.partner_id:
                partner = partner_obj.browse(cr,uid,account_voucher.partner_id.id)
                partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner.id)])
                if len(partner_attri_cnt) > 0:
                    partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                    res[account_voucher.id] = self.getYesOrNo(partner_attribute.x_Is_Tribal)
                else:
                    res[account_voucher.id]=""
            else:
                res[account_voucher.id]=""
        return res

    _name = 'account.voucher'
    _inherit = "account.voucher"
    _columns={
        'shop_id':fields.many2one('sale.shop',required='True',string ='Collection Point'),
        'partner_is_tribe': fields.function(_get_partner_attribute_Tribe_details, type='char', string ='Is Tribe')
    }


class stock_picking(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    _columns = {
        'shop_id': fields.related('sale_id', 'shop_id', type="many2one", relation="sale.shop", string='Shop', store=True, readonly=True)

        }



class stock_picking_out(osv.osv):
    _name = 'stock.picking.out'
    _inherit = 'stock.picking.out'
    _columns = {
        'shop_id': fields.related('sale_id', 'shop_id', type="many2one", relation="sale.shop", string='Shop', store=True, readonly=True)
    }
