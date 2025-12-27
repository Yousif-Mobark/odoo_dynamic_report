# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import common, tagged
from odoo.exceptions import ValidationError, UserError


@tagged('post_install', '-at_install')
class TestReportTemplate(common.TransactionCase):
    """Test suite for report.template model"""

    def setUp(self):
        super(TestReportTemplate, self).setUp()
        
        # Create test model reference
        self.partner_model = self.env['ir.model'].search([
            ('model', '=', 'res.partner')
        ], limit=1)
        
        # Create test template
        self.template = self.env['report.template'].create({
            'name': 'Test Contact Report',
            'model_id': self.partner_model.id,
            'active': True,
        })

    def test_template_creation(self):
        """Test basic template creation"""
        self.assertTrue(self.template.id)
        self.assertEqual(self.template.name, 'Test Contact Report')
        self.assertEqual(self.template.model_id.id, self.partner_model.id)
        self.assertTrue(self.template.active)

    def test_template_name_required(self):
        """Test that template name is required"""
        with self.assertRaises(ValidationError):
            self.env['report.template'].create({
                'model_id': self.partner_model.id,
            })

    def test_template_model_required(self):
        """Test that model selection is required"""
        with self.assertRaises(ValidationError):
            self.env['report.template'].create({
                'name': 'Test Template',
            })

    def test_report_action_creation(self):
        """Test automatic report action creation on template save"""
        # Check if report action was created
        report_action = self.env['ir.actions.report'].search([
            ('name', '=', self.template.name),
            ('model', '=', self.template.model_id.model)
        ])
        self.assertTrue(report_action, "Report action should be auto-created")
        self.assertEqual(report_action.report_type, 'docx')

    def test_report_action_cleanup(self):
        """Test report action cleanup on template deletion"""
        template_name = self.template.name
        model_name = self.template.model_id.model
        
        # Delete template
        self.template.unlink()
        
        # Check if report action was removed
        report_action = self.env['ir.actions.report'].search([
            ('name', '=', template_name),
            ('model', '=', model_name)
        ])
        self.assertFalse(report_action, "Report action should be removed with template")

    def test_usage_increment(self):
        """Test usage counter increment"""
        initial_usage = self.template.usage_count
        self.template.increment_usage()
        self.assertEqual(self.template.usage_count, initial_usage + 1)

    def test_template_file_attachment(self):
        """Test template file upload and storage"""
        # Simulate file upload
        import base64
        test_content = b"Test DOCX content"
        encoded_content = base64.b64encode(test_content)
        
        self.template.write({
            'template_file': encoded_content,
            'template_filename': 'test_template.docx'
        })
        
        self.assertTrue(self.template.template_file)
        self.assertEqual(self.template.template_filename, 'test_template.docx')

    def test_parse_template_action(self):
        """Test parse template action"""
        # This would require actual DOCX content with placeholders
        # For now, test that the method exists and is callable
        self.assertTrue(hasattr(self.template, 'action_parse_template'))
        
    def test_download_template_action(self):
        """Test download template action"""
        self.assertTrue(hasattr(self.template, 'action_download_template'))

    def test_multi_company_support(self):
        """Test multi-company field existence"""
        self.assertTrue(hasattr(self.template, 'company_id'))

    def test_template_copy(self):
        """Test template duplication"""
        copied_template = self.template.copy()
        self.assertTrue(copied_template.id)
        self.assertNotEqual(copied_template.id, self.template.id)
        self.assertTrue(copied_template.name.endswith('(copy)'))

    def test_field_mappings_relationship(self):
        """Test relationship with field mappings"""
        # Create field mapping
        mapping = self.env['report.field.mapping'].create({
            'template_id': self.template.id,
            'field_name': 'name',
            'field_path': 'name',
            'field_type': 'char',
        })
        
        self.assertIn(mapping, self.template.field_mapping_ids)
        self.assertEqual(mapping.template_id, self.template)


@tagged('post_install', '-at_install')
class TestReportFieldMapping(common.TransactionCase):
    """Test suite for report.field.mapping model"""

    def setUp(self):
        super(TestReportFieldMapping, self).setUp()
        
        # Create test template
        partner_model = self.env['ir.model'].search([
            ('model', '=', 'res.partner')
        ], limit=1)
        
        self.template = self.env['report.template'].create({
            'name': 'Test Template',
            'model_id': partner_model.id,
        })

    def test_field_mapping_creation(self):
        """Test basic field mapping creation"""
        mapping = self.env['report.field.mapping'].create({
            'template_id': self.template.id,
            'field_name': 'name',
            'field_path': 'name',
            'field_type': 'char',
        })
        
        self.assertTrue(mapping.id)
        self.assertEqual(mapping.field_name, 'name')
        self.assertEqual(mapping.field_path, 'name')

    def test_nested_field_path(self):
        """Test nested field path validation"""
        mapping = self.env['report.field.mapping'].create({
            'template_id': self.template.id,
            'field_name': 'partner_id.name',
            'field_path': 'partner_id.name',
            'field_type': 'char',
        })
        
        self.assertEqual(mapping.field_path, 'partner_id.name')

    def test_field_formatting(self):
        """Test field formatting options"""
        mapping = self.env['report.field.mapping'].create({
            'template_id': self.template.id,
            'field_name': 'create_date',
            'field_path': 'create_date',
            'field_type': 'datetime',
            'formatting': "date:'%Y-%m-%d'",
        })
        
        self.assertEqual(mapping.formatting, "date:'%Y-%m-%d'")

    def test_default_value(self):
        """Test default value assignment"""
        mapping = self.env['report.field.mapping'].create({
            'template_id': self.template.id,
            'field_name': 'optional_field',
            'field_path': 'optional_field',
            'field_type': 'char',
            'default_value': 'N/A',
        })
        
        self.assertEqual(mapping.default_value, 'N/A')
