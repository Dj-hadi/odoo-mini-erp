/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class QCStatusBadgeWidget extends Component {
    static template = "isil_manufacturing_planning.QCStatusBadgeWidget";
    static props = { ...standardFieldProps };

    get value()      { return !!this.props.record.data[this.props.name]; }
    get badgeClass() { return this.value ? "qc-status-passed" : "qc-status-failed"; }
    get icon()       { return this.value ? "fa-check-circle"  : "fa-times-circle";  }
    get label()      { return this.value ? "Passed"           : "Failed";            }
}

registry.category("fields").add("qc_status_badge", {
    component: QCStatusBadgeWidget,
    supportedTypes: ["boolean"],
});
