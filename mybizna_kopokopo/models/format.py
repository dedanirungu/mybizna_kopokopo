from odoo import models, fields


class Format(models.Model):

    _name = 'mybizna.mobilecom.format'
    _rec_name = 'title'

    title = fields.Char('Title', required=True)
    format = fields.Text('Format', required=True)
    fields_str = fields.Text('Fields', required=True)
    published = fields.Boolean('Published')
