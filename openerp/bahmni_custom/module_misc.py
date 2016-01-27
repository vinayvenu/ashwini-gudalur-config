import logging
from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)

class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    _order = "id"
    _columns={
        'tin_number':fields.char('TIN'),
        }
res_partner()

