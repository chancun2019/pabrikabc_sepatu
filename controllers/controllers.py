# -*- coding: utf-8 -*-
# from odoo import http


# class Addonsxx/pabrikabc(http.Controller):
#     @http.route('/addonsxx/pabrikabc/addonsxx/pabrikabc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/addonsxx/pabrikabc/addonsxx/pabrikabc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('addonsxx/pabrikabc.listing', {
#             'root': '/addonsxx/pabrikabc/addonsxx/pabrikabc',
#             'objects': http.request.env['addonsxx/pabrikabc.addonsxx/pabrikabc'].search([]),
#         })

#     @http.route('/addonsxx/pabrikabc/addonsxx/pabrikabc/objects/<model("addonsxx/pabrikabc.addonsxx/pabrikabc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('addonsxx/pabrikabc.object', {
#             'object': obj
#         })
