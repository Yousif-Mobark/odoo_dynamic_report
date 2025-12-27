# Odoo Dynamic Report Builder

## Overview

The **Dynamic Report Builder** is a powerful Odoo 18 module that enables users to design custom DOCX reports without any programming knowledge. With an intuitive drag-and-drop interface, users can create professional documents by selecting fields from any Odoo model and placing them in a Word document template.

## Features

### 🎨 Visual Designer
- Drag and drop interface for field selection
- Real-time template preview
- Easy-to-use DOCX editor
- Support for tables, images, and complex layouts

### 🔗 Field Integration
- Access fields from any Odoo model
- Support for nested fields (e.g., `partner_id.name`)
- Handle related records (many2one, one2many, many2many)
- Computed field support
- Date, number, and currency formatting

### 📄 Template Management
- Upload custom DOCX templates
- Save and reuse templates
- Template versioning
- Share templates across companies

### 🖨️ Print Integration
- Automatic integration with Odoo's print menu
- Batch printing support
- Multi-record reports
- PDF export option

### 🔒 Security
- Role-based access control
- Multi-company support
- Record rules for data isolation
- Secure template storage

## Installation

### Prerequisites

1. **Odoo 18** must be installed and running
2. **Python 3.10+** is required
3. Required Python packages:
   ```bash
   pip install python-docx
   pip install lxml
   pip install Pillow
   ```

### Installation Steps

1. Clone or download this module to your Odoo addons directory:
   ```bash
   cd /path/to/odoo/addons
   git clone <repository-url> odoo_dynamic_report
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the Odoo apps list:
   - Go to Apps menu
   - Click "Update Apps List"
   - Search for "Dynamic Report Builder"

4. Install the module:
   - Click "Install" button

## Usage

### Creating Your First Report Template

1. **Navigate to Reports**
   - Go to: Settings → Technical → Reports → Dynamic Report Templates
   - Or use the main menu: Reports → Report Templates

2. **Create New Template**
   - Click "Create" button
   - Enter a name for your template
   - Select the Odoo model (e.g., Sale Order, Invoice, Partner)

3. **Upload Base Template**
   - Prepare a DOCX file with your desired layout
   - Click "Upload Template" and select your file
   - Or use the built-in designer to create from scratch

4. **Add Fields**
   - Open the field selector panel
   - Browse available fields for your selected model
   - Drag fields into your document
   - Fields are inserted as placeholders: `{{field_name}}`

5. **Format Your Template**
   - Style text, tables, and images as needed
   - Use Word's formatting tools
   - Preview with sample data

6. **Save and Test**
   - Click "Save" to store your template
   - Use "Preview" to test with real data
   - The template automatically appears in the print menu

### Using Template Placeholders

#### Simple Fields
```
{{name}}
{{email}}
{{phone}}
```

#### Related Fields
```
{{partner_id.name}}
{{partner_id.country_id.name}}
{{user_id.email}}
```

#### Many2one Fields
```
{{order_id.name}}
{{invoice_id.partner_id.name}}
```

#### Date Formatting
```
{{date_order|date:'%Y-%m-%d'}}
{{create_date|date:'%B %d, %Y'}}
```

#### Number Formatting
```
{{amount_total|number:'0.2f'}}
{{quantity|number:'0.0f'}}
```

#### Tables and Lists (One2many)
```
For order lines, create a table in Word and use:
{{#order_line}}
    {{product_id.name}} | {{quantity}} | {{price_unit}}
{{/order_line}}
```

### Printing Reports

1. **From Form View**
   - Open any record (e.g., Sales Order)
   - Click the "Print" button
   - Select your custom template from the dropdown
   - Download the generated DOCX or PDF

2. **Batch Printing**
   - Select multiple records in list view
   - Click "Print" in the action menu
   - Choose your template
   - Download combined report

## Configuration

### Security Groups

The module provides two security groups:

1. **Report User** (base.group_user)
   - Can view and use existing templates
   - Can generate reports
   - Cannot create or modify templates

2. **Report Designer** (base.group_system)
   - Full access to create, modify, and delete templates
   - Can configure field mappings
   - Manage template library

### Settings

Configure module settings at: Settings → Technical → Reports → Configuration

- Default paper format
- Template storage location
- Preview record limits
- Cache settings

## Advanced Features

### Custom Field Formatters

Create custom formatters for special field types:

```python
# In your custom module
from odoo import models

class ReportTemplate(models.Model):
    _inherit = 'report.template'
    
    def _format_field_custom(self, value, format_string):
        # Your custom formatting logic
        return formatted_value
```

### Template Inheritance

Extend base templates:

```xml
<record id="custom_invoice_template" model="report.template">
    <field name="name">Custom Invoice</field>
    <field name="parent_template_id" ref="base_invoice_template"/>
    <field name="model_id" ref="account.model_account_move"/>
</record>
```

## Troubleshooting

### Common Issues

**Issue**: Template upload fails
- **Solution**: Ensure the file is a valid DOCX format (not DOC or RTF)
- Check file size is under 10MB

**Issue**: Fields not rendering
- **Solution**: Verify field names match exactly
- Check field access permissions
- Ensure the field exists on the selected model

**Issue**: Preview not working
- **Solution**: Ensure python-docx is installed
- Check Odoo logs for errors
- Verify model has accessible records

**Issue**: Generated report is empty
- **Solution**: Check placeholder syntax is correct
- Verify the record has data in those fields
- Check field access rights

### Debug Mode

Enable debug logging:

```python
# In odoo.conf
log_handler = odoo.addons.odoo_dynamic_report:DEBUG
```

View logs:
```bash
tail -f /var/log/odoo/odoo.log | grep odoo_dynamic_report
```

## Development

### Project Structure

```
odoo_dynamic_report/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── report_template.py
│   ├── report_field_mapping.py
│   └── ir_actions_report.py
├── views/
│   ├── report_template_views.xml
│   └── menu_views.xml
├── controllers/
│   ├── __init__.py
│   └── main.py
├── report/
│   ├── __init__.py
│   ├── report_docx_generator.py
│   └── report_parser.py
├── wizard/
│   ├── __init__.py
│   └── report_preview_wizard.py
├── static/
│   ├── description/
│   ├── src/
│   │   ├── js/
│   │   ├── css/
│   │   └── xml/
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── data/
    └── report_paperformat.xml
```

### Running Tests

```bash
odoo-bin -c odoo.conf -u odoo_dynamic_report --test-enable --log-level=test
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## Support

- **Documentation**: [Link to full documentation]
- **Issues**: [GitHub Issues]
- **Community**: [Forum or mailing list]
- **Email**: support@yourcompany.com

## License

This module is licensed under LGPL-3. See LICENSE file for details.

## Credits

- **Author**: Your Company
- **Maintainer**: Your Company
- **Contributors**: [List of contributors]

## Changelog

### Version 18.0.1.0.0 (2025-12-28)
- Initial release
- Visual template designer
- Drag-and-drop field selector
- DOCX generation engine
- Print menu integration
- Multi-company support

---

**Made with ❤️ for the Odoo Community**
