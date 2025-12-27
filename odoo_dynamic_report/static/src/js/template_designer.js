/** @odoo-module **/

import { Component, useState, onWillStart, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * Template Designer Component
 * Main interface for designing and editing report templates
 */
export class TemplateDesigner extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.notification = useService("notification");
        
        this.state = useState({
            templateId: this.props.templateId || null,
            template: null,
            modelFields: [],
            selectedField: null,
            placeholders: [],
            isLoading: false,
            isDirty: false,
        });

        onWillStart(async () => {
            if (this.state.templateId) {
                await this.loadTemplate();
            }
        });

        onMounted(() => {
            this.setupDragDrop();
        });
    }

    /**
     * Load template data
     */
    async loadTemplate() {
        this.state.isLoading = true;
        try {
            const templates = await this.orm.searchRead(
                "report.template",
                [["id", "=", this.state.templateId]],
                ["name", "model_id", "model_name", "template_data", "field_mappings"]
            );
            
            if (templates.length > 0) {
                this.state.template = templates[0];
                await this.loadModelFields();
                await this.parseTemplate();
            }
        } catch (error) {
            this.notification.add(
                "Error loading template: " + error.message,
                { type: "danger" }
            );
        } finally {
            this.state.isLoading = false;
        }
    }

    /**
     * Load available fields for the template's model
     */
    async loadModelFields() {
        if (!this.state.template || !this.state.template.model_name) {
            return;
        }

        try {
            const result = await this.rpc("/report_template/get_model_fields", {
                model_name: this.state.template.model_name,
                include_related: true,
                max_depth: 2,
            });

            if (result.success) {
                this.state.modelFields = result.fields;
            } else {
                throw new Error(result.error || "Failed to load fields");
            }
        } catch (error) {
            this.notification.add(
                "Error loading model fields: " + error.message,
                { type: "danger" }
            );
        }
    }

    /**
     * Parse template to extract placeholders
     */
    async parseTemplate() {
        if (!this.state.template || !this.state.template.template_data) {
            return;
        }

        try {
            const result = await this.rpc("/report_template/parse_template", {
                template_id: this.state.templateId,
            });

            if (result.success) {
                this.state.placeholders = result.placeholders || [];
            }
        } catch (error) {
            console.error("Error parsing template:", error);
        }
    }

    /**
     * Setup drag and drop functionality
     */
    setupDragDrop() {
        // This will be enhanced when integrating with field selector
        const designArea = this.designAreaRef?.el;
        if (!designArea) return;

        designArea.addEventListener("dragover", (e) => {
            e.preventDefault();
            designArea.classList.add("drag-over");
        });

        designArea.addEventListener("dragleave", () => {
            designArea.classList.remove("drag-over");
        });

        designArea.addEventListener("drop", (e) => {
            e.preventDefault();
            designArea.classList.remove("drag-over");
            
            const fieldData = e.dataTransfer.getData("application/json");
            if (fieldData) {
                const field = JSON.parse(fieldData);
                this.insertFieldPlaceholder(field);
            }
        });
    }

    /**
     * Insert field placeholder into template
     */
    insertFieldPlaceholder(field) {
        const placeholder = `{{${field.path}}}`;
        this.notification.add(
            `Placeholder ${placeholder} added. Remember to update your DOCX template.`,
            { type: "info" }
        );
        
        // Add to placeholders list
        if (!this.state.placeholders.includes(field.path)) {
            this.state.placeholders.push(field.path);
            this.state.isDirty = true;
        }
    }

    /**
     * Upload new template file
     */
    async onUploadTemplate(ev) {
        const file = ev.target.files[0];
        if (!file) return;

        if (!file.name.endsWith('.docx')) {
            this.notification.add(
                "Please upload a DOCX file",
                { type: "warning" }
            );
            return;
        }

        this.state.isLoading = true;
        try {
            const reader = new FileReader();
            reader.onload = async (e) => {
                const base64Data = e.target.result.split(',')[1];
                
                await this.orm.write("report.template", [this.state.templateId], {
                    template_data: base64Data,
                    template_filename: file.name,
                });

                await this.parseTemplate();
                
                this.notification.add(
                    "Template uploaded successfully",
                    { type: "success" }
                );
            };
            reader.readAsDataURL(file);
        } catch (error) {
            this.notification.add(
                "Error uploading template: " + error.message,
                { type: "danger" }
            );
        } finally {
            this.state.isLoading = false;
        }
    }

    /**
     * Preview template with sample data
     */
    async onPreview() {
        if (!this.state.templateId) {
            this.notification.add("Please save the template first", { type: "warning" });
            return;
        }

        window.open(
            `/report_template/preview?template_id=${this.state.templateId}`,
            '_blank'
        );
    }

    /**
     * Download template file
     */
    async onDownload() {
        if (!this.state.templateId) {
            return;
        }

        window.location.href = `/report_template/download/${this.state.templateId}`;
    }

    /**
     * Save field mappings
     */
    async onSave() {
        if (!this.state.templateId) return;

        this.state.isLoading = true;
        try {
            const fieldMappings = JSON.stringify({
                placeholders: this.state.placeholders,
            });

            await this.orm.write("report.template", [this.state.templateId], {
                field_mappings: fieldMappings,
            });

            this.state.isDirty = false;
            
            this.notification.add(
                "Template saved successfully",
                { type: "success" }
            );
        } catch (error) {
            this.notification.add(
                "Error saving template: " + error.message,
                { type: "danger" }
            );
        } finally {
            this.state.isLoading = false;
        }
    }

    /**
     * Copy placeholder to clipboard
     */
    copyPlaceholder(fieldPath) {
        const placeholder = `{{${fieldPath}}}`;
        navigator.clipboard.writeText(placeholder);
        this.notification.add(
            `Copied: ${placeholder}`,
            { type: "info" }
        );
    }

    /**
     * Validate field path
     */
    async validateField(fieldPath) {
        try {
            const result = await this.rpc("/report_template/validate_field", {
                model_name: this.state.template.model_name,
                field_path: fieldPath,
            });

            if (result.success && result.valid) {
                this.notification.add(
                    `Field ${fieldPath} is valid`,
                    { type: "success" }
                );
            } else {
                this.notification.add(
                    result.error || "Field validation failed",
                    { type: "warning" }
                );
            }
        } catch (error) {
            this.notification.add(
                "Error validating field: " + error.message,
                { type: "danger" }
            );
        }
    }
}

TemplateDesigner.template = "odoo_dynamic_report.TemplateDesigner";
TemplateDesigner.props = {
    templateId: { type: Number, optional: true },
};

// Register as a component that can be used in views
registry.category("view_widgets").add("template_designer", TemplateDesigner);
