# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class VhInvoicingOrderItem(models.Model):
  _name = 'vh.invoicing.order.item'
  _inherit = ['mail.thread','vh.model.sequence.mixin']
  _prefix = "ORDER-ITEM"
  name= fields.Char(_("Name"))
  partner_id = fields.Many2one('res.partner',string=_("Partner"))
  order_id = fields.Many2one('vh.invoicing.order',string=("Order"))
  invoice_ids = fields.One2many('account.invoice','order_item_id',string=_("Invoices"))
  total_invoiced = fields.Float(string=_("Total invoiced"),compute="_get_total_invoiced",store=False)
  total_untaxed_invoiced = fields.Float(string=_("Total invoiced untaxed"),compute="_get_total_untaxed_invoiced",store=False)
  total_taxes = fields.Float(string=_("Total taxes"),compute="_get_total_taxes",store=False)
  company_id = fields.Many2one('res.company',string=_("System Company"),compute="_get_company_id",store=False)
  period = fields.Char(string=_("Period"),compute="_get_period")
  currency_id = fields.Many2one(
    'res.currency',
    string='Currency',
    compute="_get_currency_id"
  )
  payment_mode_id = fields.Many2one(
    'account.payment.mode',
    string='Currency',
    compute="_get_payment_mode_id"
  )
  comment = fields.Char(string="Terms & Conditions",compute="_get_comment")
  partner_bank_id = fields.Many2one(
    'res.partner.bank',
    string='Partner Bank',
    compute="_get_partner_bank_id"
  )
  receipt_total_invoiced = fields.Float(string=_("Total invoiced"),compute="_get_receipt_total_invoiced",store=False)
  receipt_total_untaxed_invoiced = fields.Float(string=_("Total invoiced untaxed"),compute="_get_receipt_total_untaxed_invoiced",store=False)
  receipt_total_taxes = fields.Float(string=_("Total taxes"),compute="_get_receipt_total_taxes",store=False)
  receipt_invoice_ids = fields.One2many(
    'account.invoice',
    string=_("Receipt Invoices"),
    compute="_get_receipt_invoice_ids",
    store=False
  )
  non_receipt_invoice_ids = fields.One2many(
    'account.invoice',
    string=_("Non Receipt Invoices"),
    compute="_get_non_receipt_invoice_ids",
    store=False
  )
  receipt_line_ids = fields.One2many(
    'account.invoice.line',
    'invoice_id', string='Invoice Lines',
    oldname='invoice_line',
    readonly=True,
    store=False,
    compute="_get_receipt_line_ids"
  )
  report_doc_filename = fields.Char(
    string=_("Report doc filename"),
    compute="_get_report_doc_filename",
    store="False"
  )
  report_ref = fields.Char(
    string=_("Report ref"),
    compute="_get_report_ref",
    store="False"
  )

  _order = "name desc"

  @api.depends('name')
  def _get_report_doc_filename(self):
    for record in self:
      record.report_doc_filename = _("rebut-habitatge-")+record.report_ref

  @api.depends('name')
  def _get_report_ref(self):
    for record in self:
      record.report_ref = record.name.strip(self._prefix)

  @api.depends('invoice_ids')
  def _get_receipt_invoice_ids(self):
    for record in self:
      record.receipt_invoice_ids = record.invoice_ids.filtered(lambda r: r.journal_id.belongs_to_receipt_doc == True)

  @api.depends('invoice_ids')
  def _get_non_receipt_invoice_ids(self):
    for record in self:
      record.non_receipt_invoice_ids = record.invoice_ids.filtered(lambda r: r.journal_id.belongs_to_receipt_doc != True)

  def _get_receipt_total_invoiced(self):
    for record in self:
      total = 0
      for invoice in record.receipt_invoice_ids:
        total += invoice.amount_total
      record.receipt_total_invoiced = total

  def _get_receipt_total_untaxed_invoiced(self):
    for record in self:
      total = 0
      for invoice in record.receipt_invoice_ids:
        total += invoice.amount_untaxed
      record.receipt_total_untaxed_invoiced = total

  def _get_receipt_total_taxes(self):
    for record in self:
      total = 0
      for invoice in record.receipt_invoice_ids:
        total += invoice.amount_tax
      record.receipt_total_taxes = total

  @api.depends('invoice_ids')
  def _get_receipt_line_ids(self):
    for record in self:
      receipt_line_ids_ids = self.env['account.invoice.line']
      for invoice in record.invoice_ids:
        if invoice.journal_id.belongs_to_receipt_doc:
          receipt_line_ids_ids += invoice.invoice_line_ids
      self.receipt_line_ids = receipt_line_ids_ids

  @api.depends('invoice_ids')
  def _get_total_invoiced(self):
    for record in self:
      total = 0
      for invoice in record.invoice_ids:
        total += invoice.amount_total
      record.total_invoiced = total

  @api.depends('invoice_ids')
  def _get_total_untaxed_invoiced(self):
    for record in self:
      total = 0
      for invoice in record.invoice_ids:
        total += invoice.amount_untaxed
      record.total_untaxed_invoiced = total

  @api.depends('invoice_ids')
  def _get_total_taxes(self):
    for record in self:
      total = 0
      for invoice in record.invoice_ids:
        total += invoice.amount_tax
      record.total_taxes = total

  @api.depends('invoice_ids')
  def _get_currency_id(self):
    for record in self:
      record.currency_id = False
      for invoice in record.receipt_invoice_ids:
        if invoice.currency_id:
          record.currency_id = invoice.currency_id.id
          break

  @api.depends('invoice_ids')
  def _get_payment_mode_id(self):
    for record in self:
      record.payment_mode_id = False
      for invoice in record.receipt_invoice_ids:
        if invoice.payment_mode_id:
          record.payment_mode_id = invoice.payment_mode_id.id
          break

  @api.depends('invoice_ids')
  def _get_comment(self):
    for record in self:
      record.comment = False
      for invoice in record.receipt_invoice_ids:
        if invoice.comment:
          record.comment = invoice.comment
          break

  @api.depends('invoice_ids')
  def _get_partner_bank_id(self):
    for record in self:
      record.partner_bank_id = False
      for invoice in record.receipt_invoice_ids:
        if invoice.mandate_id.partner_bank_id:
          record.partner_bank_id = invoice.mandate_id.partner_bank_id.id
          break

  @api.depends('order_id')
  def _get_period(self):
    for record in self:
      if record.order_id:
        record.period = record.order_id.period

  def _get_company_id(self):
    for record in self:
      record.company_id = record.env.user.company_id.id