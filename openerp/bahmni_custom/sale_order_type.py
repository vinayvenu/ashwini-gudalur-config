import logging
import time
import decimal_precision as dp

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import uuid
from osv import fields, osv
from tools.translate import _
from openerp import netsvc
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import logging
_logger = logging.getLogger(__name__)


class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    def action_button_confirm(self, cr, uid, ids, context=None):
        # assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        # wf_service = netsvc.LocalService('workflow')
        # wf_service.trg_validate(uid, 'sale.order', ids[0], 'order_confirm', cr)
        sale_order_line=self.pool.get("sale.order.line").search(cr,uid,[('order_id','=',ids[0])])
        if len(sale_order_line) == 1:
            return super(sale_order, self).action_button_confirm( cr, uid, ids, context)
        else:
            if len(sale_order_line) < 1:
                return super(sale_order, self).action_button_confirm( cr, uid, ids, context)
            else:
                commoncatlist=self.pool.get("product.category").search(cr,uid,[('name','=','Common')])
                commoncat = commoncatlist[0];
                _logger.error("common_cat===%s",commoncat)
                not_a_common_sol = self.getNotACommonSaleOrderLine(cr,uid,sale_order_line,commoncat)
                if not not_a_common_sol:
                    return super(sale_order, self).action_button_confirm( cr, uid, ids, context)
                else:
                    catIds = self.getArrayOfCategoryIds(cr,uid,not_a_common_sol)
                    catIds.append(commoncat);
                    _logger.error("not_common_cat===%s",catIds)
                for sol in sale_order_line:
                        _logger.error("Sol=%s",sol)
                        template = self.getProdTemplate(cr,uid,sol)
                        if template.categ_id.id not in catIds:
                            raise osv.except_osv(
                                _('Error!'),
                                _('You cannot have items from different departments in same quotation.'))
            return super(sale_order, self).action_button_confirm( cr, uid, ids, context)


    def getProdTemplate(self, cr,uid,sol):
        soltemp= self.pool.get("sale.order.line").browse(cr,uid,sol)
        product = self.pool.get("product.product").browse(cr,uid,soltemp.product_id.id)
        template = self.pool.get("product.template").browse(cr,uid,product.product_tmpl_id.id)
        return template;

    def getNotACommonSaleOrderLine(self, cr,uid,sale_order_lines,common_cat):
        # get the common's id
        for sol in sale_order_lines:
            template = self.getProdTemplate(cr,uid,sol)
            if template.categ_id.id!=common_cat:
                return sol;



    def getArrayOfCategoryIds(self, cr,uid,sol):
        res=[]
        template = self.getProdTemplate(cr,uid,sol)
        _logger.error("Template=%s",template)
        cr.execute("""select category_id from syncjob_department_category_mapping where department_name=
                      (select department_name from syncjob_department_category_mapping where category_id="""+str(template.categ_id.id)+")")
        rows = cr.fetchall()
        for row in rows:
            res.append(row[0])
        return res;

    _columns={
        'care_setting': fields.selection([('ipd', 'IPD'), ('opd', 'OPD')], 'Care Setting',required='True'),
    }

sale_order()
