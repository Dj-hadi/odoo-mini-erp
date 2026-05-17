/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class IsilDashboard extends Component {
    static template = "isil_dashboard.Dashboard";

    setup() {
        this.rpc    = useService("rpc");
        this.action = useService("action");
        this.state  = useState({
            loading:  true,
            spinning: false,
            sales:    { total_orders: 0, total_revenue: 0, pending_invoice: 0 },
            stock:    { total_products: 0, active_alerts: 0, total_value: 0 },
            mfg:      { orders_in_progress: 0, pending_qc: 0 },
            hr:       { total_employees: 0, pending_requests: 0 },
            objectives: [],
        });
        // Bind so template arrow-function calls don't lose 'this'
        this.go      = this.go.bind(this);
        this.refresh = this.refresh.bind(this);
        onWillStart(() => this._load());
    }

    async _load() {
        try {
            const data = await this.rpc("/isil_dashboard/get_live_data");
            Object.assign(this.state, data, { loading: false });
        } catch {
            this.state.loading = false;
        }
    }

    async refresh() {
        if (this.state.spinning) return;
        this.state.spinning = true;
        try {
            const data = await this.rpc("/isil_dashboard/get_live_data");
            Object.assign(this.state, data);
        } finally {
            this.state.spinning = false;
        }
    }

    get currentDate() {
        return new Date().toLocaleDateString("en-GB", {
            weekday: "long", year: "numeric", month: "long", day: "numeric",
        });
    }

    fmt(val) {
        if (val >= 1_000_000) return (val / 1_000_000).toFixed(1) + " M";
        if (val >= 1_000)     return (val / 1_000).toFixed(1) + " K";
        return Math.round(val).toLocaleString();
    }

    objCls(status) {
        return { on_track: "db-obj-ok", at_risk: "db-obj-risk",
                 behind: "db-obj-behind", completed: "db-obj-done" }[status] || "";
    }

    objLabel(status) {
        return { on_track: "On Track", at_risk: "At Risk",
                 behind: "Behind", completed: "Done" }[status] || (status || "—");
    }

    go(module) {
        const routes = {
            sales:         "sale.action_quotations_with_onboarding",
            stock:         "isil_stock_traceability.action_stock_lots",
            manufacturing: "mrp.mrp_production_action",
            hr:            "isil_hr_advanced.action_hr_custom_employee",
        };
        if (routes[module]) this.action.doAction(routes[module]);
    }
}

registry.category("actions").add("isil_dashboard.client_action", IsilDashboard);
