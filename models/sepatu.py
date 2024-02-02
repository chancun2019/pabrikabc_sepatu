from odoo import models, fields

class ABCSepatu(models.Model):
    _name = 'abc.sepatu'
    _description = 'Sepatu Model'
    _rec_name = 'nama_sepatu'

    id_sepatu = fields.Char(string='ID Sepatu', default=lambda self: self.env['ir.sequence'].next_by_code('abc.sepatu'), readonly=True)
    nama_sepatu = fields.Char(string='Nama', required=True)
    ukuran_sepatu = fields.Char(string='Ukuran')
    warna_sepatu = fields.Char(string='Warna')
    harga_sepatu = fields.Float(string='Harga')
    waktu_produksi = fields.Date(string='Waktu Produksi')
    stok = fields.Integer(string='Stok')
    image = fields.Binary(string='Image', attachment=True)

    jenis_bahan_sepatu = fields.Many2many('abc.bahan.sepatu', string='Jenis Bahan Sepatu')
    jenis_bahan_sepatu_display = fields.Char(string='Jenis Bahan Sepatu Display', compute='_compute_jenis_bahan_sepatu_display', store=True)

    # Existing field for the button label
    report_button_label = fields.Char(string='Report Button Label', compute='_compute_report_button_label', store=False)

    def _compute_jenis_bahan_sepatu_display(self):
        for record in self:
            names = ', '.join(record.jenis_bahan_sepatu.mapped('nama_bahan_sepatu'))
            record.jenis_bahan_sepatu_display = names

    # Existing compute method for jenis_bahan_sepatu_display
    def _compute_report_button_label(self):
        for record in self:
            # Your computation logic for report_button_label
            # Example:
            record.report_button_label = f"Label: {record.nama_sepatu}"  # Replace with your actual computation logic
