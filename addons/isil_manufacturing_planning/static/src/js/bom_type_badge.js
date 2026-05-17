/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const BOM_TYPE_META = {
    normal:  { icon: "fa-cog",  label: "Manufacture", cls: "bom-type-normal" },
    phantom: { icon: "fa-cubes", label: "Kit",         cls: "bom-type-phantom" },
};

export class BomTypeBadgeWidget extends Component {
    static template = "isil_manufacturing_planning.BomTypeBadgeWidget";
    static props = { ...standardFieldProps };

    get value() { return this.props.record.data[this.props.name] || false; }
    get meta()  {
        return BOM_TYPE_META[this.value] || { icon: "fa-circle-o", label: this.value || "—", cls: "" };
    }
    get selectionValues() { return this.props.record.fields[this.props.name]?.selection || []; }
    onChange(ev) { this.props.record.update({ [this.props.name]: ev.target.value || false }); }
}

registry.category("fields").add("bom_type_badge", {
    component: BomTypeBadgeWidget,
    supportedTypes: ["selection"],
});
