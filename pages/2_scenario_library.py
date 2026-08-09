"""
2_scenario_library.py
Scenario Library page for SecureSphere AI.
"""

import streamlit as st
import config
from data.db_manager import DatabaseManager
from components.sidebar import render_sidebar

st.set_page_config(page_title=f"Scenario Library | {config.PROJECT_NAME}", page_icon="🏢", layout="wide")
render_sidebar()

# ==========================================
# PAGE HEADER
# ==========================================
st.title("🏢 Scenario Library")
st.write(
    "Explore predefined enterprise environments. Loading a scenario will automatically "
    "pre-fill realistic company values and security baselines in the Simulation Lab."
)
st.markdown("---")


# ==========================================
# DATA FETCHING
# ==========================================
@st.cache_data
def load_scenarios() -> list:
    db = DatabaseManager()
    try:
        rows = db.fetch_all("SELECT * FROM scenarios ORDER BY title ASC")
        return [dict(row) for row in rows]
    except Exception as e:
        st.error(f"Failed to load scenarios: {e}")
        return []


scenarios = load_scenarios()

if not scenarios:
    st.info("No scenarios found. Please ensure the database has been seeded via the Home page.")
    st.stop()

# ==========================================
# FILTERS
# ==========================================
industries = sorted(list(set(scenario["industry"] for scenario in scenarios)))
industries.insert(0, "All Industries")

selected_industry = st.selectbox("🏭 Filter by Industry", industries)

filtered_scenarios = [s for s in scenarios if
                      selected_industry == "All Industries" or s["industry"] == selected_industry]

st.caption(f"**Showing {len(filtered_scenarios)} of {len(scenarios)} scenarios**")
st.write("")

# ==========================================
# UI: RESPONSIVE CARD LAYOUT
# ==========================================
if not filtered_scenarios:
    st.warning("No scenarios match your criteria.")
else:
    cols = st.columns(2)

    for index, scenario in enumerate(filtered_scenarios):
        col = cols[index % 2]
        with col:
            with st.container(border=True):
                # Calculate basic executive metrics
                industry_mult = config.INDUSTRY_MULTIPLIERS.get(scenario["industry"], 1.0)
                likelihood = "High" if industry_mult > 2.0 else "Medium" if industry_mult > 1.5 else "Low"
                maturity = "High" if scenario["default_size"] > 1000 else "Moderate" if scenario[
                                                                                            "default_size"] > 100 else "Low"

                st.subheader(f"🏢 {scenario['title']}")
                st.markdown(
                    f"<span style='background-color:{config.COLORS['surface']}; padding: 4px 8px; border-radius: 4px; color: {config.COLORS['primary']}; font-weight: bold;'>{scenario['industry'].upper()}</span>",
                    unsafe_allow_html=True)
                st.write("")

                st.markdown(f"**Company Size:** {scenario['default_size']:,} Employees")
                st.markdown(f"**Annual Revenue:** ${scenario['default_revenue']:,.0f}")
                st.markdown(f"**Primary Target Asset:** {scenario['critical_asset']}")

                st.markdown("---")
                sub_col1, sub_col2 = st.columns(2)
                sub_col1.markdown(f"**Target Likelihood:** {likelihood}")
                sub_col2.markdown(f"**Expected Maturity:** {maturity}")

                st.write("")

                # Session state for button toggle logic
                btn_key = f"explore_{scenario['scenario_id']}"
                if btn_key not in st.session_state:
                    st.session_state[btn_key] = False


                def toggle_explore(key):
                    st.session_state[key] = not st.session_state[key]


                # Functional Explore Button
                st.button(
                    "Close Details" if st.session_state[btn_key] else "Explore Scenario",
                    key=f"btn_{scenario['scenario_id']}",
                    on_click=toggle_explore,
                    args=(btn_key,),
                    use_container_width=True
                )

                # Expandable Panel Content
                if st.session_state[btn_key]:
                    # Determine common attack based on industry
                    if scenario["industry"] in ["Healthcare", "Manufacturing"]:
                        common_attack = "Ransomware"
                    elif scenario["industry"] in ["Finance", "Retail"]:
                        common_attack = "Data Breach"
                    elif scenario["industry"] in ["Technology"]:
                        common_attack = "Supply Chain Attack"
                    else:
                        common_attack = "Phishing"

                    # Calculate impacts using config multipliers
                    ass_mult = config.CRITICAL_ASSET_MULTIPLIERS.get(scenario["critical_asset"], 1.0)
                    att_mult = config.ATTACK_TYPE_MULTIPLIERS.get(common_attack, 1.0)

                    base_impact = scenario["default_revenue"] * 0.005
                    calculated_impact = base_impact * industry_mult * att_mult * ass_mult
                    min_loss = calculated_impact * 0.7
                    max_loss = calculated_impact * 1.4

                    # Sort controls by weight to get the top 3 recommendations
                    sorted_controls = sorted(config.CONTROL_WEIGHTS.items(), key=lambda item: item[1], reverse=True)
                    top_controls = [ctrl[0].replace('_', ' ').title() for ctrl in sorted_controls[:3]]

                    # Display Insights Panel
                    st.markdown("---")
                    st.markdown("##### 🔍 Scenario Insights")
                    st.markdown(f"**Industry Risk Level:** {likelihood}")
                    st.markdown(f"**Most Common Attack:** {common_attack}")
                    st.markdown(
                        f"**Estimated Annual Loss:** <span style='color: {config.COLORS['critical']}; font-weight:bold;'>${min_loss:,.0f} - ${max_loss:,.0f}</span>",
                        unsafe_allow_html=True)
                    st.markdown(f"**Critical Asset Importance:** High ({ass_mult}x Impact)")
                    st.markdown(f"**Recommended Security Controls:** {', '.join(top_controls)}")