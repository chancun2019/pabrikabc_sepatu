from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ABCBahanSepatu(models.Model):
    _name = 'abc.bahan.sepatu'
    _description = 'Bahan Sepatu Model'
    _rec_name = 'nama_bahan_sepatu'

    nama_bahan_sepatu = fields.Char(string='Nama Bahan', required=True)
    stok = fields.Integer(string='Stok', default=0)
    harga_modal_bahan_sepatu = fields.Integer(string='Harga Modal Bahan Sepatu')
    nama_sepatu = fields.Many2many(comodel_name='abc.sepatu', string='Nama Sepatu')
    

    # S-changed
    nama_sepatu_total_stok = fields.Integer(string='Total Stok', compute='_compute_total_stok') #background
    current_stock = fields.Integer(string='Current Stock', compute='_compute_current_stock')
    ukuran_satuan = fields.Selection(selection=[('sepasang', 'Sepasang'), ('satuan', 'Satuan')], string='Ukuran Satuan', default='sepasang')
    deskripsi = fields.Text(string='Deskripsi')

    # Functions
    @api.depends('nama_sepatu')
    def _compute_total_stok(self):
        for record in self:
            record.nama_sepatu_total_stok = sum(record.nama_sepatu.mapped('stok'))

    @api.depends('nama_sepatu')
    def _compute_current_stock(self):
        for record in self:
            record.current_stock = record.stok - (record.nama_sepatu_total_stok * 2)