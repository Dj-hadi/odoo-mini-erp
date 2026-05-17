/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const EXPIRY_META = {
    no_date:       { icon: "fa-calendar-o",  label: "No Date",       cls: "st-expiry-none"    },
    fresh:         { icon: "fa-check-circle", label: "Fresh",         cls: "st-expiry-fresh"   },
    expiring_soon: { icon: "fa-clock-o",      label: "Expiring Soon", cls: "st-expiry-soon"    },
    expired:       { icon: "fa-times-circle", label: "Expired",       cls: "st-expiry-expired" },
};

export class ExpiryBadgeWidget extends Component {
    static template = "isil_stock_traceability.ExpiryBadgeWidget";
    static props = { ...standardFieldProps };

    get value() { return this.props.record.data[this.props.name] || "no_date"; }
    get meta()  { return EXPIRY_META[this.value] || EXPIRY_META.no_date; }
}

registry.category("fields").add("expiry_badge", {
    component: ExpiryBadgeWidget,
    supportedTypes: ["selection"],
});
