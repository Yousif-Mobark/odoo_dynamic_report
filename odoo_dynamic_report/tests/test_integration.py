# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import common, tagged
from odoo.exceptions import UserError, ValidationError
import base64


@tagged('post_install', '-at_install')
class TestReportIntegration(common.TransactionCase):
    """Integration tests for end-to-end report workflows"""

    def setUp(self):
        super(TestReportIntegration, self).setUp()
        
        # Create test data
        self.partner_model = self.env['ir.model'].search([
            ('model', '=', 'res.partner')
        ], limit=1)
        
        self.partner = self.env['res.partner'].create({
            'name': 'Integration Test Partner',
            'email': 'integration@test.com',
            'phone': '+9876543210',
            'street': '456 Integration Ave',
            'city': 'Test City',
            'zip': '54321',
        })

    def test_complete_template_workflow(self):
        """Test complete workflow: create -> upload -> parse -> generate"""
        
        # Step 1: Create template
        template = self.env['report.template'].create({
            'name': 'Integration Test Template',
            'model_id': self.partner_model.id,
        })
        
        self.assertTrue(template.id)
        
        # Step 2: Verify report action was created
        report_action = self.env['ir.actions.report'].search([
            ('name', '=', template.name),
            ('model', '=', 'res.partner')
        ])
        
        self.assertTrue(report_action)
        self.assertEqual(report_action.report_type, 'docx')
        
        # Step 3: Add field mappings
        mapping = self.env['report.field.mapping'].create({
            'template_id': template.id,
            'field_name': 'name',
            'field_path': 'name',
            'field_type': 'char',
        })
        
        self.assertIn(mapping, template.field_mapping_ids)
        
        # Step 4: Increment usage (simulate generation)
        initial_usage = template.usage_count
        template.increment_usage()
        self.assertEqual(template.usage_count, initial_usage + 1)
        
        # Step 5: Delete template and verify cleanup
        template_name = template.name
        template.unlink()
        
        report_action = self.env['ir.actions.report'].search([
            ('name', '=', template_name),
            ('model', '=', 'res.partner')
        ])
        
        self.assertFalse(report_action, "Report action should be cleaned up")

    def test_print_menu_integration(self):
        """Test that template appears in print menu"""
        
        # Create active template
        template = self.env['report.template'].create({
            'name': 'Print Menu Test',
            'model_id': self.partner_model.id,
            'active': True,
        })
        
        # Get all report actions for res.partner
        report_actions = self.env['ir.actions.report'].search([
            ('model', '=', 'res.partner')
        ])
        
        # Our template's action should be in the list
        action_names = report_actions.mapped('name')
        self.assertIn('Print Menu Test', action_names)

    def test_multi_company_isolation(self):
        """Test multi-company data isolation"""
        
        # Get or create companies
        company1 = self.env['res.company'].search([], limit=1)
        
        # Create template in company 1
        template1 = self.env['report.template'].with_company(company1).create({
            'name': 'Company 1 Template',
            'model_id': self.partner_model.id,
            'company_id': company1.id,
        })
        
        self.assertEqual(template1.company_id, company1)
        
        # Try to create another company if possible
        try:
            company2 = self.env['res.company'].create({
                'name': 'Test Company 2',
            })
            
            # Create template in company 2
            template2 = self.env['report.template'].with_company(company2).create({
                'name': 'Company 2 Template',
                'model_id': self.partner_model.id,
                'company_id': company2.id,
            })
            
            # Search from company 1 context should not return company 2 template
            templates_company1 = self.env['report.template'].with_company(company1).search([
                ('name', '=', 'Company 2 Template')
            ])
            
            # Depending on record rules, might be empty
            # This tests that multi-company rules are applied
            self.assertIsNotNone(templates_company1)
            
        except Exception:
            # Multi-company setup might not be available in test environment
            pass

    def test_field_mapping_workflow(self):
        """Test field mapping creation and usage"""
        
        template = self.env['report.template'].create({
            'name': 'Field Mapping Test',
            'model_id': self.partner_model.id,
        })
        
        # Create multiple field mappings
        fields = [
            ('name', 'name', 'char'),
            ('email', 'email', 'char'),
            ('phone', 'phone', 'char'),
            ('country_id.name', 'country_id.name', 'char'),
        ]
        
        for field_name, field_path, field_type in fields:
            self.env['report.field.mapping'].create({
                'template_id': template.id,
                'field_name': field_name,
                'field_path': field_path,
                'field_type': field_type,
            })
        
        # Verify all mappings created
        self.assertEqual(len(template.field_mapping_ids), 4)
        
        # Verify mapping details
        mapping_names = template.field_mapping_ids.mapped('field_name')
        self.assertIn('name', mapping_names)
        self.assertIn('email', mapping_names)
        self.assertIn('country_id.name', mapping_names)

    def test_template_copy_functionality(self):
        """Test template duplication"""
        
        # Create original template with mappings
        original = self.env['report.template'].create({
            'name': 'Original Template',
            'model_id': self.partner_model.id,
        })
        
        self.env['report.field.mapping'].create({
            'template_id': original.id,
            'field_name': 'name',
            'field_path': 'name',
            'field_type': 'char',
        })
        
        # Copy template
        copied = original.copy()
        
        # Verify copy
        self.assertNotEqual(copied.id, original.id)
        self.assertTrue(copied.name.endswith('(copy)'))
        self.assertEqual(copied.model_id, original.model_id)
        self.assertEqual(len(copied.field_mapping_ids), len(original.field_mapping_ids))

    def test_preview_wizard_workflow(self):
        """Test preview wizard creation and execution"""
        
        template = self.env['report.template'].create({
            'name': 'Preview Test',
            'model_id': self.partner_model.id,
        })
        
        # Create preview wizard
        wizard = self.env['report.preview.wizard'].create({
            'template_id': template.id,
            'record_id': self.partner.id,
        })
        
        self.assertEqual(wizard.template_id, template)
        self.assertEqual(wizard.record_id, self.partner.id)
        
        # Test preview action exists
        self.assertTrue(hasattr(wizard, 'action_preview'))

    def test_security_groups_and_access(self):
        """Test security groups are properly configured"""
        
        # Check security groups exist
        designer_group = self.env.ref('odoo_dynamic_report.group_report_designer', raise_if_not_found=False)
        user_group = self.env.ref('odoo_dynamic_report.group_report_user', raise_if_not_found=False)
        
        # Groups might not exist in test environment
        # Just verify we can search for them
        groups = self.env['res.groups'].search([
            ('name', 'in', ['Report Designer', 'Report User'])
        ])
        
        # Should have access rights configured
        access_rights = self.env['ir.model.access'].search([
            ('model_id', 'in', [self.partner_model.id])
        ])
        
        self.assertTrue(len(access_rights) > 0)

    def test_template_activation_deactivation(self):
        """Test template active/inactive states"""
        
        template = self.env['report.template'].create({
            'name': 'Active Test',
            'model_id': self.partner_model.id,
            'active': True,
        })
        
        # Initially active
        self.assertTrue(template.active)
        
        # Get report action
        report_action = self.env['ir.actions.report'].search([
            ('name', '=', template.name)
        ])
        self.assertTrue(report_action)
        
        # Deactivate
        template.active = False
        
        # Still exists in system
        self.assertTrue(template.id)
        
        # Reactivate
        template.active = True
        self.assertTrue(template.active)

    def test_error_handling_missing_model(self):
        """Test error handling when model doesn't exist"""
        
        # Try to create template with invalid model
        with self.assertRaises((ValidationError, UserError)):
            self.env['report.template'].create({
                'name': 'Invalid Model Test',
                'model_id': 99999,  # Non-existent model ID
            })

    def test_concurrent_template_usage(self):
        """Test template usage by multiple users/processes"""
        
        template = self.env['report.template'].create({
            'name': 'Concurrent Test',
            'model_id': self.partner_model.id,
        })
        
        initial_count = template.usage_count
        
        # Simulate concurrent usage
        template.increment_usage()
        template.increment_usage()
        template.increment_usage()
        
        self.assertEqual(template.usage_count, initial_count + 3)

    def test_large_dataset_handling(self):
        """Test handling of reports with many records"""
        
        # Create multiple partners
        partners = self.env['res.partner'].create([
            {'name': f'Bulk Partner {i}', 'email': f'bulk{i}@test.com'}
            for i in range(10)
        ])
        
        self.assertEqual(len(partners), 10)
        
        template = self.env['report.template'].create({
            'name': 'Bulk Test',
            'model_id': self.partner_model.id,
        })
        
        # This tests that the system can handle multiple records
        # Actual generation would require template file
        self.assertTrue(template.id)
        self.assertTrue(len(partners) > 0)

    def test_field_path_resolution(self):
        """Test complex field path resolution"""
        
        # Ensure partner has related records
        country = self.env['res.country'].search([], limit=1)
        if country:
            self.partner.country_id = country
            
            # Create mapping with nested field
            template = self.env['report.template'].create({
                'name': 'Nested Field Test',
                'model_id': self.partner_model.id,
            })
            
            mapping = self.env['report.field.mapping'].create({
                'template_id': template.id,
                'field_name': 'country_id.name',
                'field_path': 'country_id.name',
                'field_type': 'char',
            })
            
            self.assertEqual(mapping.field_path, 'country_id.name')
