from openerp.osv import fields, osv
import logging
from logging import getLogger

_logger = getLogger(__name__)


class claim_type(osv.osv):
    _name = 'claim.type'
    _description = "Type of program"
    _columns = {
        'claim_type': fields.selection([('1', 'Sickle Cell'), ('2', 'Bed Grant')], 'Claim Type'),
        'erp_patient_id':fields.many2one('res.partner','ERP Patient Id',required=True),
    }

    def create(self, cr, uid, values, context=None):

        res=self.pool.get('claim.type').search(cr, uid, [('erp_patient_id', '=', values['erp_patient_id'])], limit=1)
        _logger.error('claim_type------RESult----------%s',res)
        if len(res)>0:
            # super(osv.osv, self).write(cr, uid, ids, vals, context=context)
            # record = self.browse(cr,uid,res)
            # claim_type.write({'claim_type': values['claim_type']})
            super(osv.osv, self).write(cr, uid,res, values, context)
            erp_patient = res[0];
            # _logger('claim_type------create----------%s',erp_patient)
        else :
            erp_patient = osv.Model.create(self,cr, uid, values, context)
            _logger.error('claim_type------update----------%s',erp_patient)
        return erp_patient
claim_type()
