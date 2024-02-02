from odoo import models, fields, api
from odoo.exceptions import UserError

class ABCCustomer(models.Model):
    _name = 'abc.customer'
    _description = 'Customer Model'

    id_customer = fields.Char(string='ID Customer', required=True)
    nama = fields.Char(string='Nama', required=True)
    alamat = fields.Text(string='Alamat')
    pre_order_ids = fields.One2many('abc.pre_order', 'customer_id', string='Pre-Orders')
    order_ids = fields.One2many('abc.order', 'customer_id', string='Orders')

    @api.model
    def create_order(self, sepatu_id, quantity):
        sepatu = self.env['abc.sepatu'].browse(sepatu_id)
        if sepatu.quantity_on_hand >= quantity:
            order = self.env['abc.order'].create({
                'sepatu_id': sepatu.id,
                'customer_id': self.id,
                'quantity': quantity,
            })
            sepatu.write({'quantity_on_hand': sepatu.quantity_on_hand - quantity})
        else:
            pre_order = self.env['abc.pre_order'].create({
                'sepatu_id': sepatu.id,
                'customer_id': self.id,
                'quantity': quantity,
            })
            raise UserError("Stok tidak mencukupi. Pesanan Anda akan diproses sebagai pre-order.")
        return True
