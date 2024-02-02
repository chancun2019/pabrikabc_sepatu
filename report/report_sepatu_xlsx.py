# reports/report_sepatu_xlsx.py

from odoo import models, fields, api

class ReportSepatuXlsx(models.AbstractModel):
    _name = 'report.pabrikabc.report_sepatu_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    tgl_laporan = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, sepatu):
        sheet = workbook.add_worksheet('Sepatu')
        bold = workbook.add_format({'bold': True})
        italic = workbook.add_format({'italic': True})
        
        row = 1
        col = 0

        sheet.write(0, 0, str(self.tgl_laporan))
        sheet.write(row, col, 'Nama Sepatu', bold)
        sheet.write(row, col+1, 'Harga', bold)
        sheet.write(row, col+2, 'Stok', bold)

        for obj in sepatu:
            row += 1
            col = 0
            sheet.write(row, col, obj.nama_sepatu, italic)
            sheet.write(row, col+1, obj.harga_sepatu)
            sheet.write(row, col+2, obj.stok)
