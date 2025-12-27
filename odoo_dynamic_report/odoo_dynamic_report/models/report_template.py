# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import json
import base64
import logging

_logger = logging.getLogger(__name__)


class ReportTemplate(models.Model):
    _name = 'report.template'
    _description = 'Dynamic Report Template'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Template Name',
        required=True,
        tracking=True,
        help="Name of the report template"
    )
    
    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Odoo model this template is for"
    )
    
    model_name = fields.Char(
        related='model_id.model',
        string='Model Technical Name',
        store=True,
        readonly=True
    )
    
    template_data = fields.Binary(
        string='Template File',
        attachment=True,
        help="Upload your DOCX template file"
    )
    
    template_filename = fields.Char(
        string='Filename',
        help="Name of the uploaded template file"
    )
    
    field_mappings = fields.Text(
        string='Field Mappings',
        help='JSON structure storing field mappings and configurations',
        default='{}'
    )
    
    field_mapping_ids = fields.One2many(
        'report.field.mapping',
        'template_id',
        string='Field Mappings',
        help="Detailed field mapping configurations"
    )
    
    active = fields.Boolean(
        default=True,
        help="Inactive templates won't appear in print menu"
    )
    
    report_action_id = fields.Many2one(
        'ir.actions.report',
        string='Report Action',
        readonly=True,
        ondelete='cascade',
        help="Linked report action for print menu"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this template belongs to"
    )
    
    description = fields.Text(
        string='Description',
        help="Description of what this template is used for"
    )
    
    paper_format_id = fields.Many2one(
        'report.paperformat',
        string='Paper Format',
        help="Paper format for this report"
    )
    
    # Statistics
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        readonly=True,
        help="Number of times this template has been used"
    )
    
    last_used_date = fields.Datetime(
        string='Last Used',
        readonly=True,
        help="Last time this template was used"
    )

    @api.constrains('template_data')
    def _check_template_data(self):
        """Validate that uploaded file is a valid DOCX"""
        for record in self:
            if record.template_data:
                try:
                    # Try to parse the template
                    self.env['report.docx.generator']._validate_template(record.template_data)
                except Exception as e:
                    raise ValidationError(
                        _("Invalid DOCX template file: %s") % str(e)
                    )

    @api.model
    def create(self, vals):
        """Create template and associated report action"""
        record = super(ReportTemplate, self).create(vals)
        record._create_report_action()
        return record

    def write(self, vals):
        """Update template and report action if needed"""
        res = super(ReportTemplate, self).write(vals)
        if 'name' in vals or 'model_id' in vals or 'active' in vals:
            self._update_report_action()
        return res

    def unlink(self):
        """Delete associated report actions before deleting template"""
        self.mapped('report_action_id').unlink()
        return super(ReportTemplate, self).unlink()

    def _create_report_action(self):
        """Create ir.actions.report for this template"""
        self.ensure_one()
        
        if self.report_action_id:
            return self.report_action_id
        
        report_action = self.env['ir.actions.report'].create({
            'name': self.name,
            'model': self.model_name,
            'report_type': 'docx',
            'report_name': f'dynamic_report.template_{self.id}',
            'binding_model_id': self.model_id.id,
            'binding_type': 'report',
            'paperformat_id': self.paper_format_id.id if self.paper_format_id else False,
        })
        
        self.report_action_id = report_action
        _logger.info(f"Created report action {report_action.id} for template {self.name}")
        
        return report_action

    def _update_report_action(self):
        """Update existing report action when template changes"""
        for record in self:
            if record.report_action_id:
                record.report_action_id.write({
                    'name': record.name,
                    'model': record.model_name,
                    'binding_model_id': record.model_id.id,
                    'active': record.active,
                })
                _logger.info(f"Updated report action for template {record.name}")

    def action_preview(self):
        """Open preview wizard"""
        self.ensure_one()
        return {
            'name': _('Preview Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'report.preview.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_template_id': self.id,
                'default_model_id': self.model_id.id,
            }
        }

    def action_download_template(self):
        """Download the template file"""
        self.ensure_one()
        
        if not self.template_data:
            raise UserError(_("No template file uploaded yet."))
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/report.template/{self.id}/template_data/{self.template_filename}?download=true',
            'target': 'self',
        }

    def action_parse_template(self):
        """Parse template and extract placeholders"""
        self.ensure_one()
        
        if not self.template_data:
            raise UserError(_("Please upload a template file first."))
        
        # Parse template to find all placeholders
        parser = self.env['report.docx.generator']
        placeholders = parser._extract_placeholders(self.template_data)
        
        # Create or update field mappings
        self._sync_field_mappings(placeholders)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Template Parsed'),
                'message': _('Found %s field placeholders in template.') % len(placeholders),
                'type': 'success',
                'sticky': False,
            }
        }

    def _sync_field_mappings(self, placeholders):
        """Sync field mappings with discovered placeholders"""
        self.ensure_one()
        
        existing_mappings = {m.field_path: m for m in self.field_mapping_ids}
        
        for placeholder in placeholders:
            if placeholder not in existing_mappings:
                # Create new mapping
                self.env['report.field.mapping'].create({
                    'template_id': self.id,
                    'field_path': placeholder,
                    'field_name': placeholder.split('.')[-1],
                })

    def increment_usage(self):
        """Increment usage counter"""
        self.write({
            'usage_count': self.usage_count + 1,
            'last_used_date': fields.Datetime.now(),
        })

    def get_field_mappings_dict(self):
        """Return field mappings as dictionary"""
        self.ensure_one()
        
        try:
            return json.loads(self.field_mappings) if self.field_mappings else {}
        except json.JSONDecodeError:
            return {}

    def set_field_mappings_dict(self, mappings_dict):
        """Set field mappings from dictionary"""
        self.ensure_one()
        self.field_mappings = json.dumps(mappings_dict)
