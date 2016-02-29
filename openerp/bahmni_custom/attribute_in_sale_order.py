
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
                res[sale_order.id]=" "
        return res

    def _get_partner_attribute_Tribe_details(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale_order in self.browse(cr, uid, ids):
            partner_obj = self.pool.get("res.partner")
            partner = partner_obj.browse(cr,uid,sale_order.partner_id.id)
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner.id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res[sale_order.id] = partner_attribute.x_Is_Tribal
            else:
                res[sale_order.id]="N/A"
        return res
    def _get_partner_attribute_Sangam_details(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale_order in self.browse(cr, uid, ids):
            partner_obj = self.pool.get("res.partner")
            partner = partner_obj.browse(cr,uid,sale_order.partner_id.id)
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner.id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res[sale_order.id] = partner_attribute.x_Is_Sangam
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
                res[sale_order.id] = partner_attribute.x_Is_Premium_Paid
            else:
                res[sale_order.id]="N/A"
        return res
    def onchange_partner_id(self, cr, uid,ids, partner_id, context = None):
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids,partner_id,context=context)
        if partner_id:
            partner_attri_cnt=self.pool.get("res.partner.attributes").search(cr,uid,[('partner_id','=',partner_id)])
            if len(partner_attri_cnt) > 0:
                partner_attribute=self.pool.get("res.partner.attributes").browse(cr,uid,partner_attri_cnt[0])
                res['value']['partner_caste'] = partner_attribute.x_Tribe
                res['value']['partner_is_tribe'] = partner_attribute.x_Is_Tribal
                res['value']['partner_is_sangam'] = partner_attribute.x_Is_Sangam
                res['value']['partner_is_Premium'] = partner_attribute.x_Is_Premium_Paid
            else:
                res['value']['partner_caste'] = ''
                res['value']['partner_is_tribe']= ''
                res['value']['partner_is_sangam']= ''
                res['value']['partner_is_Premium']= ''
        return res

    _columns = {
        'partner_caste': fields.function(_get_partner_attribute_details, type='char', string ='Tribe'),
        'partner_is_tribe': fields.function(_get_partner_attribute_Tribe_details, type='char', string ='Is Tribe'),
        'partner_is_sangam':fields.function(_get_partner_attribute_Sangam_details, type='char', string ='Is Sangam'),
        'partner_is_Premium':fields.function(_get_partner_attribute_Sangam_details, type='char', string ='Is Premium',),
    }
sale_order()