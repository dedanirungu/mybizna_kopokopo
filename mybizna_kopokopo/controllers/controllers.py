# -*- coding: utf-8 -*-
from odoo import http


class MobileCom(http.Controller):
    @http.route('/mobilecom/sms/post', auth='public')
    def index(self, **kw):
        return "Hello, world"

#     @http.route('/mybizna_mobilecom/mybizna_mobilecom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mybizna_mobilecom.listing', {
#             'root': '/mybizna_mobilecom/mybizna_mobilecom',
#             'objects': http.request.env['mybizna_mobilecom.mybizna_mobilecom'].search([]),
#         })

#     @http.route('/mybizna_mobilecom/mybizna_mobilecom/objects/<model("mybizna_mobilecom.mybizna_mobilecom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mybizna_mobilecom.object', {
#             'object': obj
#         })
