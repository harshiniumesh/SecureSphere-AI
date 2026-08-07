"""
sidebar.py
Reusable sidebar component for SecureSphere AI.
Handles custom navigation, platform status, and metadata styling with adaptive themes.
"""

import streamlit as st
import config


def render_sidebar():
    """Renders the custom enterprise sidebar across all pages."""

    # SVG Logo using currentColor for Dark/Light mode adaptability
    svg_logo = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="45" height="45" style="flex-shrink: 0;">
      <circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="4"/>
      <ellipse cx="50" cy="50" rx="20" ry="40" fill="none" stroke="currentColor" stroke-width="4"/>
      <ellipse cx="50" cy="50" rx="40" ry="20" fill="none" stroke="currentColor" stroke-width="4"/>
      <circle cx="50" cy="10" r="5" fill="#00B4D8"/>
      <circle cx="50" cy="90" r="5" fill="#00B4D8"/>
      <circle cx="10" cy="50" r="5" fill="#00B4D8"/>
      <circle cx="90" cy="50" r="5" fill="#00B4D8"/>
      <circle cx="50" cy="50" r="7" fill="#00B4D8"/>
      <circle cx="30" cy="50" r="4" fill="currentColor"/>
      <circle cx="70" cy="50" r="4" fill="currentColor"/>
      <circle cx="50" cy="30" r="4" fill="currentColor"/>
      <circle cx="50" cy="70" r="4" fill="currentColor"/>
    </svg>
    """

    # Injecting CSS to customize native Streamlit components and apply adaptive themes
    st.markdown(
        """
        <style>
            /* Hide default Streamlit sidebar navigation */
            [data-testid="stSidebarNav"] { 
                display: none !important; 
            }

            /* Modern Navigation Cards */
            [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
                background-color: var(--secondary-background-color);
                border-radius: 8px;
                padding: 10px 15px;
                margin-bottom: 8px;
                border: 1px solid rgba(128, 128, 128, 0.1);
                transition: all 0.2s ease-in-out;
                color: var(--text-color);
                font-weight: 500;
            }

            /* Hover Effect */
            [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
                background-color: rgba(0, 180, 216, 0.08);
                border: 1px solid rgba(0, 180, 216, 0.4);
                transform: translateX(4px);
            }

            /* Active Page Highlight */
            [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][data-active="true"],
            [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
                background-color: rgba(0, 180, 216, 0.12);
                border-left: 4px solid #00B4D8;
                border-right: 1px solid rgba(0, 180, 216, 0.1);
                border-top: 1px solid rgba(0, 180, 216, 0.1);
                border-bottom: 1px solid rgba(0, 180, 216, 0.1);
            }

            /* Hide the default st.page_link underline */
            [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p {
                text-decoration: none !important;
            }

            hr {
                margin-top: 1.5rem;
                margin-bottom: 1.5rem;
                border-color: rgba(128, 128, 128, 0.2);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        # 1 & 2. Branded Premium Header
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px; margin-top: 10px;">
                <div style="color: var(--text-color);">{svg_logo}</div>
                <div style="line-height: 1.3;">
                    <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-color);">SecureSphere AI</div>
                    <div style="font-size: 0.75rem; font-weight: 600; color: #00B4D8; text-transform: uppercase; letter-spacing: 0.5px;">Enterprise Cyber Intelligence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 4. Interactive Rounded Navigation Cards
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_simulation_lab.py", label="Simulation Lab", icon="🧪")
        st.page_link("pages/2_scenario_library.py", label="Scenario Library", icon="🏢")
        st.page_link("pages/3_learning_center.py", label="Learning Center", icon="🎓")

        st.markdown("---")

        # 5. Platform Status Badges
        st.markdown(
            """
            <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-color); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;">Platform Status</div>

            <div style="background-color: var(--secondary-background-color); padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem; display: flex; align-items: center; border: 1px solid rgba(128,128,128,0.15); color: var(--text-color);">
                <span style="margin-right: 10px; font-size: 0.75rem;">🟢</span> Simulation Engine
            </div>

            <div style="background-color: var(--secondary-background-color); padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem; display: flex; align-items: center; border: 1px solid rgba(128,128,128,0.15); color: var(--text-color);">
                <span style="margin-right: 10px; font-size: 0.75rem;">🟢</span> Database
            </div>

            <div style="background-color: var(--secondary-background-color); padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem; display: flex; align-items: center; border: 1px solid rgba(128,128,128,0.15); color: var(--text-color);">
                <span style="margin-right: 10px; font-size: 0.75rem;">🟢</span> PDF Reports
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # 6. Project Information Card
        st.markdown(
            f"""
            <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-color); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;">Project Info</div>

            <div style="background-color: var(--secondary-background-color); padding: 15px; border-radius: 8px; font-size: 0.85rem; color: var(--text-color); border: 1px solid rgba(128,128,128,0.15); line-height: 1.6;">
                <strong>Version {config.APP_VERSION}</strong><br>
                <span style="opacity: 0.8;">{config.APP_AUTHOR}</span><br>
                <span style="opacity: 0.8;">{config.PROJECT_YEAR}</span>
            </div>
            """,
            unsafe_allow_html=True
        )