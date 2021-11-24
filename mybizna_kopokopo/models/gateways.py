from odoo import models, fields


class Gateways(models.Model):

    _name = 'mybizna.mobilecom.gateways'
    _rec_name = 'title'

    title = fields.Char('Title', required=True)
    username = fields.Char('Username', required=True)
    token = fields.Char('Token', required=True)
    url = fields.Char('Url', required=True)
    type = fields.Selection(
        [('playsms', 'Playsms')], 'Type', default='playsms')
    published = fields.Boolean('Published')
