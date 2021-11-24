import re, logging

from datetime import datetime,time


class MessageProcessor:

    def __init__(self,):
        env = {}

    def processMessages(self, env):

        self.env = env

        messages = self.env['mybizna.mobilecom.message'].search([
            ("direction", "=", "in"),
            ("completed", "!=", 1),
        ])    

        for message in messages:
            self.processMessage(message)    
            message.write({"completed": 1, "successful": 1})
            self.env.cr.commit()
             

    def processMessage(self, record):

        phone = record.phone


        found = self.processFormat(record)

        # search in moreinfo list
        moreinfo_list = self.env['mybizna.mobilecom.message_moreinfo'].search([
            ("phone", "=", phone),
        ])
     
        if len(moreinfo_list) > 1 and found:
  
            self.sendMessage('pending_request_info', record)

        elif(len(moreinfo_list) and not found):
            
            for moreinfo in moreinfo_list:

                if moreinfo.request_type == 'customer_not_found' or moreinfo.request_type == 'customer_not_found_again':
                    moreinfo = self.updateMoreinfo(moreinfo, {"account": record.message})

                self.processPayment(moreinfo)

                return True

        return False



    def processFormat(self, record):

        formats = self.env['mybizna.mobilecom.format'].search([
            ("published", "=", 1),
        ])

        if len(formats):
            for formating in formats:

                moreinfo = self.analyzeFormat(formating, record)

                if moreinfo:
                    self.processPayment(moreinfo)
                    return True

        return False

    def processPayment(self, moreinfo):

        setting = self.getDefaultSetting()


        if not moreinfo.account:
            if moreinfo.request_type == 'customer_not_found':

                self.sendMessage('customer_not_found_again', moreinfo)
                moreinfo = self.updateMoreinfo(moreinfo, {"request_type": 'customer_not_found_again'})

            else:
                self.sendMessage('customer_not_found', moreinfo)
                moreinfo = self.updateMoreinfo(moreinfo, {"request_type": 'customer_not_found'})


        elif moreinfo.account:


            partner = self.getPartner(moreinfo)

            if partner:
                    moreinfo = self.updateMoreinfo(moreinfo, {"partner_id": partner[0].id})
            else:
                if moreinfo.request_type == 'customer_not_found' or moreinfo.request_type == 'customer_not_found_again':
                    self.sendMessage('customer_not_found_again', moreinfo)
                else:
                    self.sendMessage('customer_not_found', moreinfo)

            if moreinfo.partner_id:

                invoices = self.getInvoices(moreinfo)

                moreinfo = self.updateMoreinfo(moreinfo, {"invoice_id": invoices[0].id})


            if moreinfo.partner_id and moreinfo.invoice_id:


                setting = self.getDefaultSetting()


                datetime_object = datetime.now()
                datetime_str = datetime_object.strftime('%Y-%m-%d %H:%M:%S')

                payment_log = self.env['mybizna.mobilecom.payment'].create({
                    "phone": moreinfo.phone,
                    "code": moreinfo.code,
                    "name": moreinfo.name,
                    "amount": moreinfo.amount,
                    "account": moreinfo.account,
                    "format_id": moreinfo.format_id.id,
                    "message_id": moreinfo.message_id.id,
                    "partner_id": moreinfo.partner_id.id,
                    "invoice_id": moreinfo.invoice_id.id,
                    "date_sent": str(moreinfo.datetime),
                    "completed": True,
                    "successful": True,
                })  
                self.env.cr.commit()


                Payment = self.env['account.payment'].with_context(active_model='account.move', active_id=moreinfo.invoice_id.id)

                payment = Payment.create({

                    'payment_date': datetime_str,
                    'payment_method_id': int(setting['payment_method_id']),
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'partner_id': moreinfo.partner_id.id,
                    'amount': moreinfo.amount,
                    'journal_id': int(setting['journal_id']),
                    'company_id': self.env.company.id,
                    'currency_id': int(setting['currency_id']),
                    #'payment_difference_handling': 'reconcile',
                    #'writeoff_account_id': int(setting['writeoff_account_id']),

                })
                self.env.cr.commit()

  
                self.sendMessage('payment_successful', moreinfo)

                payment.post()
                #moreinfo.unlink()
                self.env.cr.commit()



    def sendMessage(self, unique_name, moreinfo = None):

        admin_phone = self.env.company.phone


        _logger = logging.getLogger(__name__)
        _logger.warning(' %s', self.env.company)

        phone = invoice_id = note = amount = ''

        if moreinfo:

            account = moreinfo.account if hasattr(moreinfo, 'account') and moreinfo.account  else ''
            phone = moreinfo.phone if hasattr(moreinfo, 'phone') and moreinfo.phone  else ''
            invoice_id = moreinfo.invoice_id.id if hasattr(moreinfo, 'invoice_id') and moreinfo.invoice_id else ''
            note = moreinfo.note if hasattr(moreinfo, 'note') and moreinfo.note else ''
            amount = moreinfo.amount if hasattr(moreinfo, 'amount') and moreinfo.amount else ''

        templates = self.env['mybizna.mobilecom.message_template'].search([
            ("unique_name", "=", unique_name),
        ])

        message = 'Unknown issue prease contact admin ' + admin_phone

        if len(templates):
            for template in templates:
                message = template.template
                message = message.replace("[ACCOUNT]", account)
                message = message.replace("[PHONE]", phone)
                message = message.replace("[INVOICE_ID]", invoice_id)
                message = message.replace("[NOTE]", note)
                message = message.replace("[AMOUNT]", amount)
                message = message.replace("[ADMIN_PHONE]", admin_phone)

        self.env['mybizna.mobilecom.message'].create({
            'phone': moreinfo.phone,
            'message': message,
            'direction': 'out',
            'date_sent': datetime.now(),
        })
        self.env.cr.commit()


    def analyzeFormat(self, formating, record):

        parts = re.findall(formating.format, record.message)

        if parts and formating.fields_str:

            analysis = {'name': '', 'phone': '', 'code': '', 'date': '', 'message_id': record.id,
                        'time': '', 'amount': '', 'account': '', 'datetime': '', 'format_id': formating.id,
                        }

            fields = formating.fields_str.split(',')

            num = 0

            for field in fields:

                if field == 'name':
                    analysis['name'] = parts[0][num]
                if field == 'phone':
                    phone = parts[0][num]
                    suffix = phone[-9:]
                    prefix = 254
                    phone = str(prefix) + str(suffix)
                    analysis['phone'] = phone
                if field == 'code':
                    analysis['code'] = parts[0][num]
                if field == 'date':
                    analysis['date'] = parts[0][num]
                if field == 'time':
                    analysis['time'] = parts[0][num]
                if field == 'amount':
                    analysis['amount'] = float(
                        re.sub(r'[^\d.]', '', parts[0][num]))
                if field == 'account':
                    analysis['account'] = parts[0][num]

                num = num + 1

            
            if analysis['account'] == '':
                analysis['account'] = analysis['phone']

            datetime_str = analysis['date'] + " " + \
                analysis['time'].replace(' ', '')
            datetime_object = datetime.strptime(
                datetime_str, "%d/%m/%y %I:%M%p")
            analysis['datetime'] = datetime_object.strftime('%Y-%m-%d %H:%M:%S')

            moreinfo = self.env['mybizna.mobilecom.message_moreinfo'].create(analysis)
            self.env.cr.commit()

            return moreinfo

        else:

            return False

    def getDefaultSetting(self, ):

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

        default_currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1).id
        if not default_currency:
            default_currency = self.env['res.currency'].search([], limit=1).id

        return {
            'journal_id': params.get_param('mybizna_mobilecom_journal_id', default=default_journal),
            'payment_method_id': params.get_param('mybizna_mobilecom_payment_method_id', default=default_payment_method),
            'writeoff_account_id': params.get_param('mybizna_mobilecom_writeoff_account_id', default=default_writeoff_account),
            'currency_id': params.get_param('mybizna_mobilecom_currency_id', default=default_currency)
        }


    def getPartner(self, moreinfo):

        partner = self.env['res.partner'].search(
            [('phone', 'ilike', moreinfo.account)], limit=1)

        if(len(partner)):
            self.updateMoreinfo(moreinfo, {"partner_id": partner[0].id})

            return partner[0]

        return False

    def getInvoices(self, moreinfo):

        invoices = self.env['account.move'].search([
            ('partner_id', '=', moreinfo.partner_id.id),
            ('type', '=', 'out_invoice'),
            ('invoice_payment_state', '<>', 'paid')
        ], order="id desc")

        return invoices
        
    def updateMoreinfo(self, moreinfo, data):

        moreinfo.write(data)
        self.env.cr.commit()

        return self.env['mybizna.mobilecom.message_moreinfo'].browse(moreinfo.id)
        

