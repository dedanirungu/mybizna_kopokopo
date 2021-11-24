from odoo import models, fields, api


class MessageTemplate(models.Model):

    _name = 'mybizna.mobilecom.message_template'
    _rec_name = 'title'

    title = fields.Char('Title', required=True)
    unique_name = fields.Char('Unique Name', required=True)
    template = fields.Text('Template', required=True)
    published = fields.Boolean('Published')
