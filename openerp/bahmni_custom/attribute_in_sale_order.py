
import logging

from osv import fields, osv
from logging import getLogger

_logger = getLogger(__name__)


class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"

    def _get_partner_attribute_details(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale_order in self.browse(cr, uid, ids):
            partner_obj = self.pool.get("res.partner")
            partner = partner_obj.browse(cr,uid,sale_order.partner_id.id)
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner.id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res[sale_order.id] = partner_attribute.x_Tribe
            else:
                res[sale_order.id]=""
        return res

    def _get_partner_attribute_Tribe_details(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale_order in self.browse(cr, uid, ids):
            partner_obj = self.pool.get("res.partner")
            partner = partner_obj.browse(cr,uid,sale_order.partner_id.id)
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner.id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res[sale_order.id] = self.getYesOrNo(partner_attribute.x_Is_Tribal)
            else:
                res[sale_order.id]=""
        return res
    def _get_partner_attribute_Sangam_details(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale_order in self.browse(cr, uid, ids):
            partner_obj = self.pool.get("res.partner")
            partner = partner_obj.browse(cr,uid,sale_order.partner_id.id)
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner.id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res[sale_order.id] = self.getYesOrNo(partner_attribute.x_Is_Sangam)
            else:
                res[sale_order.id]=""
        return res
    def _get_partner_attribute_Premium_details(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale_order in self.browse(cr, uid, ids):
            partner_obj = self.pool.get("res.partner")
            partner = partner_obj.browse(cr,uid,sale_order.partner_id.id)
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner.id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res[sale_order.id] = self.getYesOrNo(partner_attribute.x_Is_Premium_Paid)
            else:
                res[sale_order.id]=""
        return res

    def _get_order_type(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale_order in self.browse(cr, uid, ids):
            if (sale_order.shop_id):
                map_id_List = self.pool.get('order.type.shop.map').search(cr, uid, [('shop_id', '=', sale_order.shop_id.id)], context=context)
                if(map_id_List):
                    order_type_map = self.pool.get('order.type.shop.map').browse(cr, uid, map_id_List[0], context=context)
                    res[sale_order.id] = order_type_map.order_type
                else:
                    res[sale_order.id]=""
            else:
                res[sale_order.id]=""
        return res

    def _get_partner_attribute_Visiting(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale_order in self.browse(cr, uid, ids):
            partner_obj = self.pool.get("res.partner")
            partner = partner_obj.browse(cr,uid,sale_order.partner_id.id)
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner.id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res[sale_order.id] = partner_attribute.x_Visiting
            else:
                res[sale_order.id]=""
        return res
    def getYesOrNo(self, name):
        if(name):
            return 'Yes' if name.lower()=='True'.lower() else 'No'
        return ''

    def onchange_partner_id(self, cr, uid,ids, partner_id, context = None):
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids,partner_id,context=context)
        if partner_id:
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner_id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res['value']['partner_caste'] = partner_attribute.x_Tribe
                res['value']['partner_is_tribe'] = self.getYesOrNo(partner_attribute.x_Is_Tribal)
                res['value']['partner_is_sangam'] = self.getYesOrNo(partner_attribute.x_Is_Sangam)
                res['value']['partner_is_Premium'] = self.getYesOrNo(partner_attribute.x_Is_Premium_Paid)
                res['value']['partner_visting'] = partner_attribute.x_Visiting
            else:
                res['value']['partner_caste'] = ''
                res['value']['partner_is_tribe']= ''
                res['value']['partner_is_sangam']= ''
                res['value']['partner_is_Premium']= ''
                res['value']['partner_visting']= ''
        return res;

    _columns = {
        'partner_caste': fields.function(_get_partner_attribute_details, type='char', string ='Tribe'),
        'partner_is_tribe': fields.function(_get_partner_attribute_Tribe_details, type='char', string ='Is Tribe'),
        'partner_is_sangam':fields.function(_get_partner_attribute_Sangam_details, type='char', string ='Is Sangam'),
        'partner_is_Premium':fields.function(_get_partner_attribute_Premium_details, type='char', string ='Is Premium',),
        'partner_visting':fields.function(_get_partner_attribute_Visiting, type='char', string ='Visiting',),
        'order_type':fields.function(_get_order_type, type='char', string ='Order Type',),
    }
sale_order()