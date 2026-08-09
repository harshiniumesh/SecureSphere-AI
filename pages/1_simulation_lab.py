"""
1_simulation_lab.py
Simulation Lab page for SecureSphere AI.
"""

import os
import tempfile
import streamlit as st
import plotly.graph_objects as go
import config
from core.risk_engine import RiskEngine
from core.timeline_builder import TimelineBuilder
from core.pdf_generator import PDFGenerator
from components.sidebar import render_sidebar

st.set_page_config(page_title=f"Simulation Lab | {config.PROJECT_NAME}", page_icon="🧪", layout="wide")
render_sidebar()

if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = None


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def get_timeline_icon(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["email", "phishing"]): return "📧"
    if any(w in t for w in ["credential", "login", "password"]): return "🔑"
    if any(w in t for w in ["lateral", "network", "spread"]): return "💻"
    if any(w in t for w in ["database", "access", "extract"]): return "📂"
    if any(w in t for w in ["exfiltration", "forward", "leak", "sale"]): return "📤"
    if any(w in t for w in ["ransomware", "encrypt", "payload"]): return "🔒"
    if any(w in t for w in ["halt", "freeze", "disrupt", "outage"]): return "🛑"
    if any(w in t for w in ["vulnerability", "exploit"]): return "🚨"
    return "⚠️"


# ==========================================
# PAGE HEADER
# ==========================================
st.title("🧪 Simulation Lab")
st.write(
    "Simulate enterprise cyber attacks by configuring the business profile and security controls. "
    "Run the simulation to generate an attack timeline, risk score, and financial impact estimate."
)
st.markdown("---")

left_col, right_col = st.columns([1, 1], gap="large")

# ==========================================
# LEFT PANEL: CONFIGURATION
# ==========================================
with left_col:
    with st.container(border=True):
        st.subheader("Scenario Configuration")
        persona = st.selectbox("Business Persona", options=list(config.BUSINESS_PERSONAS.keys()))
        attack_type = st.selectbox("Attack Type", options=config.ATTACK_TYPES)
        industry = st.selectbox("Industry", options=list(config.INDUSTRY_MULTIPLIERS.keys()))
        critical_asset = st.selectbox("Critical Asset", options=list(config.CRITICAL_ASSET_MULTIPLIERS.keys()))

        annual_revenue = st.number_input(
            "Annual Revenue ($)",
            min_value=config.SIMULATION_LIMITS["annual_revenue_min"],
            max_value=config.SIMULATION_LIMITS["annual_revenue_max"],
            value=config.DEFAULT_SIMULATION["annual_revenue"],
            step=100_000,
            format="%d"
        )
        employee_count = st.number_input(
            "Employee Count",
            min_value=config.SIMULATION_LIMITS["employee_count_min"],
            max_value=config.SIMULATION_LIMITS["employee_count_max"],
            value=config.DEFAULT_SIMULATION["employee_count"],
            step=10,
            format="%d"
        )

    with st.container(border=True):
        st.subheader("Security Controls")
        mfa_enabled = st.checkbox("MFA Enabled", value=config.DEFAULT_SIMULATION["controls"]["mfa_enabled"])
        firewall_active = st.checkbox("Firewall Active", value=config.DEFAULT_SIMULATION["controls"]["firewall_active"])
        edr_deployed = st.checkbox("EDR Deployed", value=config.DEFAULT_SIMULATION["controls"]["edr_deployed"])
        immutable_backups = st.checkbox("Immutable Backups",
                                        value=config.DEFAULT_SIMULATION["controls"]["immutable_backups"])
        automated_patching = st.checkbox("Automated Patching",
                                         value=config.DEFAULT_SIMULATION["controls"]["automated_patching"])
        employee_training = st.checkbox("Employee Training",
                                        value=config.DEFAULT_SIMULATION["controls"]["employee_training"])

    st.write("")
    if st.button("Run Simulation", type="primary", use_container_width=True):
        controls = {
            "mfa_enabled": mfa_enabled,
            "firewall_active": firewall_active,
            "edr_deployed": edr_deployed,
            "immutable_backups": immutable_backups,
            "automated_patching": automated_patching,
            "employee_training": employee_training
        }

        risk_engine = RiskEngine()
        timeline_builder = TimelineBuilder()

        risk_score = risk_engine.calculate_risk_score(controls)
        readiness = risk_engine.get_readiness_level(risk_score)
        min_loss, max_loss = risk_engine.estimate_financial_loss(
            annual_revenue=annual_revenue, industry=industry,
            attack_type=attack_type, critical_asset=critical_asset
        )
        timeline = timeline_builder.build_timeline(attack_type)

        st.session_state.simulation_results = {
            "persona": persona,
            "attack_type": attack_type,
            "industry": industry,
            "critical_asset": critical_asset,
            "annual_revenue": annual_revenue,
            "employee_count": employee_count,
            "controls": controls,
            "risk_score": risk_score,
            "readiness": readiness,
            "min_loss": min_loss,
            "max_loss": max_loss,
            "timeline": timeline
        }

# ==========================================
# RIGHT PANEL: RESULTS & TIMELINE
# ==========================================
with right_col:
    results = st.session_state.simulation_results

    # 1. Executive Summary & Charts
    with st.container(border=True):
        st.subheader("Executive Summary")
        if results:
            # Visualizations Layout
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                # Plotly Risk Gauge
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=results['risk_score'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': config.COLORS["primary"]},
                        'steps': [
                            {'range': [0, 20], 'color': config.COLORS["success"]},
                            {'range': [20, 60], 'color': config.COLORS["warning"]},
                            {'range': [60, 100], 'color': config.COLORS["critical"]}
                        ]
                    }
                ))
                fig_gauge.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)

            with chart_col2:
                # Plotly Donut Chart (Enabled vs Disabled)
                controls_dict = results['controls']
                active_count = sum(controls_dict.values())
                inactive_count = len(controls_dict) - active_count

                fig_donut = go.Figure(data=[go.Pie(
                    labels=['Enabled', 'Disabled'],
                    values=[active_count, inactive_count],
                    hole=.6,
                    marker_colors=[config.COLORS["success"], config.COLORS["critical"]]
                )])
                fig_donut.update_layout(height=200, margin=dict(l=0, r=0, t=20, b=20))
                st.plotly_chart(fig_donut, use_container_width=True)

            # AI-Style Executive Summary Text
            disabled = [k.replace('_', ' ').title() for k, v in controls_dict.items() if not v]

            summary = f"Overall Cyber Readiness is **{results['readiness']['label']}**.\n\n"
            if disabled:
                summary += f"Primary exposure comes from missing **{', '.join(disabled)}**.\n\n"
            else:
                summary += "All core security controls are active, minimizing primary exposure.\n\n"

            summary += f"Estimated financial impact ranges between **${results['min_loss']:,.0f}** and **${results['max_loss']:,.0f}**.\n\n"

            if disabled:
                summary += f"Recommended next investment: **Enable {disabled[0]}**."

            st.info(summary)
        else:
            st.markdown(f"**Cyber Readiness:** ★★★☆☆")
            st.markdown(f"**Risk Score:** 0 / 100")
            st.markdown(f"**Estimated Financial Loss:** $0")

    # 2. Dynamic What-If Optimization
    with st.container(border=True):
        st.subheader("What-If Optimization")
        if results:
            recommendations_found = False
            for control, is_active in results["controls"].items():
                if not is_active:
                    recommendations_found = True
                    weight = config.CONTROL_WEIGHTS[control]
                    st.markdown(f"""
                    **Enable {control.replace('_', ' ').title()}**  
                    Risk decreases by {weight}
                    """)

            if not recommendations_found:
                st.success(
                    "All security controls are currently enabled. No further optimization required at this level.")
        else:
            st.markdown("""
            > **If you enable [ MFA ]:**  
            > Readiness becomes ★★★★☆ (Strong)
            >
            > **If you deploy [ EDR ]:**  
            > Risk Score drops by 12 points
            """)

    # 3. Attack Story Timeline
    with st.container(border=True):
        st.subheader("Attack Story Timeline")
        if results:
            for i, event in enumerate(results["timeline"]):
                icon = get_timeline_icon(event['description'] + " " + event['title'])
                st.markdown(f"**{icon} {event['day']}**  \n**{event['title']}:** {event['description']}")
                if i < len(results["timeline"]) - 1:
                    st.markdown("---")
        else:
            st.markdown("""
            **Day 1**  
            Placeholder event: Initial compromise vector executed.

            ---
            **Day 3**  
            Placeholder event: Attacker moves laterally through the network.

            ---
            **Day 5**  
            Placeholder event: Critical asset accessed and compromised.

            ---
            **Day 7**  
            Placeholder event: Business operations disrupted.
            """)

    # 4. Download PDF Report Button
    st.write("")
    if results:
        simulation_data = {
            "company_name": config.DEFAULT_SIMULATION["company_name"],
            "business_persona": results["persona"],
            "industry": results["industry"],
            "annual_revenue": results["annual_revenue"],
            "employee_count": results["employee_count"],
            "critical_asset": results["critical_asset"],
            "attack_type": results["attack_type"],
            "risk_score": results["risk_score"],
            "readiness_stars": results["readiness"]["stars_display"],
            "financial_loss_range": (results["min_loss"], results["max_loss"]),
            "timeline": results["timeline"]
        }

        pdf_generator = PDFGenerator()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf_path = tmp_file.name

        pdf_generator.generate_report(pdf_path, simulation_data)
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        os.remove(pdf_path)

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"SecureSphere_{results['attack_type'].replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.button("Download PDF Report", disabled=True, use_container_width=True)