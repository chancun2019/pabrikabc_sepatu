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
    
class ABCPenjualanHeader(models.Model):
    _name = 'abc.penjualan.header'
    _description = 'Penjualan Sepatu'
    _rec_name = 'reference_no'
    
    qr_code = fields.Binary(string='QR Code', readonly=True, copy=False, attachment=True)
    reference_no = fields.Char(string='Reference No.', default='New', readonly=True)
    pdf_report = fields.Binary(string='PDF Report', readonly=True, copy=False, attachment=True)
    transaction_date = fields.Datetime(string='Tanggal Transaksi', default=fields.Datetime.now())
    customer_id = fields.Many2one('abc.customers', string='Customer')
    state = fields.Selection([
        ('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')
    ], string='State', readonly=True, default="draft", required=True)
    is_membership = fields.Boolean(string="Member?", readonly=True)
    penjualan_line = fields.One2many('abc.penjualan.line', 'penjualan_header_id', string='Penjualan Line')
    subtotal_penjualan_line = fields.Float(compute='_compute_subtotal_penjualan_line', string='Subtotal', store=True)

    @api.depends('penjualan_line')
    def _compute_subtotal_penjualan_line(self):
        """
        To count the subtotal """
        for record in self:
            record.subtotal_penjualan_line = sum(record.penjualan_line.mapped('subtotal'))

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})
    
    def generate_qr_code(self, reference_no):
        """
        Generate QR Code based on reference number
        """
        try:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=4)
            qr.add_data(reference_no)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            return qr_image
        except ImportError:
            return False
    
    def decrease_stok_sepatu(self):
        """
        Decrease stok sepatu based on penjualan line
        """
        for line in self.penjualan_line:
            line.nama_sepatu.stok -= line.qty

    def action_done(self):
        """
        Set state to done, generate qr code, and decrease stok in sepatu
        """
        is_membership = self.is_membership
        sequence_code = 'abc.membership_sale' if is_membership else 'abc.sale'

        # Get the current sequence
        sequence = self.env['ir.sequence'].search([('code', '=', sequence_code)], limit=1)

        if sequence:
            prefix = sequence.prefix or ''
            suffix = sequence.suffix or ''

            # Generate reference_no with prefix and suffix
            reference_no = self.reference_no
            reference_with_prefix_suffix = f"{prefix}{reference_no}{suffix}"

            # Generate QR code based on the reference with prefix and suffix
            qr_code = self.generate_qr_code(reference_with_prefix_suffix)

            # Update the QR code field with the generated QR code
            self.write({'state': 'done', 'qr_code': qr_code})
            self.decrease_stok_sepatu()
        else:
            # Handle the case where the sequence is not found
            raise ValueError("Sequence not found for code: {}".format(sequence_code))

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        """
        Get checklist member if customer membership"""
        self.is_membership = self.customer_id.is_member

    def _get_reference_no(self):
        """Generate reference number based on membership status"""
        sequence_code = 'abc.membership_sale' if self.is_membership else 'abc.sale'
        return self.env['ir.sequence'].next_by_code(sequence_code) or ''
    
    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self._get_reference_no()
        return super(ABCPenjualanHeader, self).create(vals)

    # report pdf
    def generate_pdf_report(self):
        # Create a buffer to store the PDF content
        buffer = BytesIO()

        # Create a ReportLab PDF document
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Add content to the PDF document
        pdf.setTitle(f"Penjualan PDF Report - {self.reference_no}")

        # Add QR Code
        qr_code = self.qr_code
        if qr_code:
            qr_code_img = BytesIO(base64.b64decode(qr_code))
            pil_image = Image.open(qr_code_img)
            pil_image_format = pil_image.format or 'PNG'
            qr_code_img.seek(0)  # Reset the buffer position

        # Draw the image on the PDF
        pdf.drawInlineImage(pil_image, 400, 500, width=100, height=100)

            # Add report header
        pdf.setFont("Helvetica", 16)
        pdf.drawString(100, 750, f"Penjualan PDF Report - Reference No: {self.reference_no}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 730, f"Transaction Date: {self.transaction_date}")
        pdf.drawString(100, 710, f"Customer: {self.customer_id.name}")

        # Create a list to store data for the penjualan line table
        table_data = [
            ["Item", "Quantity", "Price", "Subtotal"]
        ]

        # Add penjualan line details to the table data
        for line in self.penjualan_line:
            table_data.append([line.nama_sepatu.nama_sepatu, line.qty, line.harga, line.subtotal])

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
        table.wrapOn(pdf, 400, 600)
        table.drawOn(pdf, 100, 650)

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
            'name': f'Penjualan_Report_{self.reference_no}.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'store_fname': f'Penjualan_Report_{self.reference_no}.pdf',
            'res_model': self._name,
            'res_id': self.id,
        })

        # Update the 'pdf_report' field with the attachment ID
        self.write({'pdf_report': base64.b64encode(pdf_content)})

        # Construct the URL for the attachment
        return {
            'name': _('Penjualan PDF Report'),
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'new',
        }
    
class ABCPenjualanLine(models.Model):
    _name = 'abc.penjualan.line'
    _description = 'Penjualan Sepatu Line'
    
    penjualan_header_id = fields.Many2one('abc.penjualan.header', string='ID Penjualan', ondelete='cascade')
    nama_sepatu = fields.Many2one('abc.sepatu', string='Nama Sepatu')
    qty = fields.Integer(string='Quantity')
    harga = fields.Float(string='Harga', compute='_compute_harga', store=True)
    subtotal = fields.Float(compute='_compute_subtotal', string='Subtotal', store=True)

    @api.depends('qty', 'nama_sepatu')
    def _compute_harga(self):
        for record in self:
            if record.nama_sepatu:
                record.harga = record.nama_sepatu.harga_sepatu or 0

    @api.depends('qty', 'harga')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.qty * record.harga

    @api.constrains('qty')
    def _checkQuantity(self):
        for record in self:
            if record.qty < 1:
                raise ValidationError(
                    'Stok {} tidak hanya {} pcs. Silahkan melakukan preorder'.format(record.nama_sepatu.nama_sepatu, record.qty)
                )
            elif record.qty > record.nama_sepatu.stok:
                raise ValidationError(
                    'Stok {} tidak mencukupi, maksimal pembelian {} pcs'.format(record.nama_sepatu.nama_sepatu, record.nama_sepatu.stok)
                )
                # Optionally, you can modify the quantity to the available stock
                record.qty = record.nama_sepatu.stok
