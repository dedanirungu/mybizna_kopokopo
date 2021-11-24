from odoo import models, fields
import datetime

class Payment(models.Model):

    _name = 'mybizna.mobilecom.payment'
    _rec_name = 'phone'

    phone = fields.Char('Phone', required=True)
    code = fields.Char('Code', required=True)
    name = fields.Char('name', required=True)
    format_id = fields.Many2one(
        'mybizna.mobilecom.format', string='Format')
    message_id = fields.Many2one(
        'mybizna.mobilecom.message', string='Message')
    currency_id = fields.Many2one(
        'res.currency', string='Currency')
    partner_id = fields.Many2one('res.partner', 'Partner', ondelete="cascade")
    invoice_id = fields.Many2one('account.move', string='Invoice')
    amount = fields.Monetary('Amount', required=True)        
    account = fields.Char('Account', required=True)
    date_sent = fields.Date('Date Sent')
    completed = fields.Boolean('Completed')
    successful = fields.Boolean('Successful')

    
    def processPayments(self):

        payments = self.env['account.payment'].search([
            ('state','!=','reconciled'),
            ('payment_date','<=', ((datetime.datetime.now()-datetime.timedelta(minutes=1)).strftime('%Y-%m-%d')))
        ])

        if len(payments) != 0:
            for payment in payments:
                invoices = self.env['account.move'].search([
                    ('partner_id', '=', payment.partner_id.id),
                    ('account.move', '=', 'out_invoice'),
                    ('state', '=', 'posted'),
                    ('payment_state', '<>', 'paid')
                ], order="id desc")

            if len(invoices) != 0:
                    for invoice in invoices:
                        self.reconcile_invoice(invoice)


    def reconcile_invoice(self, invoice):

        if invoice.state != 'posted' or invoice.invoice_payment_state != 'not_paid' or not invoice.is_invoice(include_receipts=True):
            return False
            
        pay_term_line_ids = invoice.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))

        domain = [('account_id', 'in', pay_term_line_ids.mapped('account_id').ids),
            '|', ('move_id.state', '=', 'posted'), '&', ('move_id.state', '=', 'draft'), ('journal_id.post_at', '=', 'bank_rec'),
            ('partner_id', '=', invoice.commercial_partner_id.id),
            ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0),
            ('amount_residual_currency', '!=', 0.0)]

        if invoice.is_inbound():
                domain.extend([('credit', '>', 0), ('debit', '=', 0)])

        lines = self.env['account.move.line'].search(domain)

        if len(lines) != 0:
            for line in lines:
                lines = self.env['account.move.line'].browse(line.id)
                lines += invoice.line_ids.filtered(lambda line: line.account_id == lines[0].account_id and not line.reconciled)
                lines.reconcile()
