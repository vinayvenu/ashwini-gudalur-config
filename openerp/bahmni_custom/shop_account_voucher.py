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
    _name = 'account.voucher'
    _inherit = "account.voucher"
    _columns={
        'shop_id':fields.many2one('sale.shop',required='True',string ='Collection Point')
    }