from odoo import models, fields


class Sms(models.Model):

    _name = 'mybizna.mobilecom.sms'
    _rec_name = 'phone'

    phone = fields.Char('Phone', required=True)
    sms = fields.Text('SMS', required=True)
    direction = fields.Selection(
        [('in', 'In'), ('out', 'Out')], 'Direction', required=True, default='in')
    date_sent = fields.Date('Date Sent')
    completed = fields.Boolean('Completed')
    successful = fields.Boolean('Successful')
