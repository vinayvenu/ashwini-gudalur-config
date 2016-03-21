from openerp.osv import fields, osv
import logging
from logging import getLogger

_logger = getLogger(__name__)


class syncjob_department_category_mapping(osv.osv):
    _name = 'syncjob.department.category.mapping'
    _description = "Department"


    _columns = {
        'department_name': fields.char('Department',required=True),
        'category_id':fields.many2one('product.category','Category Id',required=True,unique=True),
    }

    def create(self, cr, uid, values, context=None):

        res=self.pool.get('syncjob.department.category.mapping').search(cr, uid, [('category_id', '=', values['category_id'])], limit=1)
        _logger.error('dept_type------RESult----------%s',res)
        if len(res)>0:
            super(osv.osv, self).write(cr, uid,res, values, context)
            dept = res[0];
        else :
            dept = osv.Model.create(self,cr, uid, values, context)
            _logger.error('dept_type------update----------%s',dept)
        return dept


