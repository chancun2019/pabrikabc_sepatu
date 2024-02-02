from odoo import models, fields, api

class ABCManusia(models.Model):
    _name = 'abc.manusia'
    _description = 'deskripsi global manusia'
    _rec_name = 'nama_manusia'

    nama_manusia = fields.Char(string='Nama', required=True)
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female'),])
    alamat = fields.Char(string='Alamat')
    
    
    
