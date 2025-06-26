# -*- coding: utf-8 -*-
# from odoo import http


# class PerpustakaanCustom(http.Controller):
#     @http.route('/perpustakaan_custom/perpustakaan_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/perpustakaan_custom/perpustakaan_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('perpustakaan_custom.listing', {
#             'root': '/perpustakaan_custom/perpustakaan_custom',
#             'objects': http.request.env['perpustakaan_custom.perpustakaan_custom'].search([]),
#         })

#     @http.route('/perpustakaan_custom/perpustakaan_custom/objects/<model("perpustakaan_custom.perpustakaan_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('perpustakaan_custom.object', {
#             'object': obj
#         })

