from odoo import models, fields, api


class MessageMoreinfo(models.Model):

    _name = 'mybizna.mobilecom.message_moreinfo'
    _rec_name = 'message_id'

    phone = fields.Char('Phone', required=True)
    name = fields.Char('Name')
    code = fields.Char('Code')
    date = fields.Char('Date')
    time = fields.Char('Time')
    amount = fields.Char('Amount')
    account = fields.Char('Account')
    datetime = fields.Datetime('Date')
    format_id = fields.Many2one(
        'mybizna.mobilecom.format', string='Format')
    partner_id = fields.Many2one('res.partner', 'Partner', ondelete="cascade")
    message_id = fields.Many2one(
        'mybizna.mobilecom.message', string='Message')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    request = fields.Char('Request')
    request_type = fields.Char('Request Type')
    note = fields.Char('Note')
