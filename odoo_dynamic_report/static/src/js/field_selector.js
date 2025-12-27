/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

/**
 * Field Selector Component
 * Tree view of model fields with drag-and-drop support
 */
export class FieldSelector extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        
        this.state = useState({
            modelName: this.props.modelName || null,
            fields: [],
            filteredFields: [],
            searchText: "",
            expandedFields: new Set(),
            selectedField: null,
            isLoading: false,
            groupBy: "type", // 'type' or 'none'
        });

        onWillStart(async () => {
            if (this.state.modelName) {
                await this.loadFields();
            }
        });
    }

    /**
     * Load fields for the model
     */
    async loadFields() {
        this.state.isLoading = true;
        try {
            const result = await this.rpc("/report_template/get_model_fields", {
                model_name: this.state.modelName,
                include_related: true,
                max_depth: 2,
            });

            if (result.success) {
                this.state.fields = this.organizeFields(result.fields);
                this.state.filteredFields = this.state.fields;
            } else {
                throw new Error(result.error || "Failed to load fields");
            }
        } catch (error) {
            this.notification.add(
                "Error loading fields: " + error.message,
                { type: "danger" }
            );
        } finally {
            this.state.isLoading = false;
        }
    }

    /**
     * Organize fields into a tree structure
     */
    organizeFields(fields) {
        const fieldMap = new Map();
        const rootFields = [];

        // First pass: create field nodes
        fields.forEach(field => {
            const parts = field.path.split('.');
            const depth = parts.length - 1;
            
            const fieldNode = {
                ...field,
                depth: depth,
                children: [],
                isExpanded: false,
                parent: depth > 0 ? parts.slice(0, -1).join('.') : null,
            };

            fieldMap.set(field.path, fieldNode);
        });

        // Second pass: build tree structure
        fieldMap.forEach((node) => {
            if (node.parent && fieldMap.has(node.parent)) {
                fieldMap.get(node.parent).children.push(node);
            } else if (node.depth === 0) {
                rootFields.push(node);
            }
        });

        return rootFields;
    }

    /**
     * Get field icon based on type
     */
    getFieldIcon(fieldType) {
        const iconMap = {
            'char': 'fa-font',
            'text': 'fa-align-left',
            'integer': 'fa-hashtag',
            'float': 'fa-calculator',
            'boolean': 'fa-check-square',
            'date': 'fa-calendar',
            'datetime': 'fa-clock-o',
            'many2one': 'fa-link',
            'one2many': 'fa-list',
            'many2many': 'fa-tags',
            'binary': 'fa-file',
            'selection': 'fa-list-ul',
            'monetary': 'fa-dollar',
            'html': 'fa-code',
        };
        return iconMap[fieldType] || 'fa-question';
    }

    /**
     * Get field type color
     */
    getFieldTypeColor(fieldType) {
        const colorMap = {
            'char': '#3498db',
            'text': '#3498db',
            'integer': '#e74c3c',
            'float': '#e74c3c',
            'boolean': '#9b59b6',
            'date': '#f39c12',
            'datetime': '#f39c12',
            'many2one': '#1abc9c',
            'one2many': '#16a085',
            'many2many': '#16a085',
            'binary': '#95a5a6',
            'selection': '#34495e',
            'monetary': '#27ae60',
            'html': '#e67e22',
        };
        return colorMap[fieldType] || '#95a5a6';
    }

    /**
     * Filter fields based on search text
     */
    onSearchInput(ev) {
        this.state.searchText = ev.target.value.toLowerCase();
        this.filterFields();
    }

    /**
     * Filter fields
     */
    filterFields() {
        if (!this.state.searchText) {
            this.state.filteredFields = this.state.fields;
            return;
        }

        const matchesSearch = (field) => {
            return (
                field.name.toLowerCase().includes(this.state.searchText) ||
                field.string.toLowerCase().includes(this.state.searchText) ||
                field.path.toLowerCase().includes(this.state.searchText)
            );
        };

        const filterRecursive = (fields) => {
            return fields.filter(field => {
                const matches = matchesSearch(field);
                if (field.children && field.children.length > 0) {
                    field.children = filterRecursive(field.children);
                    return matches || field.children.length > 0;
                }
                return matches;
            });
        };

        this.state.filteredFields = filterRecursive([...this.state.fields]);
    }

    /**
     * Toggle field expansion
     */
    toggleFieldExpansion(field) {
        field.isExpanded = !field.isExpanded;
    }

    /**
     * Start dragging a field
     */
    onDragStart(ev, field) {
        ev.dataTransfer.effectAllowed = "copy";
        ev.dataTransfer.setData("application/json", JSON.stringify(field));
        ev.target.classList.add("dragging");
    }

    /**
     * End dragging
     */
    onDragEnd(ev) {
        ev.target.classList.remove("dragging");
    }

    /**
     * Select a field
     */
    selectField(field) {
        this.state.selectedField = field;
        
        // Trigger event for parent components
        if (this.props.onFieldSelected) {
            this.props.onFieldSelected(field);
        }
    }

    /**
     * Copy field placeholder to clipboard
     */
    copyFieldPlaceholder(field) {
        const placeholder = `{{${field.path}}}`;
        navigator.clipboard.writeText(placeholder);
        
        this.notification.add(
            `Copied: ${placeholder}`,
            { type: "info", sticky: false }
        );
    }

    /**
     * Insert field into template
     */
    insertField(field) {
        if (this.props.onFieldInsert) {
            this.props.onFieldInsert(field);
        } else {
            this.copyFieldPlaceholder(field);
        }
    }

    /**
     * Get field tooltip
     */
    getFieldTooltip(field) {
        let tooltip = `${field.string}\n`;
        tooltip += `Type: ${field.type}\n`;
        tooltip += `Path: ${field.path}\n`;
        if (field.help) {
            tooltip += `\n${field.help}`;
        }
        return tooltip;
    }

    /**
     * Group fields by type
     */
    toggleGrouping() {
        this.state.groupBy = this.state.groupBy === "type" ? "none" : "type";
    }

    /**
     * Render field tree
     */
    renderFieldTree(fields, depth = 0) {
        return fields.map(field => this.renderFieldNode(field, depth));
    }

    /**
     * Render single field node
     */
    renderFieldNode(field, depth) {
        const hasChildren = field.children && field.children.length > 0;
        const indent = depth * 20;

        return {
            field,
            hasChildren,
            indent,
            isExpanded: field.isExpanded,
        };
    }
}

FieldSelector.template = "odoo_dynamic_report.FieldSelector";
FieldSelector.props = {
    modelName: { type: String, optional: true },
    onFieldSelected: { type: Function, optional: true },
    onFieldInsert: { type: Function, optional: true },
};

// Register as a reusable component
registry.category("view_widgets").add("field_selector", FieldSelector);

export default FieldSelector;
