from odoo import models, fields


class PaymentSource(models.Model):

    _name = 'mybizna.mobilecom.payment_source'
    _rec_name = 'phone'

    phone = fields.Char('Phone', required=True)
    published = fields.Boolean('Published')

