# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ReportFieldMapping(models.Model):
    _name = 'report.field.mapping'
    _description = 'Report Field Mapping'
    _order = 'sequence, field_name'

    template_id = fields.Many2one(
        'report.template',
        string='Template',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    field_name = fields.Char(
        string='Field Name',
        required=True,
        help="Display name of the field"
    )
    
    field_path = fields.Char(
        string='Field Path',
        required=True,
        help="Full path to the field (e.g., partner_id.name)"
    )
    
    field_type = fields.Selection([
        ('char', 'Text'),
        ('text', 'Multiline Text'),
        ('integer', 'Integer'),
        ('float', 'Decimal'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('many2one', 'Many2One'),
        ('one2many', 'One2Many'),
        ('many2many', 'Many2Many'),
        ('binary', 'Binary/Image'),
        ('selection', 'Selection'),
        ('monetary', 'Monetary'),
        ('html', 'HTML'),
    ], string='Field Type', help="Type of the field")
    
    format_string = fields.Char(
        string='Format',
        help="Custom format string (e.g., for dates: %%Y-%%m-%%d)"
    )
    
    default_value = fields.Char(
        string='Default Value',
        help="Default value if field is empty"
    )
    
    is_required = fields.Boolean(
        string='Required',
        default=False,
        help="Show error if this field is empty"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of field processing"
    )
    
    placeholder = fields.Char(
        string='Placeholder',
        compute='_compute_placeholder',
        help="Placeholder text in template"
    )
    
    position_info = fields.Text(
        string='Position Info',
        help="JSON data about position in document"
    )
    
    description = fields.Text(
        string='Description',
        help="Additional notes about this field"
    )

    @api.depends('field_path')
    def _compute_placeholder(self):
        """Generate placeholder syntax"""
        for record in self:
            record.placeholder = f'{{{{{record.field_path}}}}}' if record.field_path else ''

    @api.constrains('field_path', 'template_id')
    def _check_field_path(self):
        """Validate that field path exists on the model"""
        for record in self:
            if record.field_path and record.template_id.model_name:
                try:
                    model = self.env[record.template_id.model_name]
                    # Validate field path exists
                    self._validate_field_path(model, record.field_path)
                except Exception as e:
                    raise ValidationError(
                        _("Invalid field path '%s' for model '%s': %s") % 
                        (record.field_path, record.template_id.model_name, str(e))
                    )

    def _validate_field_path(self, model, field_path):
        """Recursively validate a field path"""
        parts = field_path.split('.', 1)
        field_name = parts[0]
        
        if field_name not in model._fields:
            raise ValidationError(_("Field '%s' does not exist on model '%s'") % (field_name, model._name))
        
        field = model._fields[field_name]
        
        # If there are more parts, validate recursively
        if len(parts) > 1:
            if field.type in ('many2one', 'one2many', 'many2many'):
                related_model = self.env[field.comodel_name]
                self._validate_field_path(related_model, parts[1])
            else:
                raise ValidationError(
                    _("Cannot traverse field '%s' - it's not a relational field") % field_name
                )

    def action_test_field(self):
        """Test field with sample data"""
        self.ensure_one()
        
        # Get a sample record
        model = self.env[self.template_id.model_name]
        sample_record = model.search([], limit=1)
        
        if not sample_record:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No Data'),
                    'message': _('No records found in model %s') % self.template_id.model_name,
                    'type': 'warning',
                }
            }
        
        # Get field value
        try:
            value = self._get_field_value(sample_record, self.field_path)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Sample Value'),
                    'message': _('Field: %s\nValue: %s') % (self.field_path, value),
                    'type': 'success',
                    'sticky': True,
                }
            }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Error'),
                    'message': str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }

    def _get_field_value(self, record, field_path):
        """Get value from record using field path"""
        parts = field_path.split('.', 1)
        field_name = parts[0]
        
        if not hasattr(record, field_name):
            return self.default_value or ''
        
        value = getattr(record, field_name)
        
        # If there are more parts, traverse
        if len(parts) > 1 and value:
            if isinstance(value, models.BaseModel):
                if len(value) == 1:
                    return self._get_field_value(value, parts[1])
                else:
                    # Multiple records - return comma-separated
                    return ', '.join([
                        str(self._get_field_value(rec, parts[1]))
                        for rec in value
                    ])
        
        # Format value
        if value is False:
            return self.default_value or ''
        elif isinstance(value, models.BaseModel):
            return value.display_name
        elif isinstance(value, (list, tuple)):
            return ', '.join(str(v) for v in value)
        else:
            return str(value)
