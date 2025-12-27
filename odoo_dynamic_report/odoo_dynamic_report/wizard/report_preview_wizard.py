# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ReportPreviewWizard(models.TransientModel):
    _name = 'report.preview.wizard'
    _description = 'Report Preview Wizard'

    template_id = fields.Many2one(
        'report.template',
        string='Template',
        required=True,
        readonly=True
    )
    
    model_id = fields.Many2one(
        'ir.model',
        related='template_id.model_id',
        string='Model',
        readonly=True
    )
    
    record_id = fields.Many2oneReference(
        string='Sample Record',
        model_field='model_name',
        help="Select a record to preview the template"
    )
    
    model_name = fields.Char(
        related='template_id.model_name',
        string='Model Name',
        readonly=True
    )

    def action_preview(self):
        """Generate and download preview"""
        self.ensure_one()
        
        if not self.record_id:
            raise UserError(_("Please select a record to preview"))
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report_template/preview?template_id={self.template_id.id}&record_id={self.record_id}',
            'target': 'self',
        }

    def action_preview_first(self):
        """Preview with first available record"""
        self.ensure_one()
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report_template/preview?template_id={self.template_id.id}',
            'target': 'self',
        }
