from odoo import models, fields, api, _

class ABCPegawai(models.Model):
    _name = 'abc.pegawai'
    _inherit = 'abc.manusia'
    _description = 'abc.pegawai'
    _rec_name = 'ref'

    ref = fields.Char(
        string="No. Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))

    bagian = fields.Selection(
        string='Bagian',
        selection=[('kasir', 'Kasir'),
                   ('pabrik', 'Pabrik'),
                   ('kebersihan', 'Kebersihan')],
        required=True)
    gaji = fields.Integer(string='Gaji per bulan')
    foto = fields.Binary(string='Foto')

    # @api.model
    # def create(self, vals):
    #     if vals.get('ref', _("New")) == _("New"):
    #         bag = vals.get('bagian', 'kasir')
    #         if bag == 'kasir':
    #             vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.karyawankasir') or _("New")
    #         elif bag == 'akunting':
    #             vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.karyawanakunting') or _("New")
    #         elif bag == 'kebersihan':
    #             vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.karyawankebersihan') or _("New")
    #     record = super(ABCPegawai, self).create(vals)
    #     return record

    # def write(self, vals):
    #     bag = vals.get('bagian', 'kasir')
    #     if bag == 'kasir':
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.karyawankasir') or _("New")
    #     elif bag == 'akunting':
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.karyawanakunting') or _("New")
    #     elif bag == 'kebersihan':
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.karyawankebersihan') or _("New")
    #     record = super(ABCPegawai, self).write(vals)
    #     return record
