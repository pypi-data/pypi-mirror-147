from odoo import models, fields, api
from odoo.tools.translate import _

class VhContract(models.Model):
  _inherit = 'contract.contract'

  @api.multi
  def _prepare_invoice(self, date_invoice, journal=None):
    for record in self:
      invoice_vals = res = super(VhContract,record)._prepare_invoice(date_invoice,journal)
      if record.account_receivable_id:
        invoice_vals['account_id'] = record.account_receivable_id.id
      if record.note:
        invoice_vals['comment'] = record.note
      return invoice_vals