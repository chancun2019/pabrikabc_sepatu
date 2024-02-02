from odoo import models, fields

class ABCJenisSepatu(models.Model):
    _name = 'abc.jenis_sepatu'
    _description = 'Jenis Sepatu Model'

    id_jenis = fields.Char(string='ID Jenis', required=True)
    nama_jenis = fields.Char(string='Nama Jenis', required=True)
    deskripsi = fields.Text(string='Deskripsi')

class JenisBarang(models.Model):
    _name = 'abc.jenis_barang'
    _inherit = 'abc.jenis_sepatu'
    _description = 'Jenis Barang Model'

    _table = 'abc_jenis_barang'  # Tabel yang digunakan untuk jenis_barang

    jenis_barang_ids = fields.One2many('abc.barang', 'jenis_barang_id', string='Barang')
