# -*- coding: utf-8 -*-
{
    'name': "addonsxx/pabrikabc",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'auto_install': False,
    'application': True,
    'installable': True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product', 'report_xlsx',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        # 'report/report_penjualan_pdf.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/sepatu_view.xml',
        'views/bahan_sepatu_view.xml',
        'views/pegawai_kasir_view.xml',
        'views/pegawai_kebersihan_view.xml',
        'views/pegawai_pabrik_view.xml',
        'views/pegawai_pabrik_inherit_view.xml',
        'views/pembelian_bahan_sepatu_view.xml',
        'views/supplier_view.xml',
        'views/penjualan_sepatu.xml',
        'views/customer_view.xml',
        # 'report/report_sepatu_xlsx.xml',
        

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
