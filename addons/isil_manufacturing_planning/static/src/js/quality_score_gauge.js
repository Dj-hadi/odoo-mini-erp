/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const RADIUS = 36;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS; // ≈ 226.195

export class QualityScoreGauge extends Component {
    static template = "isil_manufacturing_planning.QualityScoreGauge";
    static props = { ...standardFieldProps };

    get score() {
        const v = this.props.record.data[this.props.name];
        return typeof v === "number" ? Math.max(0, Math.min(100, v)) : 0;
    }
    get gaugeClass() {
        if (this.score >= 70) return "qc-gauge-pass";
        if (this.score >= 50) return "qc-gauge-risk";
        return "qc-gauge-fail";
    }
    get strokeColor() {
        if (this.score >= 70) return "#10B981";
        if (this.score >= 50) return "#F59E0B";
        return "#EF4444";
    }
    get statusLabel() {
        if (this.score >= 70) return "Passed";
        if (this.score >= 50) return "At Risk";
        return "Failed";
    }
    get arcStyle() {
        const offset = CIRCUMFERENCE * (1 - this.score / 100);
        return [
            `stroke-dasharray: ${CIRCUMFERENCE.toFixed(3)}`,
            `stroke-dashoffset: ${CIRCUMFERENCE.toFixed(3)}`,
            `--arc-target: ${offset.toFixed(3)}`,
            "transform: rotate(-90deg)",
            "transform-origin: 40px 40px",
        ].join("; ");
    }
}

registry.category("fields").add("quality_score_gauge", {
    component: QualityScoreGauge,
    supportedTypes: ["float", "integer"],
});
