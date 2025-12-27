<!--
SYNC IMPACT REPORT - Constitution Update v1.0.0

Version Change: [template] → 1.0.0 (Initial Ratification)
Rationale: First complete constitution based on implemented project requirements

Modified Principles:
- Added: I. Document-Centric Design (DOCX library foundation)
- Added: II. User-First Interface (no-code drag-drop requirement)
- Added: III. Field Flexibility (comprehensive field system)
- Added: IV. Validation & Error Prevention (quality gates)
- Added: V. Multi-Tenancy & Security (enterprise requirements)

Added Sections:
- Technology Requirements (mandatory stack)
- Performance Standards (SLA requirements)
- Quality Gates (deployment criteria)
- Governance (amendment procedures)

Templates Requiring Updates:
✅ Constitution completed
⚠ PENDING: Review plan-template.md for alignment
⚠ PENDING: Review spec-template.md for alignment
⚠ PENDING: Review tasks-template.md for alignment

Follow-up TODOs:
- None - all principles defined based on project implementation

Date: 2025-12-28
-->

# Odoo Dynamic Report Builder Constitution

**Project Purpose**: Enable users to design custom DOCX reports for Odoo without programming 
knowledge through an intuitive drag-and-drop interface for field selection and template 
management, automatically integrating with Odoo's print system.

## Core Principles

### I. Document-Centric Design

**MUST use python-docx library** as the foundation for all DOCX template manipulation and 
report generation. All template processing MUST preserve native DOCX formatting, structure, 
and features (tables, images, styles, headers/footers).

**Rationale**: python-docx provides reliable, maintained DOCX manipulation without requiring 
Microsoft Office installation. Native DOCX support ensures users can design templates in 
familiar tools (Word, LibreOffice) and maintain full formatting control.

**Implementation Requirements**:
- Template upload/download MUST support .docx format
- Field placeholders MUST use simple syntax: `{{field_name}}`
- Template parsing MUST extract structure without losing formatting
- Report generation MUST preserve all Word formatting features

### II. User-First Interface (NON-NEGOTIABLE)

**Interface MUST be clear, intuitive, and require zero coding knowledge.** Users MUST be 
able to design complete reports through visual drag-and-drop actions without writing any 
code, expressions, or understanding technical syntax.

**Rationale**: Target audience is business users, not developers. Success depends on 
eliminating technical barriers. QWeb-like functionality MUST be achieved through visual 
design tools, not code.

**Implementation Requirements**:
- Drag-and-drop field selection MUST be primary interaction model
- Field tree MUST display available fields with icons, types, and descriptions
- Template designer MUST provide visual feedback during field placement
- Error messages MUST be user-friendly with suggested corrections
- Documentation MUST include visual examples, not just code samples

### III. Field Flexibility & Iteration

**MUST support comprehensive field access including simple fields, nested relationships 
(many2one), and table iteration (one2many/many2many).** Users MUST be able to insert any 
field from the selected Odoo model and related models without limitation.

**Rationale**: Reports often require data from related records (e.g., partner details on 
invoice, order lines in quotation). Table iteration enables line-by-line reporting of 
child records, matching QWeb functionality.

**Implementation Requirements**:
- Simple fields: `{{field_name}}` for direct model fields
- Nested fields: `{{partner_id.name}}` for related record access
- Table loops: `{{#field_name}}...{{/field_name}}` for iterating one2many
- Custom formatters: `{{date|date:'%Y-%m-%d'}}` for presentation control
- Field validation MUST occur before report generation
- Related field depth MUST support at least 3 levels (e.g., `order_id.partner_id.country_id.name`)

### IV. Validation & Error Prevention

**Template validation MUST occur at design time, not runtime.** All field references MUST 
be validated when template is saved. Report generation errors MUST provide clear 
diagnostics with field path and suggested fixes.

**Rationale**: Catching errors during design prevents user frustration and report 
generation failures in production. Preview functionality enables testing before deployment.

**Implementation Requirements**:
- Field path validation MUST run on template save
- Invalid field references MUST block template activation
- Preview wizard MUST test template with real data before production use
- Error messages MUST include: field path, error type, model context, suggestion
- Logging MUST capture generation errors for administrator review

### V. Multi-Tenancy & Security

**MUST support Odoo multi-company architecture with proper data isolation.** Templates MUST 
be company-scoped. Record rules MUST enforce data access restrictions. Security groups 
MUST separate design permissions from usage permissions.

**Rationale**: Enterprise Odoo deployments require multi-company support. Security is 
non-negotiable for business documents containing sensitive data.

**Implementation Requirements**:
- Templates MUST have `company_id` field with multi-company record rules
- Security groups: "Report Designer" (create/edit templates), "Report User" (generate only)
- Access rights MUST respect model-level permissions during generation
- Template storage MUST be secure (no public file access)
- Generated reports MUST respect record-level security rules

## Technology Requirements

### Mandatory Stack

**Backend** (NON-NEGOTIABLE):
- Odoo 18.0+ (framework)
- Python 3.10+ (language)
- python-docx (DOCX manipulation)
- lxml (XML parsing)
- Pillow (image processing)

**Frontend** (NON-NEGOTIABLE):
- Owl Framework (Odoo's component system for Odoo 18+)
- JavaScript ES6+ (language)
- CSS3 (styling with responsive design)

**Rationale**: These technologies are chosen for compatibility with Odoo 18's architecture 
and proven reliability. python-docx is the de facto standard for Python DOCX work. Owl is 
Odoo 18's official frontend framework replacing legacy widget system.

### Dependency Management

- External Python dependencies MUST be listed in `requirements.txt`
- Module manifest MUST declare Odoo module dependencies (`base`, `web`)
- Breaking dependency changes require MAJOR version increment

## Performance Standards

### Service Level Requirements

**Template Operations**:
- Template upload: MUST complete < 2 seconds for files up to 10MB
- Template parsing: MUST complete < 3 seconds for templates up to 50 pages
- Field validation: MUST complete < 1 second for any field path

**Report Generation**:
- Standard report (1-10 pages, ≤100 line items): MUST complete < 5 seconds
- Complex report (11-50 pages, ≤1000 line items): MUST complete < 15 seconds
- Large report (50+ pages, >1000 line items): Background processing acceptable

**User Interface**:
- Designer interface: MUST load < 2 seconds
- Field tree: MUST render < 1 second for models with ≤500 fields
- Preview generation: MUST complete < 3 seconds or show progress indicator

**Rationale**: Performance directly impacts user adoption. These targets balance user 
experience with technical feasibility. Background processing prevents UI blocking for 
large reports.

### Optimization Requirements

- Template caching SHOULD be implemented for frequently-used templates
- Field metadata caching SHOULD reduce model introspection overhead
- Progress indicators MUST be shown for operations exceeding 3 seconds
- Error handling MUST not degrade performance (fail fast principle)

## Quality Gates

### Deployment Criteria

Before any production deployment, the following MUST be verified:

**Functional Requirements** (ALL must pass):
- [ ] Users can create templates for any Odoo model
- [ ] Drag-and-drop field insertion works in designer
- [ ] Templates automatically appear in Print menu
- [ ] Generated reports correctly replace all placeholders
- [ ] Multi-company isolation functions correctly
- [ ] Field validation prevents invalid templates

**Testing Requirements** (RECOMMENDED, not blocking):
- [ ] Model unit tests exist for report_template, report_field_mapping
- [ ] Parser tests validate placeholder extraction
- [ ] Generator tests verify field replacement logic
- [ ] Controller tests cover all API endpoints
- [ ] Integration tests verify end-to-end workflow

**Documentation Requirements** (ALL must pass):
- [ ] README.md includes installation and usage instructions
- [ ] Template placeholder syntax documented with examples
- [ ] Field selector usage explained
- [ ] Troubleshooting guide available

**Security Review** (ALL must pass):
- [ ] Security groups properly configured
- [ ] Record rules enforce multi-company isolation
- [ ] No SQL injection vulnerabilities in field path handling
- [ ] File upload validates DOCX format and size limits

### Quality Standards

- Critical bugs (data loss, security, crashes): ZERO tolerance
- Major bugs (functionality broken): Fix before deployment
- Minor bugs (cosmetic, edge cases): Document and schedule
- Test coverage: 70%+ recommended, not mandatory
- Code review: Recommended for complex changes

## Governance

### Amendment Procedure

1. **Proposal**: Any team member may propose constitution amendment
2. **Review**: Technical lead reviews for consistency and impact
3. **Documentation**: Update this file with rationale in sync impact report
4. **Propagation**: Update affected templates and documentation
5. **Version**: Increment version per semantic versioning rules
6. **Approval**: Commit requires approval from technical lead

### Version Policy

**MAJOR** (X.0.0): Backward-incompatible changes
- Removing or redefining core principles
- Technology stack changes (e.g., replacing python-docx)
- Breaking changes to fundamental architecture

**MINOR** (0.X.0): Additive changes
- New principles added
- New sections added
- Expanded requirements or quality gates

**PATCH** (0.0.X): Clarifications
- Wording improvements
- Typo corrections
- Non-semantic refinements
- Example updates

### Compliance

- All feature specifications MUST align with principles herein
- All implementation plans MUST reference relevant constitutional requirements
- All code reviews SHOULD verify principle compliance
- This constitution supersedes conflicting practices or documentation
- Principle violations require explicit justification and technical lead approval

### Living Document

- Constitution MUST be reviewed after major feature additions
- Principles should evolve with project maturity but remain stable
- Contradictions between constitution and reality require resolution (update one or the other)
- Team feedback on constitutional burden is welcome and considered

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
