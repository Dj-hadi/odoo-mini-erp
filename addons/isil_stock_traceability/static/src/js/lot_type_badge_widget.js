/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const LOT_TYPE_META = {
    raw_material:     { icon: "fa-cubes",   label: "Raw Material",     cls: "st-lot-raw"      },
    finished_product: { icon: "fa-archive", label: "Finished Product", cls: "st-lot-finished" },
};

export class LotTypeBadgeWidget extends Component {
    static template = "isil_stock_traceability.LotTypeBadgeWidget";
    static props = { ...standardFieldProps };

    get value() { return this.props.record.data[this.props.name] || false; }
    get meta()  { return LOT_TYPE_META[this.value] || { icon: "fa-circle-o", label: this.value || "—", cls: "" }; }
    get selectionValues() { return this.props.record.fields[this.props.name]?.selection || []; }
    onChange(ev) { this.props.record.update({ [this.props.name]: ev.target.value || false }); }
}

registry.category("fields").add("lot_type_badge", {
    component: LotTypeBadgeWidget,
    supportedTypes: ["selection"],
});
