# models/report_sepatu_pdf.py

from odoo import models, fields, api


class ReportSepatuPDF(models.AbstractModel):
    _name = 'report.pabrikabc.report_sepatu_pdf'
    _description = 'Sepatu Report in PDF'

    tgl_laporan = fields.Date.today()

    @api.model
    def _get_report_values(self, docids, data=None):
        sepatu_records = self.env['abc.sepatu'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'abc.sepatu',
            'docs': sepatu_records,
            'tgl_laporan': self.tgl_laporan,
        }
