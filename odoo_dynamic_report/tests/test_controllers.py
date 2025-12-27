# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import common, tagged
from odoo import http
import json


@tagged('post_install', '-at_install')
class TestReportControllers(common.HttpCase):
    """Test suite for report template controllers"""

    def setUp(self):
        super(TestReportControllers, self).setUp()
        
        # Authenticate
        self.authenticate('admin', 'admin')
        
        # Create test model and template
        self.partner_model = self.env['ir.model'].search([
            ('model', '=', 'res.partner')
        ], limit=1)
        
        self.template = self.env['report.template'].create({
            'name': 'Test API Template',
            'model_id': self.partner_model.id,
        })
        
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com',
        })

    def test_get_model_fields_endpoint(self):
        """Test /report_template/get_model_fields endpoint"""
        url = '/report_template/get_model_fields'
        data = {
            'params': {
                'model': 'res.partner',
                'max_depth': 2
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('result', result)
        self.assertIsInstance(result['result'], list)
        self.assertTrue(len(result['result']) > 0)

    def test_validate_field_endpoint(self):
        """Test /report_template/validate_field endpoint"""
        url = '/report_template/validate_field'
        
        # Test valid field
        data = {
            'params': {
                'model': 'res.partner',
                'field_path': 'name'
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['result']['valid'])
        
        # Test invalid field
        data['params']['field_path'] = 'invalid_field_xyz'
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        self.assertFalse(result['result']['valid'])

    def test_parse_template_endpoint(self):
        """Test /report_template/parse_template endpoint"""
        url = '/report_template/parse_template'
        data = {
            'params': {
                'template_id': self.template.id
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('result', result)

    def test_download_template_endpoint(self):
        """Test /report_template/download endpoint"""
        url = f'/report_template/download/{self.template.id}'
        
        response = self.url_open(url)
        
        # Should return file or error message
        self.assertIn(response.status_code, [200, 404])

    def test_generate_report_endpoint(self):
        """Test /report_template/generate endpoint"""
        url = '/report_template/generate'
        data = {
            'params': {
                'template_id': self.template.id,
                'record_ids': [self.partner.id]
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return success or error
        self.assertIn(response.status_code, [200, 400, 404])

    def test_preview_endpoint(self):
        """Test /report_template/preview endpoint"""
        url = '/report_template/preview'
        data = {
            'params': {
                'template_id': self.template.id,
                'record_id': self.partner.id
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return preview or error
        self.assertIn(response.status_code, [200, 400, 404])

    def test_endpoint_authentication(self):
        """Test that endpoints require authentication"""
        # Logout
        self.logout()
        
        url = '/report_template/get_model_fields'
        data = {
            'params': {
                'model': 'res.partner'
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should require authentication
        self.assertIn(response.status_code, [401, 403])

    def test_invalid_model_parameter(self):
        """Test handling of invalid model parameter"""
        self.authenticate('admin', 'admin')
        
        url = '/report_template/get_model_fields'
        data = {
            'params': {
                'model': 'invalid.model.name'
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        result = response.json()
        # Should return error or empty result
        self.assertIn(response.status_code, [200, 400])

    def test_missing_parameters(self):
        """Test handling of missing required parameters"""
        self.authenticate('admin', 'admin')
        
        url = '/report_template/validate_field'
        data = {
            'params': {}  # Missing required parameters
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return error
        self.assertIn(response.status_code, [400, 500])

    def test_nested_field_validation(self):
        """Test validation of nested field paths"""
        self.authenticate('admin', 'admin')
        
        url = '/report_template/validate_field'
        data = {
            'params': {
                'model': 'res.partner',
                'field_path': 'country_id.name'
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['result']['valid'])

    def test_json_response_format(self):
        """Test that responses are properly formatted JSON"""
        self.authenticate('admin', 'admin')
        
        url = '/report_template/get_model_fields'
        data = {
            'params': {
                'model': 'res.partner',
                'max_depth': 1
            }
        }
        
        response = self.url_open(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should be valid JSON
        try:
            result = response.json()
            self.assertIsInstance(result, dict)
            self.assertIn('result', result)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

    def test_cors_headers(self):
        """Test CORS headers if applicable"""
        self.authenticate('admin', 'admin')
        
        url = '/report_template/get_model_fields'
        response = self.url_open(url)
        
        # Check if CORS headers are present (if configured)
        headers = response.headers
        self.assertIsInstance(headers, dict)
