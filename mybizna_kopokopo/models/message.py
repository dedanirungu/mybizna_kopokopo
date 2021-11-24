from odoo import models, fields, api

from ..classes.message_processor import MessageProcessor

import requests, re, logging

class Message(models.Model):

    _name = 'mybizna.mobilecom.message'

    phone = fields.Char('Phone', required=True)
    message = fields.Text('Message', required=True)
    direction = fields.Selection(
        [('in', 'In'), ('out', 'Out')], 'Direction', required=True, default='in')
    date_sent = fields.Datetime('Date Sent')
    params = fields.Text('Params')
    playsms_id = fields.Integer('Playsms ID')
    gateway_id = fields.Many2one(
        'mybizna.mobilecom.gateways', string='Gateways')
    completed = fields.Boolean('Completed')
    successful = fields.Boolean('Successful')


    def name_get(self):

        res = []

        for rec in self:
            res.append((rec.id, "%s" % rec.message[:75]))     

        return res

    
    def processMessages(self):

        message_processor = MessageProcessor()

        message_processor.processMessages(self.env)


    def fetchMessages(self):

        gateways = self.env['mybizna.mobilecom.gateways'].search([
            ("published", "=", True),
        ])

        messages = self.env['mybizna.mobilecom.message'].search([
            ("direction", "=", 'in')
        ], order="playsms_id desc")

        url = gateways[0].url

        payload = {
            'app': 'ws', 
            'op': 'ix', 
            'u': gateways[0].username, 
            'h': gateways[0].token, 
        }

        if len(messages):
            payload['last'] =  messages[0].playsms_id

        r = requests.get(url, params=payload)
        result = r.json()


        if 'data' in result:
            for item in result['data']:

                saverecord = True

                ignores = self.env['mybizna.mobilecom.ignore'].search([
                    ("published", "=", 1),
                ])

                if len(ignores):
                    for ignore in ignores:
                        parts = re.findall(ignore.format, item['msg'])

                        if len(parts) or item['msg'] == ignore.format:
                            saverecord = False

                if saverecord:

                    self.env['mybizna.mobilecom.message'].create({
                        'phone': ''.join(e for e in item['src'] if e.isalnum()),
                        'message': item['msg'],
                        'playsms_id': item['id'],
                        'date_sent': item['dt'],
                        'direction': 'in',
                    })

    def sendMessages(self):

        gateways = self.env['mybizna.mobilecom.gateways'].search([
            ("published", "=", True),
        ])

        messages = self.env['mybizna.mobilecom.message'].search([
            ("direction", "=", 'out'),
            ("completed", "=", False),
        ])

        for message in messages:

            url = gateways[0].url

            payload = {
                'app': 'ws', 
                'op': 'pv', 
                'u': gateways[0].username, 
                'h': gateways[0].token, 
                'to': message.phone, 
                'msg': message.message, 
            }

            r = requests.get(url, params=payload)
            result = r.json()
            
            message.write({'completed': True, 'successful': True})
            self.env.cr.commit()