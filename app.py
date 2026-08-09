"""
app.py
Main entry point for the SecureSphere AI application.
Initializes the database, handles automatic seeding, and renders the premium Home Page.
"""
import streamlit.components.v1 as components
import streamlit as st
import config
from data.db_manager import DatabaseManager
from data.seed_data import run_seeder
from components.sidebar import render_sidebar

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title=config.PROJECT_NAME,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. APPLICATION STARTUP (DB INITIALIZATION)
# ==========================================
@st.cache_resource
def initialize_system() -> DatabaseManager:
    db = DatabaseManager()
    db.initialize_database()
    run_seeder()
    return db


db_manager = initialize_system()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
render_sidebar()
# ==========================================
# 4. HOME PAGE CONTENT
# ==========================================
def render_home_page():

    # ------------------------------------------------
    # 1. HERO SECTION
    # ------------------------------------------------
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    # ------------------------------------------------
    # HERO TITLE
    # ------------------------------------------------
    # ------------------------------------------------
    # HERO TITLE (Theme-Adaptive)
    # ------------------------------------------------
    # ------------------------------------------------
    # HERO TITLE
    # ------------------------------------------------
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
        <div style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-top: 5px; margin-bottom: 5px; color: var(--text-color);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="52" height="52" style="flex-shrink: 0;">
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
            <h1 style="margin: 0; padding: 0; font-family: 'Space Grotesk', sans-serif; font-size: 50px; font-weight: 700; letter-spacing: -1px; color: var(--text-color); line-height: 1.1;">
                SecureSphere AI
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Subtitle
    st.markdown(
        """
        <h3 style="
            text-align:center;
            color:#94A3B8;
            font-size:1.5rem;
            font-weight:500;
            margin-top:4px;
            margin-bottom:10px;">
            Enterprise Cyber Risk Intelligence Platform
        </h3>
        """,
        unsafe_allow_html=True,
    )

    # Tagline
    st.markdown(
        """
        <h2 style="
            text-align:center;
            color:#00B4D8;
            letter-spacing:4px;
            font-weight:700;
            margin-top:0px;
            margin-bottom:10px;">
            PREDICT • SIMULATE • PROTECT
        </h2>
        """,
        unsafe_allow_html=True,
    )

    # Description
    st.markdown(
        """
        <p style="
            text-align:center;
            font-size:1.15rem;
            color:#94A3B8;
            max-width:800px;
            margin:0 auto 10px auto;
            line-height:1.6;">
            AI-powered enterprise platform for cyber risk assessment,
            intelligent attack simulation, financial impact analysis,
            and executive-ready reporting.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------
    # ------------------------------------------------
    # ACTION BUTTONS
    # ------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("# 🧪")
            st.subheader("Simulation Lab")
            st.write("Run a complete enterprise cyber attack simulation.")
            st.write("")
            if st.button("Launch Simulation", use_container_width=True, type="primary"):
                st.switch_page("pages/1_simulation_lab.py")

    with col2:
        with st.container(border=True):
            st.markdown("# 🏢")
            st.subheader("Scenario Library")
            st.write("Explore realistic enterprise environments.")
            st.write("")
            if st.button("View Scenarios", use_container_width=True, type="primary"):
                st.switch_page("pages/2_scenario_library.py")

    with col3:
        with st.container(border=True):
            st.markdown("# 🎓")
            st.subheader("Learning Center")
            st.write("Learn cybersecurity concepts interactively.")
            st.write("")
            if st.button("Start Learning", use_container_width=True, type="primary"):
                st.switch_page("pages/3_learning_center.py")

    st.markdown("---")

    # ------------------------------------------------
    # ------------------------------------------------
    # PLATFORM STATISTICS
    # ------------------------------------------------
    st.subheader("Platform Statistics")

    # Calculate Metrics dynamically
    num_scenarios = len(config.SCENARIOS)
    num_attack_types = len(config.ATTACK_TYPES)
    num_personas = len(config.BUSINESS_PERSONAS)

    # Fetch Learning Topics count from the database
    try:
        topic_row = db_manager.fetch_one("SELECT COUNT(*) as count FROM learning_topics")
        num_learning_topics = topic_row["count"] if topic_row else 0
    except Exception:
        num_learning_topics = 0

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        with st.container(border=True):
            st.markdown(
                f"""
                    <div style='text-align: center;'>
                        <h1 style='margin-bottom: 0px;'>🏢</h1>
                        <h1 style='margin-top: 0px; font-size: 3em;'>{num_scenarios}+</h1>
                        <p style='margin-bottom: 0px; font-size: 1.1em;'><b>Enterprise Scenarios</b></p>
                        <p style='color: gray; font-size: 0.9em; margin-top: 0px;'>Industry Templates</p>
                    </div>
                    """,
                unsafe_allow_html=True
            )

    with stat2:
        with st.container(border=True):
            st.markdown(
                f"""
                    <div style='text-align: center;'>
                        <h1 style='margin-bottom: 0px;'>⚔️</h1>
                        <h1 style='margin-top: 0px; font-size: 3em;'>{num_attack_types}</h1>
                        <p style='margin-bottom: 0px; font-size: 1.1em;'><b>Threat Simulations</b></p>
                        <p style='color: gray; font-size: 0.9em; margin-top: 0px;'>Attack Library</p>
                    </div>
                    """,
                unsafe_allow_html=True
            )

    with stat3:
        with st.container(border=True):
            st.markdown(
                """
                <div style='text-align: center;'>
                    <h1 style='margin-bottom: 0px;'>🛡️</h1>
                    <h1 style='margin-top: 0px; font-size: 3em;'>6</h1>
                    <p style='margin-bottom: 0px; font-size: 1.1em;'><b>Security Controls</b></p>
                    <p style='color: gray; font-size: 0.9em; margin-top: 0px;'>Defense Layers</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with stat4:
        with st.container(border=True):
            st.markdown(
                """
                <div style='text-align: center;'>
                    <h1 style='margin-bottom: 0px;'>📄</h1>
                    <h1 style='margin-top: 0px; font-size: 3em;'>PDF</h1>
                    <p style='margin-bottom: 0px; font-size: 1.1em;'><b>Executive Reports</b></p>
                    <p style='color: gray; font-size: 0.9em; margin-top: 0px;'>Board Ready</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ------------------------------------------------
    # PLATFORM CAPABILITIES
    # ------------------------------------------------
    st.subheader("Platform Capabilities")

    cap1, cap2, cap3 = st.columns(3)

    with cap1:
        with st.container(border=True):
            st.markdown("#### 🧪 Simulation Lab")
            st.write("Interactive cyber attack simulator")
        with st.container(border=True):
            st.markdown("#### 🏢 Scenario Library")
            st.write("Industry-specific simulations")

    with cap2:
        with st.container(border=True):
            st.markdown("#### 📊 AI Risk Analytics")
            st.write("Dynamic cyber risk scoring")
        with st.container(border=True):
            st.markdown("#### 🛡️ Security Controls")
            st.write("Evaluate enterprise defenses")

    with cap3:
        with st.container(border=True):
            st.markdown("#### 📄 Executive Reports")
            st.write("Board-ready PDF reporting")
        with st.container(border=True):
            st.markdown("#### 🎓 Learning Center")
            st.write("Interactive cyber awareness")

    st.markdown("---")

    # ------------------------------------------------
    # PLATFORM STATUS
    # ------------------------------------------------
    st.subheader("Platform Status")

    status1, status2, status3, status4, status5 = st.columns(5)

    with status1:
        with st.container(border=True):
            st.write("🟢 Simulation Engine Ready")
    with status2:
        with st.container(border=True):
            st.write("🟢 Database Connected")
    with status3:
        with st.container(border=True):
            st.write("🟢 PDF Reporting Available")
    with status4:
        with st.container(border=True):
            st.write("🟢 Scenario Library Loaded")
    with status5:
        with st.container(border=True):
            st.write("🟢 Learning Modules Ready")


render_home_page()

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #00B4D8; font-size: 0.95em; padding: 10px 0;'>
        <strong>🛡️ {config.PROJECT_NAME} © {config.PROJECT_YEAR}</strong><br>
        <span style='font-size: 0.9em;'>AI-Powered Enterprise Cyber Risk Simulator</span><br>
        <span style='font-size: 0.85em; margin-top: 5px; display: inline-block;'>Built with Python • Streamlit • SQLite • Plotly • ReportLab</span>
    </div>
    """,
    unsafe_allow_html=True
)