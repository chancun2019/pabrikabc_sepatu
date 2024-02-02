from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ABCCustomer(models.Model):
    _name = 'abc.customers'
    _rec_name = 'name'
    
    name = fields.Char(string='Nama', required=True)
    phone_number = fields.Char(string='Nomor Telepon', required=True)
    email = fields.Char(string='Email')
    order_history = fields.One2many('abc.penjualan.header', 'customer_id', string='Order History')
    is_member = fields.Boolean(string='Member?', default=False)