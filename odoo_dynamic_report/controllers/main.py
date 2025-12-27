# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)


class ReportTemplateController(http.Controller):

    @http.route('/report_template/get_model_fields', type='json', auth='user')
    def get_model_fields(self, model_name, include_related=True, max_depth=2):
        """Get all fields for a given model"""
        try:
            parser = request.env['report.parser']
            fields = parser.get_available_fields(model_name, include_related, max_depth)
            
            return {
                'success': True,
                'fields': fields
            }
        except Exception as e:
            _logger.exception("Error getting model fields")
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/report_template/validate_field', type='json', auth='user')
    def validate_field(self, model_name, field_path):
        """Validate a field path"""
        try:
            parser = request.env['report.parser']
            result = parser.validate_field_path(model_name, field_path)
            
            return {
                'success': True,
                **result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/report_template/parse_template', type='json', auth='user')
    def parse_template(self, template_id):
        """Parse template and return placeholder information"""
        try:
            template = request.env['report.template'].browse(int(template_id))
            
            if not template.exists() or not template.template_data:
                return {
                    'success': False,
                    'error': 'Template not found or has no data'
                }
            
            parser = request.env['report.parser']
            result = parser.parse_template(template.template_data)
            
            return {
                'success': True,
                **result
            }
        except Exception as e:
            _logger.exception("Error parsing template")
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/report_template/preview', type='http', auth='user')
    def preview_template(self, template_id, record_id=None, **kwargs):
        """Generate preview of template"""
        try:
            template = request.env['report.template'].browse(int(template_id))
            
            if not template.exists():
                return request.not_found()
            
            # Get sample record
            if record_id:
                record_ids = [int(record_id)]
            else:
                # Get first available record
                model = request.env[template.model_name]
                sample_record = model.search([], limit=1)
                if not sample_record:
                    return Response(
                        json.dumps({'error': 'No records found'}),
                        content_type='application/json',
                        status=404
                    )
                record_ids = [sample_record.id]
            
            # Generate report
            generator = request.env['report.docx.generator']
            docx_content = generator.generate_report(template, record_ids)
            
            # Return as download
            filename = f"{template.name}_preview.docx"
            return request.make_response(
                docx_content,
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                    ('Content-Disposition', f'attachment; filename="{filename}"')
                ]
            )
            
        except Exception as e:
            _logger.exception("Error generating preview")
            return Response(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )

    @http.route('/report_template/download/<int:template_id>', type='http', auth='user')
    def download_template(self, template_id, **kwargs):
        """Download the template file"""
        try:
            template = request.env['report.template'].browse(template_id)
            
            if not template.exists() or not template.template_data:
                return request.not_found()
            
            import base64
            template_data = base64.b64decode(template.template_data)
            filename = template.template_filename or f"{template.name}.docx"
            
            return request.make_response(
                template_data,
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                    ('Content-Disposition', f'attachment; filename="{filename}"')
                ]
            )
            
        except Exception as e:
            _logger.exception("Error downloading template")
            return request.not_found()

    @http.route('/report_template/generate', type='http', auth='user')
    def generate_report(self, template_id, record_ids, **kwargs):
        """Generate report for specific records"""
        try:
            template = request.env['report.template'].browse(int(template_id))
            
            if not template.exists():
                return request.not_found()
            
            # Parse record IDs
            if isinstance(record_ids, str):
                record_ids = [int(rid) for rid in record_ids.split(',')]
            elif not isinstance(record_ids, list):
                record_ids = [int(record_ids)]
            
            # Generate report
            generator = request.env['report.docx.generator']
            docx_content = generator.generate_report(template, record_ids)
            
            # Increment usage
            template.increment_usage()
            
            # Return as download
            filename = f"{template.name}.docx"
            return request.make_response(
                docx_content,
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                    ('Content-Disposition', f'attachment; filename="{filename}"')
                ]
            )
            
        except Exception as e:
            _logger.exception("Error generating report")
            return Response(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )
