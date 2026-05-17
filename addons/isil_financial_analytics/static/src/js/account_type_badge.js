/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const ACCOUNT_TYPE_META = {
    asset:      { icon: "fa-building-o",  label: "Asset",      cls: "ifa-type-asset" },
    liability:  { icon: "fa-credit-card", label: "Liability",  cls: "ifa-type-liability" },
    receivable: { icon: "fa-arrow-down",  label: "Receivable", cls: "ifa-type-receivable" },
    payable:    { icon: "fa-arrow-up",    label: "Payable",    cls: "ifa-type-payable" },
    wage:       { icon: "fa-users",       label: "Payroll",    cls: "ifa-type-wage" },
};

export class AccountTypeBadge extends Component {
    static template = "isil_financial_analytics.AccountTypeBadge";
    static props = { ...standardFieldProps };

    get value() { return this.props.record.data[this.props.name] || false; }
    get meta() {
        return ACCOUNT_TYPE_META[this.value] ||
            { icon: "fa-circle-o", label: this.value || "—", cls: "" };
    }
}

registry.category("fields").add("account_type_badge", {
    component: AccountTypeBadge,
    supportedTypes: ["selection"],
});
