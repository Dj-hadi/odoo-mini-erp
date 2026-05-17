/** @odoo-module **/
import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const SLIDE_MS   = 4000;
const MOD_COLORS = [
    "radial-gradient(circle at 38% 32%,#a5b4fc,#6366f1 60%,#312e81 100%)",
    "radial-gradient(circle at 38% 32%,#99f6e4,#0d9488 60%,#042f2e 100%)",
    "radial-gradient(circle at 38% 32%,#fde68a,#d97706 60%,#7c2d12 100%)",
    "radial-gradient(circle at 38% 32%,#ddd6fe,#7c3aed 60%,#2e1065 100%)",
    "radial-gradient(circle at 38% 32%,#a7f3d0,#059669 60%,#052e16 100%)",
    "radial-gradient(circle at 38% 32%,#e2e8f0,#64748b 60%,#0f172a 100%)",
];

// Each module card maps to its Odoo action XML ID
const MODULE_ACTIONS = {
    hr:            "isil_hr_advanced.action_hr_custom_employee",
    stock:         "isil_stock_traceability.action_stock_lots",
    manufacturing: "mrp.mrp_production_action",
    sales:         "sale.action_quotations_with_onboarding",
    finance:       "isil_financial_analytics.action_isil_finance_gl",
    dashboard:     "isil_dashboard.action_dashboard_client",
};

export class IsilWelcome extends Component {
    static template = "isil_welcome.Welcome";

    setup() {
        this.actionService = useService("action");
        this.state = useState({ current: 0, exiting: false });
        this._ticker    = null;
        this._handleKey = null;

        this.goToSlide  = this.goToSlide.bind(this);
        this.skipIntro  = this.skipIntro.bind(this);
        this.enter      = this.enter.bind(this);
        this.goToModule = this.goToModule.bind(this);

        onMounted(() => {
            this._mkParticles("isl-p1", 20, "isl-orb");
            this._mkParticles("isl-p2", 14, "isl-mdot", MOD_COLORS);
            this._mkParticles("isl-p3", 22, "isl-sparkle");

            this._handleKey = (e) => {
                if (e.key === "ArrowRight" || e.key === " ")
                    this.goToSlide(Math.min(this.state.current + 1, 2));
                if (e.key === "ArrowLeft")
                    this.goToSlide(Math.max(this.state.current - 1, 0));
            };
            document.addEventListener("keydown", this._handleKey);
            this.goToSlide(0);
        });

        onWillUnmount(() => {
            clearTimeout(this._ticker);
            if (this._handleKey) document.removeEventListener("keydown", this._handleKey);
        });
    }

    _mkParticles(id, count, cls, colors) {
        const wrap = document.getElementById(id);
        if (!wrap) return;
        for (let i = 0; i < count; i++) {
            const el  = document.createElement("div");
            el.className = cls;
            const sz  = 30 + Math.random() * 90;
            const col = colors ? colors[Math.floor(Math.random() * colors.length)] : null;
            el.style.cssText = `
                width:${sz}px; height:${sz}px;
                left:${Math.random() * 93}%;
                top:${Math.random()  * 93}%;
                opacity:${0.1 + Math.random() * 0.38};
                animation-duration:${3.5 + Math.random() * 4}s;
                animation-delay:${Math.random() * -6}s;
                ${col ? `background:${col};` : ""}
            `;
            wrap.appendChild(el);
        }
    }

    _sweepProgress() {
        const fill = document.getElementById("isl-prog-fill");
        if (!fill) return;
        fill.style.transition = "none";
        fill.style.width = "0%";
        requestAnimationFrame(() => requestAnimationFrame(() => {
            fill.style.transition = `width ${SLIDE_MS}ms linear`;
            fill.style.width = "100%";
        }));
    }

    goToSlide(n) {
        clearTimeout(this._ticker);
        if (this.state.current === 1)
            document.querySelectorAll(".isl-mcard").forEach(c => c.classList.remove("isl-vis"));

        this.state.current = n;

        if (n === 1) {
            setTimeout(() => {
                document.querySelectorAll(".isl-mcard").forEach((c, i) =>
                    setTimeout(() => c.classList.add("isl-vis"), i * 90));
            }, 350);
        }

        this._sweepProgress();

        if (n < 2) this._ticker = setTimeout(() => this.goToSlide(n + 1), SLIDE_MS);
    }

    // Navigate to a specific module, fading the overlay out first
    goToModule(moduleKey) {
        clearTimeout(this._ticker);
        this.state.exiting = true;
        const actionId = MODULE_ACTIONS[moduleKey];
        setTimeout(() => {
            this.actionService.doAction(actionId);
        }, 700);
    }

    skipIntro() { this.goToSlide(2); }

    // "Enter Platform" → go to the ISIL Dashboard
    enter() {
        clearTimeout(this._ticker);
        this.state.exiting = true;
        setTimeout(() => {
            this.actionService.doAction("isil_dashboard.action_dashboard_client");
        }, 700);
    }

    get isLast() { return this.state.current === 2; }
}

registry.category("actions").add("isil_welcome.action", IsilWelcome);
