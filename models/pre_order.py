from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class ABCPreOrder(models.Model):
    _name = 'abc.pre_order'
    _description = 'Pre-order Model'

    customer_id = fields.Many2one('abc.customer', string='Customer', required=True)
    product_id = fields.Many2one('abc.sepatu', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now())

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancelled')
    ], string='State', default='draft', readonly=True, required=True)

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        # You can implement additional logic here, like sending confirmation emails, etc.

    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
        if vals.get('quantity', 0) <= 0:
            raise ValidationError(_("Quantity must be greater than zero."))
        
        product_id = vals.get('product_id')
        quantity = vals.get('quantity')
        available_stock = self.env['abc.sepatu'].browse(product_id).quantity_on_hand

        if available_stock >= quantity:
            raise ValidationError(_("Stock is sufficient, no need for pre-order."))

        return super(ABCPreOrder, self).create(vals)
