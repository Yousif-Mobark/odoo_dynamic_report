# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import common, tagged
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
import tempfile
import os


@tagged('post_install', '-at_install')
class TestReportDocxGenerator(common.TransactionCase):
    """Test suite for DOCX report generator"""

    def setUp(self):
        super(TestReportDocxGenerator, self).setUp()
        self.generator = self.env['report.docx.generator']
        
        # Create test partner
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'street': '123 Test Street',
            'city': 'Test City',
            'zip': '12345',
        })

    def test_simple_field_replacement(self):
        """Test replacement of simple field placeholders"""
        template_content = "Name: {{name}}, Email: {{email}}"
        
        result = self.generator._replace_placeholders(
            template_content,
            self.partner
        )
        
        self.assertIn('Test Partner', result)
        self.assertIn('test@example.com', result)

    def test_nested_field_replacement(self):
        """Test replacement of nested field placeholders"""
        # Ensure partner has country
        country = self.env['res.country'].search([], limit=1)
        if country:
            self.partner.country_id = country
            
            template_content = "Country: {{country_id.name}}"
            result = self.generator._replace_placeholders(
                template_content,
                self.partner
            )
            
            self.assertIn(country.name, result)

    def test_missing_field_handling(self):
        """Test handling of missing/empty fields"""
        template_content = "Mobile: {{mobile}}"
        
        result = self.generator._replace_placeholders(
            template_content,
            self.partner
        )
        
        # Should handle gracefully (empty string or default)
        self.assertIsNotNone(result)

    def test_date_formatting(self):
        """Test date field formatting"""
        # Set a known date
        test_date = datetime(2025, 12, 28, 10, 30, 0)
        self.partner.write({'create_date': test_date})
        
        template_content = "Date: {{create_date|date:'%Y-%m-%d'}}"
        
        result = self.generator._format_value(
            test_date,
            'datetime',
            "date:'%Y-%m-%d'"
        )
        
        self.assertEqual(result, '2025-12-28')

    def test_number_formatting(self):
        """Test number field formatting"""
        # Test with decimal formatting
        value = 1234.567
        
        result = self.generator._format_value(
            value,
            'float',
            "number:',.2f'"
        )
        
        self.assertIn('1,234.57', result)

    def test_text_formatter_upper(self):
        """Test text uppercase formatter"""
        value = "test string"
        
        result = self.generator._format_value(
            value,
            'char',
            'upper'
        )
        
        self.assertEqual(result, 'TEST STRING')

    def test_text_formatter_lower(self):
        """Test text lowercase formatter"""
        value = "TEST STRING"
        
        result = self.generator._format_value(
            value,
            'char',
            'lower'
        )
        
        self.assertEqual(result, 'test string')

    def test_text_formatter_title(self):
        """Test text title case formatter"""
        value = "test string here"
        
        result = self.generator._format_value(
            value,
            'char',
            'title'
        )
        
        self.assertEqual(result, 'Test String Here')

    def test_boolean_field_formatting(self):
        """Test boolean field representation"""
        result_true = self.generator._format_value(True, 'boolean', None)
        result_false = self.generator._format_value(False, 'boolean', None)
        
        self.assertIn('Yes', str(result_true).title())
        self.assertIn('No', str(result_false).title())

    def test_many2one_field_value_retrieval(self):
        """Test value retrieval for many2one fields"""
        # Create country relationship
        country = self.env['res.country'].search([], limit=1)
        if country:
            self.partner.country_id = country
            
            value = self.generator._get_field_value(
                self.partner,
                'country_id.name'
            )
            
            self.assertEqual(value, country.name)

    def test_invalid_field_path_error(self):
        """Test error handling for invalid field paths"""
        with self.assertRaises((AttributeError, ValidationError, UserError)):
            self.generator._get_field_value(
                self.partner,
                'invalid_field_xyz.name'
            )

    def test_placeholder_extraction_regex(self):
        """Test placeholder extraction from template"""
        template_text = "Hello {{name}}, your email is {{email}}!"
        
        placeholders = self.generator._extract_placeholders(template_text)
        
        self.assertIn('name', placeholders)
        self.assertIn('email', placeholders)
        self.assertEqual(len(placeholders), 2)

    def test_formatted_placeholder_extraction(self):
        """Test extraction of placeholders with formatters"""
        template_text = "Date: {{create_date|date:'%Y-%m-%d'}}"
        
        placeholders = self.generator._extract_placeholders(template_text)
        
        # Should extract the base field name
        self.assertTrue(any('create_date' in p for p in placeholders))

    def test_table_loop_detection(self):
        """Test detection of table loop markers"""
        template_text = """
        {{#order_line}}
        Product: {{product_id.name}}
        {{/order_line}}
        """
        
        has_loops = self.generator._has_table_loops(template_text)
        self.assertTrue(has_loops)

    def test_empty_record_handling(self):
        """Test handling of empty/null record"""
        # This should not crash
        try:
            result = self.generator._replace_placeholders(
                "Test {{name}}",
                self.env['res.partner']
            )
            # Should handle gracefully
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Should handle empty record gracefully: {e}")

    def test_special_characters_in_field_values(self):
        """Test handling of special characters in values"""
        self.partner.name = "Test & <Partner> with \"quotes\""
        
        result = self.generator._replace_placeholders(
            "Name: {{name}}",
            self.partner
        )
        
        # Should preserve or properly escape special characters
        self.assertIn('Test', result)

    def test_multiline_field_values(self):
        """Test handling of multiline field values"""
        self.partner.comment = "Line 1\nLine 2\nLine 3"
        
        result = self.generator._replace_placeholders(
            "Comment: {{comment}}",
            self.partner
        )
        
        self.assertIn('Line 1', result)

    def test_image_field_handling(self):
        """Test handling of binary image fields"""
        # Set sample image data
        import base64
        sample_image = base64.b64encode(b"fake image data")
        self.partner.image_1920 = sample_image
        
        # Should not crash when processing image field
        try:
            result = self.generator._get_field_value(
                self.partner,
                'image_1920'
            )
            self.assertIsNotNone(result)
        except Exception as e:
            self.fail(f"Should handle image fields: {e}")

    def test_selection_field_formatting(self):
        """Test formatting of selection field values"""
        # Test with partner type (individual/company)
        self.partner.company_type = 'person'
        
        value = self.generator._get_field_value(
            self.partner,
            'company_type'
        )
        
        # Should return the selection value
        self.assertIsNotNone(value)

    def test_html_field_stripping(self):
        """Test HTML stripping from HTML fields"""
        html_content = "<p>Test <strong>content</strong></p>"
        
        result = self.generator._strip_html(html_content)
        
        self.assertNotIn('<p>', result)
        self.assertNotIn('<strong>', result)
        self.assertIn('Test', result)
        self.assertIn('content', result)
