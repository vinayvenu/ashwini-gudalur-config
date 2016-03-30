from openerp.osv import fields, osv

import logging

_logger = logging.getLogger(__name__)

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {
        'product_scheduleh': fields.boolean('Is Schedule H'),
    }
    _default={
        'product_scheduleh':False,
    }
product_product()