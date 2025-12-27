# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Dynamic Report Builder',
    'version': '18.0.1.0.0',
    'category': 'Reporting',
    'summary': 'Design custom DOCX reports with drag-and-drop interface',
    'description': """
        Dynamic Report Builder for Odoo 18
        ===================================
        
        Create professional reports without programming!
        
        Key Features:
        * Visual DOCX template designer
        * Drag and drop fields from any Odoo model
        * Support for nested and related fields
        * Automatic integration with print menu
        * Live preview functionality
        * Multi-company support
        * Easy-to-use interface for non-technical users
        
        Perfect for:
        * Custom invoices and quotations
        * Sales and purchase reports
        * Contact sheets and labels
        * Any custom document generation needs
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
    ],
    'external_dependencies': {
        'python': [
            'docx',
            'lxml',
        ],
    },
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/report_paperformat.xml',
        'data/default_templates.xml',
        
        # Views
        'views/report_template_views.xml',
        'views/menu_views.xml',
        
        # Wizard
        'wizard/report_preview_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_dynamic_report/static/src/js/template_designer.js',
            'odoo_dynamic_report/static/src/js/field_selector.js',
            'odoo_dynamic_report/static/src/css/template_designer.css',
            'odoo_dynamic_report/static/src/xml/template_designer.xml',
            'odoo_dynamic_report/static/src/xml/field_selector.xml',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': '_post_init_hook',
}
