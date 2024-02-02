from odoo import models, fields, api, _
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import TableStyle
from reportlab.platypus import Table
from reportlab.lib import colors
from odoo.exceptions import ValidationError
import qrcode
import base64

class PembelianBahan(models.Model):
    _name = 'abc.pembelian.bahan'
    _description = 'Pembelian Bahan'
    _rec_name = 'kode_pembelian'

    qr_code_pembelian = fields.Binary(string='QR Code', readonly=True, copy=False, attachment=True)
    kode_pembelian = fields.Char(string='Kode Pembelian', default=lambda self: self.env['ir.sequence'].next_by_code('abc.pembelian.bahan'), readonly=True)
    id_supplier = fields.Many2one(comodel_name='abc.supplier', string='Supplier')
    tanggal_pembelian = fields.Date(string='Tanggal Pembelian', default=fields.Date.today())
    pembelian_bahan_line = fields.One2many('abc.pembelian.bahan.line', 'id_pembelian', string='Pembelian Bahan Line')

    def submit_pembelian(self):
        for record in self:
            for line in record.pembelian_bahan_line:
                line.nama_bahan_sepatu.stok += line.qty_beli

    @api.model
    # sequence
    def create(self, vals):
        vals['kode_pembelian'] = self.env['ir.sequence'].next_by_code('abc.pembelian.bahan')
        return super(PembelianBahan, self).create(vals)
    
    def submit_pembelian(self):
        """
        After submit pembelian, will increase the stock"""
        for record in self:
            for line in record.pembelian_bahan_line:
                line.nama_bahan_sepatu.stok += line.qty_beli
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='Status', default='draft', readonly=True)
    
    def confirm_pembelian(self):
        self.write({'state': 'done'})
        reference_no = self.kode_pembelian  # or any other reference number you want to use
        qr_code = self.generate_qr_code(reference_no)
        self.write({'qr_code_pembelian': qr_code})

    def generate_qr_code(self, reference_no):
        try:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
            qr.add_data(reference_no)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            self.write({'qr_code_pembelian': qr_image})  # Update the QR code field
            return qr_image
        except ImportError:
            return False

        
    def generate_pdf_report(self):
        # Create a buffer to store the PDF content
        buffer = BytesIO()

        # Create a ReportLab PDF document
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Add content to the PDF document
        pdf.setTitle(f"Pembelian Bahan PDF Report - {self.kode_pembelian}")

        # Add QR Code
        qr_code = self.qr_code_pembelian
        if qr_code:
            qr_code_img = BytesIO(base64.b64decode(qr_code))
            pil_image = Image.open(qr_code_img)
            pil_image_format = pil_image.format or 'PNG'
            qr_code_img.seek(0)  # Reset the buffer position

        # Draw the image on the PDF
            pdf.drawInlineImage(pil_image, 400, 500, width=100, height=100)

        # Add report header
        pdf.setFont("Helvetica", 16)
        pdf.drawString(100, 750, f"Pembelian Bahan PDF Report")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 730, f"Kode Pembelian: {self.kode_pembelian}")
        pdf.drawString(100, 710, f"Tanggal Pembelian: {self.tanggal_pembelian}")
        pdf.drawString(100, 690, f"Supplier: {self.id_supplier.name_supplier}")

        # Create a list to store data for the pembelian bahan line table
        table_data = [
            ["Nama Bahan Sepatu", "Quantity Pembelian", "Harga Beli", "Bayar"]
        ]

        # Add pembelian bahan line details to the table data
        for line in self.pembelian_bahan_line:
            table_data.append([line.nama_bahan_sepatu.nama_bahan_sepatu, line.qty_beli, line.modal, line.bayar])

        # Create a table and set its style
        table = Table(table_data, colWidths=[200, 80, 80, 80], hAlign='CENTER')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))

        # Draw the table on the PDF
        table.wrapOn(pdf, 400, 620)
        table.drawOn(pdf, 100, 620)

        # Save the PDF content to the buffer
        pdf.save()

        # Move the buffer position to the beginning
        buffer.seek(0)
        pdf_content = buffer.read()
        buffer.close()

        return pdf_content

    # Modified method to store the generated PDF report
    def action_generate_pdf_report(self):
        pdf_content = self.generate_pdf_report()

        # Create an ir.attachment record to store the PDF content
        attachment = self.env['ir.attachment'].create({
            'name': f'Pembelian_Bahan_Report_{self.kode_pembelian}.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'store_fname': f'Pembelian_Bahan_Report_{self.kode_pembelian}.pdf',
            'res_model': self._name,
            'res_id': self.id,
        })

        # Update the 'qr_code_pembelian' field with the attachment ID
        self.write({'qr_code_pembelian': base64.b64encode(pdf_content)})

        # Construct the URL for the attachment
        return {
            'name': _('Pembelian Bahan PDF Report'),
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'new',
        }

class PembelianBahanLine(models.Model):
    _name = 'abc.pembelian.bahan.line'
    _description = 'Pembelian Bahan Line'

    id_pembelian = fields.Many2one('abc.pembelian.bahan', string='ID Pembelian', ondelete='cascade')
    nama_bahan_sepatu = fields.Many2one('abc.bahan.sepatu', string='Nama Bahan Sepatu')
    qty_beli = fields.Integer(string='Quantiy Pembelian')
    modal = fields.Integer(compute='_compute_modal', string='Harga Beli', store=True)
    bayar = fields.Integer(compute='_compute_bayar', string='Bayar', store=True)

    @api.depends('nama_bahan_sepatu')
    def _compute_modal(self):
        """
        To get the harga sepatu"""
        for record in self:
            record.modal = record.nama_bahan_sepatu.harga_modal_bahan_sepatu

    @api.depends('qty_beli', 'modal')
    def _compute_bayar(self):
        """
        compute bayar"""
        for record in self:
            record.bayar = record.qty_beli * record.nama_bahan_sepatu.harga_modal_bahan_sepatu
