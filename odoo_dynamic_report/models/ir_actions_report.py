# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        """Override to handle DOCX reports"""
        report_sudo = self._get_report(report_ref)
        
        # Check if this is a dynamic DOCX template report
        if report_sudo.report_type == 'docx':
            return self._render_docx_template(report_sudo, res_ids, data)
        
        return super()._render_qweb_pdf(report_ref, res_ids, data)

    def _render_docx_template(self, report_sudo, res_ids, data=None):
        """Render DOCX reports using dynamic templates"""
        # Find the template linked to this report action
        template = self.env['report.template'].search([
            ('report_action_id', '=', report_sudo.id)
        ], limit=1)
        
        if not template:
            raise UserError(
                _("No template found for report %s") % report_sudo.name
            )
        
        if not template.template_data:
            raise UserError(
                _("Template '%s' has no template file uploaded") % template.name
            )
        
        _logger.info(
            f"Rendering DOCX report for template {template.name} "
            f"with {len(res_ids)} records"
        )
        
        # Increment usage counter
        template.increment_usage()
        
        # Generate the DOCX
        docx_generator = self.env['report.docx.generator']
        docx_content = docx_generator.generate_report(template, res_ids)
        
        return docx_content, 'docx'

    def _render_docx(self, docids, data=None):
        """Compatibility method for Odoo's report rendering"""
        return self._render_docx_template(self, docids, data)
