# 🚀 Quick Start Guide - Odoo Dynamic Report Builder

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

```bash
pip install python-docx lxml Pillow
```

### Step 2: Install Module (1 minute)

1. Copy module to Odoo addons folder
2. Restart Odoo
3. Go to Apps → Update Apps List
4. Search "Dynamic Report Builder"
5. Click Install

### Step 3: Create Your First Report (2 minutes)

#### A. Create Template Record

1. Go to **Report Builder → Templates**
2. Click **Create**
3. Fill in:
   - **Name**: "My First Report"
   - **Model**: "Contact" (res.partner)
4. Click **Save**

#### B. Create DOCX Template

Open Microsoft Word or LibreOffice and create this simple document:

```
CONTACT INFORMATION

Name: {{name}}
Email: {{email}}
Phone: {{phone}}
Address: {{street}}, {{city}}, {{zip}}
Country: {{country_id.name}}

---
Generated on: {{create_date|date:'%Y-%m-%d'}}
```

Save as `contact_template.docx`

#### C. Upload & Test

1. Click **Upload DOCX Template** button
2. Select your `contact_template.docx` file
3. Click **Parse Template** (auto-detects {{placeholders}})
4. Click **Preview** button
5. Select a contact to preview
6. Download and open the generated report!

### Step 4: Use in Odoo

1. Go to **Contacts** menu
2. Open any contact
3. Click **Print** dropdown
4. Select **"My First Report"**
5. Download your custom report! 🎉

---

## 💡 Common Placeholders

### Simple Fields
```
{{name}}              Customer name
{{email}}             Email address
{{phone}}             Phone number
{{street}}            Street address
{{city}}              City
{{zip}}               Postal code
```

### Related Fields
```
{{partner_id.name}}          Partner's name
{{company_id.name}}          Company name
{{user_id.email}}            User's email
{{country_id.name}}          Country name
{{parent_id.name}}           Parent company
```

### Formatted Values
```
{{date_order|date:'%Y-%m-%d'}}           Date as 2025-12-28
{{date_order|date:'%B %d, %Y'}}          Date as December 28, 2025
{{amount_total|number:'0.2f'}}           Number with 2 decimals
{{amount_total|number:',.2f'}}           Number with comma separator
{{name|upper}}                            UPPERCASE TEXT
{{name|lower}}                            lowercase text
{{name|title}}                            Title Case Text
```

### Tables (One2Many Fields)

In a Sales Order template:

```
Order Lines:

{{#order_line}}
  Product: {{product_id.name}}
  Quantity: {{product_uom_qty}}
  Price: {{price_unit}}
  Subtotal: {{price_subtotal}}
{{/order_line}}
```

---

## 🎨 Design Tips

### ✅ Do This
- Design your layout in Word first
- Use simple placeholders: `{{field_name}}`
- Keep formatting in Word, not in placeholders
- Test with Preview before using
- Use tables for line items

### ❌ Avoid This
- Don't use complex formulas in Word
- Don't nest formatting inside placeholders
- Don't use invalid field names
- Don't forget the double curly braces {{}}

---

## 🔥 Popular Use Cases

### 1. Custom Invoice
```
INVOICE #{{name}}

Bill To: {{partner_id.name}}
Address: {{partner_id.street}}, {{partner_id.city}}

Date: {{date_invoice|date:'%Y-%m-%d'}}
Due Date: {{date_due|date:'%Y-%m-%d'}}

{{#invoice_line_ids}}
  {{product_id.name}} - {{quantity}} x {{price_unit}} = {{price_subtotal}}
{{/invoice_line_ids}}

Total: {{amount_total|number:',.2f'}}
```

### 2. Sales Quotation
```
QUOTATION #{{name}}

Customer: {{partner_id.name}}
Date: {{date_order|date:'%B %d, %Y'}}
Valid Until: {{validity_date|date:'%B %d, %Y'}}

{{#order_line}}
  {{product_id.name}}
  Quantity: {{product_uom_qty}} {{product_uom.name}}
  Unit Price: {{price_unit|number:',.2f'}}
  Subtotal: {{price_subtotal|number:',.2f'}}
{{/order_line}}

Total Amount: {{amount_total|number:',.2f'}} {{currency_id.name}}
```

### 3. Contact Sheet
```
CONTACT INFORMATION

Personal Details:
Name: {{name}}
Email: {{email}}
Phone: {{phone}}
Mobile: {{mobile}}

Address:
{{street}}
{{street2}}
{{city}}, {{state_id.name}} {{zip}}
{{country_id.name}}

Company:
{{parent_id.name}}
{{function}} - {{title.name}}

Tags: {{category_id.name}}
```

---

## 🛠️ Troubleshooting

### Issue: "Field not found"
**Solution**: Check field name spelling. Use field selector in template form.

### Issue: "Template not in print menu"
**Solution**: Make sure template is Active and saved properly.

### Issue: "Empty values"
**Solution**: Some fields might be empty for that record. Set default values in Field Mappings.

### Issue: "Table not repeating"
**Solution**: Use `{{#field_name}}` and `{{/field_name}}` markers around table rows.

---

## 📚 Next Steps

1. ✅ Create your first template (Done!)
2. 📖 Read full README.md for advanced features
3. 🎨 Explore field selector to discover available fields
4. 🔧 Add custom formatters if needed
5. 📊 Create templates for all your reports

---

## 💬 Need Help?

- **Documentation**: See README.md
- **Installation**: See INSTALLATION.md
- **Development**: See DEVELOPMENT_PLAN.md
- **Status**: See IMPLEMENTATION_SUMMARY.md

---

**Time to First Report**: 5 minutes ⏱️  
**Difficulty**: Easy ⭐  
**Fun Factor**: High 🎉
