# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class addonsxx/pabrikabc(models.Model):
#     _name = 'addonsxx/pabrikabc.addonsxx/pabrikabc'
#     _description = 'addonsxx/pabrikabc.addonsxx/pabrikabc'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
