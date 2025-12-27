# Quick Installation Guide - Odoo Dynamic Report Builder

## Prerequisites

- Odoo 18 installed and running
- Python 3.10+
- pip package manager

## Installation Steps

### 1. Install Python Dependencies

```bash
cd /home/hp/odoo_report/odoo_dynamic_report/odoo_dynamic_report/odoo_dynamic_report
pip install -r requirements.txt
```

Or install individually:
```bash
pip install python-docx>=0.8.11
pip install lxml>=4.9.0
pip install Pillow>=10.0.0
```

### 2. Copy Module to Odoo Addons

```bash
# Option A: Symlink (recommended for development)
ln -s /home/hp/odoo_report/odoo_dynamic_report/odoo_dynamic_report/odoo_dynamic_report /path/to/odoo/addons/odoo_dynamic_report

# Option B: Copy
cp -r /home/hp/odoo_report/odoo_dynamic_report/odoo_dynamic_report/odoo_dynamic_report /path/to/odoo/addons/
```

### 3. Update Odoo Apps List

```bash
# Restart Odoo server
sudo systemctl restart odoo

# Or if running manually
./odoo-bin -c odoo.conf -u odoo_dynamic_report --stop-after-init
```

### 4. Install Module via UI

1. Log in to Odoo as Administrator
2. Go to **Apps** menu
3. Remove "Apps" filter from search bar
4. Search for "Dynamic Report Builder"
5. Click **Install**

### 5. Verify Installation

1. Go to **Report Builder** → **Templates**
2. Click **Create** to test template creation
3. Check that all fields are visible

## Quick Test

### Create Your First Report

1. **Navigate to Templates**
   ```
   Report Builder → Templates → Create
   ```

2. **Fill Basic Info**
   - Name: "Partner Contact Sheet"
   - Model: "Contact" (res.partner)

3. **Create Simple DOCX Template**
   
   Create a Word document with this content:
   ```
   Contact Information
   
   Name: {{name}}
   Email: {{email}}
   Phone: {{phone}}
   Address: {{street}}, {{city}}
   Company: {{parent_id.name}}
   ```
   
   Save as `partner_template.docx`

4. **Upload Template**
   - Click "Upload DOCX Template"
   - Select your file
   - Click "Parse Template"
   - Review auto-detected fields

5. **Test Preview**
   - Click "Preview" button
   - Select a contact record
   - Download and verify the generated DOCX

6. **Use in Print Menu**
   - Go to **Contacts** → Open any contact
   - Click **Print** dropdown
   - Select "Partner Contact Sheet"
   - Download the report

## Troubleshooting

### Error: "Import docx could not be resolved"

**Solution:** Install python-docx
```bash
pip install python-docx
```

### Error: "Model 'report.template' does not exist"

**Solution:** Module not installed properly
```bash
# Restart Odoo with update
./odoo-bin -c odoo.conf -u odoo_dynamic_report
```

### Error: "Template file is missing"

**Solution:** Upload a DOCX file in the template form

### Template not appearing in Print menu

**Solution:** 
1. Check template is Active
2. Verify report_action_id is set
3. Restart Odoo

### No records found for preview

**Solution:** Create at least one record in the selected model

## Configuration

### Default Paper Format

Edit in: Settings → Technical → Reporting → Paper Formats
- Look for "Dynamic Report A4"
- Customize margins, orientation, etc.

### Security Groups

Assign users to groups:
1. Go to Settings → Users & Companies → Users
2. Select user
3. Under "Dynamic Reports" tab:
   - **Report Designer**: Can create/edit templates
   - Default users can only use existing templates

## Advanced Configuration

### Custom Formatters

Add custom formatters by inheriting the generator:

```python
# In your custom module
from odoo import models

class CustomReportGenerator(models.AbstractModel):
    _inherit = 'report.docx.generator'
    
    def _format_value(self, value, formatter):
        if formatter == 'phone':
            # Custom phone formatting
            return format_phone_number(value)
        return super()._format_value(value, formatter)
```

### Multi-Company Setup

1. Enable multi-company in Settings
2. Create templates per company
3. Leave company_id blank for shared templates

## Development Mode

For development with live reload:

```bash
# Run Odoo in dev mode
./odoo-bin -c odoo.conf --dev=all -u odoo_dynamic_report
```

## Backup & Migration

### Export Templates

```bash
# Backup template data
./odoo-bin -c odoo.conf --database=mydb --backup=/path/to/backup.zip
```

### Import Templates

Use Odoo's standard import/export feature:
1. Go to Report Templates list view
2. Select templates to export
3. Action → Export
4. Select fields to export

## Support

- Documentation: See README.md
- Development Plan: See DEVELOPMENT_PLAN.md
- Task Tracking: See TASKS.md
- Implementation Status: See IMPLEMENTATION_SUMMARY.md

---

**Installation Time**: ~10 minutes  
**Difficulty**: Easy  
**Ready for Production**: Backend Yes, Frontend Pending
