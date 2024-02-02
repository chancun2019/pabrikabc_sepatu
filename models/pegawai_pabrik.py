from odoo import models, fields, api

class ABCPegawaiPabrik(models.Model):
    _inherit = 'res.partner'

    gaji = fields.Integer(string='Gaji')
    channel_ids = fields.Many2many('mail.channel', string='Channels')  # Remove or rename this line

