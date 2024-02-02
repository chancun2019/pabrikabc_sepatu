from odoo import models, fields, api

class ABCSupplier(models.Model):
    _name = 'abc.supplier'
    _description = 'Supplier Model'
    _rec_name = 'name_supplier'

    name_supplier = fields.Char(string='Supplier Name', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    contact_person = fields.Char(string='Contact Person')
    
    nama_sepatu = fields.Many2many(comodel_name='abc.sepatu', string='Nama Sepatu')

