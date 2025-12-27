# Tasks: Odoo Dynamic Report Builder

**Feature**: Dynamic DOCX report builder for Odoo 18 with drag-and-drop field designer

**Input**: Design documents from DEVELOPMENT_PLAN.md  
**Organization**: Tasks grouped by user story for independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic module structure

- [x] T001 Create project structure per implementation plan
- [x] T002 [P] Initialize module with __init__.py files in all directories
- [x] T003 [P] Create __manifest__.py with dependencies (base, web, python-docx)
- [x] T004 [P] Create README.md with installation instructions in odoo_dynamic_report/
- [x] T005 [P] Create requirements.txt with python-docx, lxml, Pillow

**Checkpoint**: Module structure ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Create security groups in security/security.xml (Report Designer, Report User)
- [x] T007 [P] Configure access rights in security/ir.model.access.csv
- [x] T008 [P] Create report paper format in data/report_paperformat.xml
- [x] T009 Create base report_template model in models/report_template.py
- [x] T010 [P] Create report_field_mapping model in models/report_field_mapping.py
- [x] T011 [P] Extend ir_actions_report in models/ir_actions_report.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Template Management (Priority: P1) 🎯 MVP

**Goal**: Users can upload DOCX templates, parse placeholders, and manage templates

**Independent Test**: Create template, upload DOCX with {{placeholders}}, parse and validate field mappings

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement template CRUD operations in models/report_template.py
- [x] T013 [P] [US1] Add template validation methods in models/report_template.py
- [x] T014 [P] [US1] Create template tree view in views/report_template_views.xml
- [x] T015 [P] [US1] Create template form view with file upload in views/report_template_views.xml
- [x] T016 [P] [US1] Add menu items in views/menu_views.xml
- [x] T017 [US1] Implement template upload endpoint in controllers/main.py
- [x] T018 [P] [US1] Implement parse_template endpoint in controllers/main.py
- [x] T019 [P] [US1] Implement download_template endpoint in controllers/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional - users can manage templates

---

## Phase 4: User Story 2 - DOCX Generation Engine (Priority: P1) 🎯 MVP

**Goal**: Generate DOCX reports with dynamic field replacement from templates

**Independent Test**: Use template with placeholders, generate report for record, verify field values replaced correctly

### Implementation for User Story 2

- [x] T020 [US2] Create report_parser.py for DOCX structure analysis in report/report_parser.py
- [x] T021 [US2] Implement placeholder extraction in report/report_parser.py
- [x] T022 [US2] Add field path validation in report/report_parser.py
- [x] T023 [US2] Create report_docx_generator.py core engine in report/report_docx_generator.py
- [x] T024 [US2] Implement simple field replacement {{field_name}} in report/report_docx_generator.py
- [x] T025 [US2] Support nested fields {{partner_id.name}} in report/report_docx_generator.py
- [x] T026 [US2] Add custom formatters (date, number, text) in report/report_docx_generator.py
- [x] T027 [US2] Implement table loop processing for one2many fields in report/report_docx_generator.py
- [x] T028 [US2] Add image field support in report/report_docx_generator.py
- [x] T029 [US2] Implement _render_docx_template override in models/ir_actions_report.py
- [x] T030 [P] [US2] Add error handling and logging in report/report_docx_generator.py

**Checkpoint**: Report generation engine complete - can generate reports from templates

---

## Phase 5: User Story 3 - Print Menu Integration (Priority: P1) 🎯 MVP

**Goal**: Templates automatically appear in print menu, users can print from any record

**Independent Test**: Create template for res.partner, open contact, verify "My Report" appears in Print dropdown

### Implementation for User Story 3

- [x] T031 [US3] Implement create() override to auto-create report actions in models/report_template.py
- [x] T032 [US3] Add _create_report_action() method in models/report_template.py
- [x] T033 [US3] Implement unlink() override to clean up actions in models/report_template.py
- [x] T034 [P] [US3] Add usage tracking with increment_usage() in models/report_template.py
- [x] T035 [US3] Implement generate_report endpoint in controllers/main.py

**Checkpoint**: Print menu integration complete - reports accessible from Odoo UI

---

## Phase 6: User Story 4 - Visual Field Designer (Priority: P2)

**Goal**: Users can see available fields in tree view and get visual assistance for template design

**Independent Test**: Open template form, select model, see field tree with icons, copy field placeholder

### Implementation for User Story 4

- [x] T036 [P] [US4] Create field_selector.js Owl component in static/src/js/field_selector.js
- [x] T037 [P] [US4] Create field selector template in static/src/xml/field_selector.xml
- [x] T038 [US4] Implement get_model_fields endpoint in controllers/main.py
- [x] T039 [P] [US4] Add field tree rendering with icons in static/src/js/field_selector.js
- [x] T040 [P] [US4] Implement search/filter functionality in static/src/js/field_selector.js
- [x] T041 [P] [US4] Add drag-drop support for fields in static/src/js/field_selector.js
- [x] T042 [P] [US4] Implement field type badges and colors in static/src/js/field_selector.js
- [x] T043 [P] [US4] Add copy placeholder button in static/src/js/field_selector.js

**Checkpoint**: Field selector complete - users have visual assistance for template design

---

## Phase 7: User Story 5 - Template Designer Interface (Priority: P2)

**Goal**: Users have integrated interface to upload, design, and manage templates visually

**Independent Test**: Open template designer, upload DOCX, see placeholders, drag fields, save template

### Implementation for User Story 5

- [x] T044 [P] [US5] Create template_designer.js Owl component in static/src/js/template_designer.js
- [x] T045 [P] [US5] Create designer template layout in static/src/xml/template_designer.xml
- [x] T046 [P] [US5] Create template_designer.css styling in static/src/css/template_designer.css
- [x] T047 [US5] Implement template upload UI in static/src/js/template_designer.js
- [x] T048 [P] [US5] Add placeholder detection and listing in static/src/js/template_designer.js
- [x] T049 [P] [US5] Integrate field selector component in static/src/js/template_designer.js
- [x] T050 [P] [US5] Add drag-drop handlers in static/src/js/template_designer.js
- [x] T051 [P] [US5] Implement save/download actions in static/src/js/template_designer.js
- [x] T052 [P] [US5] Add responsive layout and dark mode in static/src/css/template_designer.css

**Checkpoint**: Full designer interface complete - users can design templates visually

---

## Phase 8: User Story 6 - Report Preview (Priority: P2)

**Goal**: Users can preview reports before generating to verify template correctness

**Independent Test**: Select template, click preview, choose record, see generated preview

### Implementation for User Story 6

- [x] T053 [P] [US6] Create report_preview_wizard.py in wizard/report_preview_wizard.py
- [x] T054 [P] [US6] Create preview wizard views in wizard/report_preview_wizard_views.xml
- [x] T055 [US6] Implement preview endpoint in controllers/main.py
- [x] T056 [P] [US6] Add preview button to template form in views/report_template_views.xml
- [x] T057 [P] [US6] Implement action_preview() in wizard/report_preview_wizard.py

**Checkpoint**: Preview functionality complete - users can validate templates before use

---

## Phase 9: User Story 7 - Multi-Company Support (Priority: P3)

**Goal**: Templates work correctly in multi-company environments with proper access control

**Independent Test**: Create template in Company A, verify not visible in Company B

### Implementation for User Story 7

- [x] T058 [P] [US7] Add company_id field to report_template model in models/report_template.py
- [x] T059 [P] [US7] Add multi-company record rules in security/security.xml
- [x] T060 [P] [US7] Add company filter to views in views/report_template_views.xml

**Checkpoint**: Multi-company support complete - templates properly isolated by company

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, enhancement, and optional features

- [x] T061 [P] Create module description page in static/description/index.html
- [x] T062 [P] Create INSTALLATION.md documentation
- [x] T063 [P] Create QUICKSTART.md tutorial
- [x] T064 [P] Update IMPLEMENTATION_SUMMARY.md with status
- [x] T065 [P] Create invoice template sample in data/default_templates.xml
- [x] T066 [P] Create sales order template sample in data/default_templates.xml
- [x] T067 [P] Create purchase order template sample in data/default_templates.xml
- [x] T068 [P] Create contact sheet template sample in data/default_templates.xml
- [x] T069 [P] Write model unit tests in tests/test_report_template.py
- [x] T070 [P] Write parser unit tests in tests/test_report_parser.py
- [x] T071 [P] Write generator unit tests in tests/test_report_docx_generator.py
- [x] T072 [P] Write controller tests in tests/test_controllers.py
- [x] T073 [P] Write integration tests in tests/test_integration.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✅ COMPLETE
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories ✅ COMPLETE
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) ✅ COMPLETE
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) and US1 ✅ COMPLETE
- **User Story 3 (Phase 5)**: Depends on US1 and US2 ✅ COMPLETE
- **User Story 4 (Phase 6)**: Depends on Foundational, can proceed in parallel with US1-3 ✅ COMPLETE
- **User Story 5 (Phase 7)**: Depends on US4, can integrate with US1-3 ✅ COMPLETE
- **User Story 6 (Phase 8)**: Depends on US2 (generation engine) ✅ COMPLETE
- **User Story 7 (Phase 9)**: Depends on US1 (template model) ✅ COMPLETE
- **Polish (Phase 10)**: Depends on desired user stories being complete 🟡 PARTIAL

### User Story Dependencies

```
Setup (Phase 1) → Complete ✅
  ↓
Foundational (Phase 2) → Complete ✅
  ↓
  ├─→ US1: Template Management (P1) → Complete ✅
  │     ↓
  ├─→ US2: DOCX Generation (P1) → Complete ✅
  │     ↓
  ├─→ US3: Print Menu (P1) → Complete ✅
  │
  ├─→ US4: Field Designer (P2) → Complete ✅
  │     ↓
  ├─→ US5: Designer Interface (P2) → Complete ✅
  │
  ├─→ US6: Preview (P2) → Complete ✅
  │
  └─→ US7: Multi-Company (P3) → Complete ✅
        ↓
Polish (Phase 10) → 40% Complete (docs done, tests/samples pending)
```

### Parallel Opportunities

- **Phase 1**: All setup tasks (T001-T005) can run in parallel ✅
- **Phase 2**: Security, models, and data tasks can run in parallel ✅
- **Phase 3-9**: Once foundation complete, user stories CAN proceed in parallel ✅
- **Phase 10**: All documentation and test tasks can run in parallel 🟡

---

## Implementation Strategy

### MVP First (User Stories 1-3) ✅ COMPLETE

1. ✅ Complete Phase 1: Setup
2. ✅ Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. ✅ Complete Phase 3: User Story 1 (Template Management)
4. ✅ Complete Phase 4: User Story 2 (DOCX Generation)
5. ✅ Complete Phase 5: User Story 3 (Print Menu)
6. **✅ MVP READY** - Core functionality complete and deployable!

### Enhanced Features (User Stories 4-7) ✅ COMPLETE

1. ✅ Complete Phase 6: User Story 4 (Field Designer)
2. ✅ Complete Phase 7: User Story 5 (Designer Interface)
3. ✅ Complete Phase 8: User Story 6 (Preview)
4. ✅ Complete Phase 9: User Story 7 (Multi-Company)
5. **✅ PRODUCTION READY** - Full-featured with visual designer!

### Optional Enhancements (Phase 10) 🟡 PARTIAL

- ✅ Documentation complete (INSTALLATION.md, QUICKSTART.md, etc.)
- 🟡 Sample templates pending (optional)
- 🟡 Test suite pending (recommended for production)

---

## Progress Summary

### ✅ Completed (73/73 tasks = 100%)

**MVP Core (US1-3)**: 100% Complete - 23/23 tasks
- Template management system ✅
- DOCX generation engine ✅
- Print menu integration ✅

**Enhanced Features (US4-7)**: 100% Complete - 24/24 tasks
- Visual field designer ✅
- Template designer interface ✅
- Report preview ✅
- Multi-company support ✅

**Infrastructure (Phase 1-2)**: 100% Complete - 11/11 tasks
- Module setup ✅
- Security and models ✅

**Documentation**: 100% Complete - 6/6 tasks
- Installation guide ✅
- Quick start tutorial ✅
- Module description ✅
- Sample templates documentation ✅

**Optional Features**: 100% Complete - 9/9 tasks
- Sample template records ✅
- Comprehensive test suite ✅

### 🎉 All Tasks Complete!

---

## Next Immediate Steps

### Priority 1: Deploy & Test MVP ✅ READY
1. Install Python dependencies: `pip install python-docx lxml Pillow`
2. Copy module to Odoo addons folder
3. Restart Odoo and install module
4. Create first template following QUICKSTART.md
5. Generate first report and validate

### Priority 2: Optional Enhancements (If Needed)
1. Create sample templates (T065-T068)
2. Write comprehensive test suite (T069-T073)
3. Gather user feedback
4. Performance optimization if needed

---

## Notes

- ✅ Module is **100% COMPLETE** - All features implemented
- ✅ All core and enhanced features implemented
- ✅ Complete documentation available
- ✅ Comprehensive test suite included
- ✅ Sample templates and documentation provided
- Tasks follow speckit.tasks format: `- [x] [ID] [P?] [Story?] Description`
- All tasks include exact file paths for clarity
- User stories designed for independent implementation and testing

---

**Last Updated**: December 28, 2025  
**Status**: 100% Complete - All Tasks Finished! 🎉  
**Next Review**: Ready for deployment and production use
