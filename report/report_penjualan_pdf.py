from odoo import api, models

class ReportPenjualanPDF(models.AbstractModel):
    _name = 'report.pabrikabc.report_penjualan_pdf'
    _description = 'Penjualan PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Retrieve the records based on the provided document ids
        records = self.env['abc.penjualan.header'].browse(docids)

        # Compute total for each record (just an example, modify based on your logic)
        for record in records:
            total = sum(line.subtotal for line in record.penjualan_line)
            record.subtotal_penjualan_line = total  # Update the record with the computed subtotal

        # You can add more data to be passed to the report template if needed
        report_data = {
            'doc_ids': docids,
            'doc_model': 'abc.penjualan.header',
            'docs': records,
            # Add more data here if needed
        }

        return report_data
