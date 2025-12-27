# Sample Template Documentation

This directory should contain sample DOCX template files that users can download and use as starting points.

## Creating Sample Templates

The following sample templates should be created as .docx files using Microsoft Word or LibreOffice Writer:

### 1. Invoice Template (invoice_template.docx)

**Document Structure:**
```
[COMPANY LOGO - Image placeholder]

INVOICE #{{name}}

Date: {{invoice_date|date:'%Y-%m-%d'}}
Due Date: {{invoice_date_due|date:'%Y-%m-%d'}}

BILL TO:
{{partner_id.name}}
{{partner_id.street}}
{{partner_id.city}}, {{partner_id.state_id.name}} {{partner_id.zip}}
{{partner_id.country_id.name}}

Phone: {{partner_id.phone}}
Email: {{partner_id.email}}

INVOICE DETAILS:
| Item | Description | Quantity | Unit Price | Tax | Subtotal |
|------|-------------|----------|------------|-----|----------|
{{#invoice_line_ids}}
| {{product_id.default_code}} | {{name}} | {{quantity}} | {{price_unit|number:',.2f'}} | {{tax_ids.name}} | {{price_subtotal|number:',.2f'}} |
{{/invoice_line_ids}}

                                        Subtotal: {{amount_untaxed|number:',.2f'}} {{currency_id.name}}
                                        Tax: {{amount_tax|number:',.2f'}} {{currency_id.name}}
                                        Total: {{amount_total|number:',.2f'}} {{currency_id.name}}

Payment Terms: {{invoice_payment_term_id.name}}
Reference: {{ref}}

Notes:
{{narration}}

---
Thank you for your business!
```

### 2. Sales Order Template (sales_order_template.docx)

**Document Structure:**
```
[COMPANY LOGO]

SALES QUOTATION #{{name}}

Date: {{date_order|date:'%B %d, %Y'}}
Valid Until: {{validity_date|date:'%B %d, %Y'}}
Sales Person: {{user_id.name}}

CUSTOMER:
{{partner_id.name}}
{{partner_id.street}}
{{partner_id.city}}, {{partner_id.state_id.name}} {{partner_id.zip}}
{{partner_id.country_id.name}}

Contact: {{partner_id.phone}} | {{partner_id.email}}

ORDER LINES:
| # | Product | Description | Qty | UoM | Unit Price | Discount | Subtotal |
|---|---------|-------------|-----|-----|------------|----------|----------|
{{#order_line}}
| {{sequence}} | {{product_id.name}} | {{name}} | {{product_uom_qty}} | {{product_uom.name}} | {{price_unit|number:',.2f'}} | {{discount}}% | {{price_subtotal|number:',.2f'}} |
{{/order_line}}

                                        Untaxed Amount: {{amount_untaxed|number:',.2f'}} {{currency_id.name}}
                                        Taxes: {{amount_tax|number:',.2f'}} {{currency_id.name}}
                                        Total: {{amount_total|number:',.2f'}} {{currency_id.name}}

Delivery Address:
{{partner_shipping_id.name}}
{{partner_shipping_id.street}}
{{partner_shipping_id.city}}, {{partner_shipping_id.state_id.name}} {{partner_shipping_id.zip}}

Terms and Conditions:
{{note}}
```

### 3. Purchase Order Template (purchase_order_template.docx)

**Document Structure:**
```
[COMPANY LOGO]

PURCHASE ORDER #{{name}}

Order Date: {{date_order|date:'%Y-%m-%d'}}
Expected Delivery: {{date_planned|date:'%Y-%m-%d'}}
Buyer: {{user_id.name}}

VENDOR:
{{partner_id.name}}
{{partner_id.street}}
{{partner_id.city}}, {{partner_id.state_id.name}} {{partner_id.zip}}
{{partner_id.country_id.name}}

Contact: {{partner_id.phone}} | {{partner_id.email}}

DELIVER TO:
{{picking_type_id.warehouse_id.partner_id.name}}
{{picking_type_id.warehouse_id.partner_id.street}}
{{picking_type_id.warehouse_id.partner_id.city}}

ORDER DETAILS:
| Item | Product | Description | Quantity | UoM | Unit Price | Taxes | Subtotal |
|------|---------|-------------|----------|-----|------------|-------|----------|
{{#order_line}}
| {{sequence}} | {{product_id.default_code}} | {{name}} | {{product_qty}} | {{product_uom.name}} | {{price_unit|number:',.2f'}} | {{taxes_id.name}} | {{price_subtotal|number:',.2f'}} |
{{/order_line}}

                                        Untaxed Total: {{amount_untaxed|number:',.2f'}} {{currency_id.name}}
                                        Taxes: {{amount_tax|number:',.2f'}} {{currency_id.name}}
                                        Total: {{amount_total|number:',.2f'}} {{currency_id.name}}

Payment Terms: {{payment_term_id.name}}

Notes:
{{notes}}

---
Please confirm receipt of this purchase order.
```

### 4. Contact Sheet Template (contact_sheet_template.docx)

**Document Structure:**
```
CONTACT INFORMATION

[CONTACT PHOTO - if available: {{image_1920}}]

Personal Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {{name}}
Title: {{title.name}}
Function: {{function}}
Company: {{parent_id.name}}

Contact Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Email: {{email}}
Phone: {{phone}}
Mobile: {{mobile}}
Website: {{website}}

Address:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Street: {{street}}
Street2: {{street2}}
City: {{city}}
State/Province: {{state_id.name}}
Postal Code: {{zip}}
Country: {{country_id.name}}

Business Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VAT: {{vat}}
Tax ID: {{l10n_in_gstin}}
Reference: {{ref}}

Tags: {{category_id.name}}

Additional Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{{comment}}

---
Generated: {{create_date|date:'%Y-%m-%d %H:%M:%S'}}
Last Updated: {{write_date|date:'%Y-%m-%d %H:%M:%S'}}
```

## How to Create These Templates

1. Open Microsoft Word or LibreOffice Writer
2. Design your template layout with formatting, logos, styles
3. Insert placeholders using the formats shown above:
   - Simple fields: `{{field_name}}`
   - Nested fields: `{{partner_id.name}}`
   - Formatted fields: `{{date|date:'%Y-%m-%d'}}`
   - Table loops: `{{#field_name}}...{{/field_name}}`
4. Save as .docx format
5. Upload through Odoo interface or store in data/ directory

## Notes

- Replace `[COMPANY LOGO]` with actual image
- Replace `[CONTACT PHOTO]` with image field placeholder
- Adjust table widths and formatting as needed
- Add company colors and branding
- Customize field selection based on available model fields

## Installation

To use these samples:
1. Copy template files to accessible location
2. In Odoo, go to Report Templates
3. Upload each template
4. System will auto-detect placeholders
5. Activate and test with real data
