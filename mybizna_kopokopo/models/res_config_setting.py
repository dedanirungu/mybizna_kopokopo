from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_account_journal(self):

        journal = self.env['account.journal'].search([('name', '=', 'Cash')], limit=1).id

        if not journal:
            journal = self.env['account.journal'].search([], limit=1).id

        return journal 


    def _default_payment_method(self):

        payment_method = self.env['account.payment.method'].search([('name', '=', 'Electronic')], limit=1).id

        if not payment_method:
            payment_method = self.env['account.payment.method'].search([], limit=1).id

        return payment_method 


    def _default_writeoff_account(self):

        writeoff_account = self.env['account.account'].search([('name', 'ilike', 'Investment')], limit=1).id

        if not writeoff_account:
            writeoff_account = self.env['account.account'].search([], limit=1).id

        return writeoff_account 


    def _default_currency(self):

        currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1).id

        if not currency:
            currency = self.env['res.currency'].search([], limit=1).id

        return currency 



    mybizna_mobilecom_journal_id = fields.Many2one('account.journal', 'Journal', default=_default_account_journal)
    mybizna_mobilecom_payment_method_id = fields.Many2one('account.payment.method', 'Payment', default=_default_payment_method)
    mybizna_mobilecom_writeoff_account_id = fields.Many2one('account.account', 'Writeoff Journal', default=_default_writeoff_account)
    mybizna_mobilecom_currency_id = fields.Many2one('res.currency', 'Currency', default=_default_currency)


    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()

        default_journal = self.env['account.journal'].search([('name', '=', 'Cash')], limit=1).id
        if not default_journal:
            default_journal = self.env['account.journal'].search([], limit=1).id

        default_payment_method = self.env['account.payment.method'].search([('name', '=', 'Electronic')], limit=1).id
        if not default_payment_method:
            default_payment_method = self.env['account.payment.method'].search([], limit=1).id

        default_writeoff_account = self.env['account.account'].search([('name', 'ilike', 'Investment')], limit=1).id
        if not default_writeoff_account:
            default_writeoff_account = self.env['account.account'].search([], limit=1).id

        default_currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1).id
        if not default_currency_id:
            default_currency_id = self.env['res.currency'].search([], limit=1).id

        mybizna_mobilecom_journal_id = params.get_param('mybizna_mobilecom_journal_id', default=default_journal)
        mybizna_mobilecom_payment_method_id = params.get_param('mybizna_mobilecom_payment_method_id', default=default_payment_method)
        mybizna_mobilecom_writeoff_account_id = params.get_param('mybizna_mobilecom_writeoff_account_id', default=default_writeoff_account)
        mybizna_mobilecom_currency_id = params.get_param('mybizna_mobilecom_currency_id', default=default_currency_id)

        res.update(
            mybizna_mobilecom_journal_id=int(mybizna_mobilecom_journal_id),
            mybizna_mobilecom_payment_method_id=int(mybizna_mobilecom_payment_method_id),
            mybizna_mobilecom_writeoff_account_id=int(mybizna_mobilecom_writeoff_account_id),
            mybizna_mobilecom_currency_id=int(mybizna_mobilecom_currency_id),
        )
        return res


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("mybizna_mobilecom_journal_id",  self.mybizna_mobilecom_journal_id.id)
        self.env['ir.config_parameter'].sudo().set_param("mybizna_mobilecom_payment_method_id",  self.mybizna_mobilecom_payment_method_id.id)
        self.env['ir.config_parameter'].sudo().set_param("mybizna_mobilecom_writeoff_account_id",  self.mybizna_mobilecom_writeoff_account_id.id)
        self.env['ir.config_parameter'].sudo().set_param("mybizna_mobilecom_currency_id",  self.mybizna_mobilecom_currency_id.id)