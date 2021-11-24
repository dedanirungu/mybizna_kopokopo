from odoo import models, fields


class Ignore(models.Model):

    _name = 'mybizna.mobilecom.ignore'

    format = fields.Text('Format', required=True)
    published = fields.Boolean('Published')

    def name_get(self):

        res = []

        for rec in self:
            res.append((rec.id, "%s" % rec.format[:50]))     

        return res
