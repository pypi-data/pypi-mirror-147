from odoo import models, fields, api
from odoo.tools.translate import _

class VhAbstractContract(models.AbstractModel):
  _inherit = 'contract.abstract.contract'

  account_receivable_id = fields.Many2one('account.account',string=_("Receivable Account"))