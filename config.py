"""
config.py
Central configuration file for SecureSphere AI.
Contains all constants, weights, multipliers, UI settings, and scenarios.
"""

# ==========================================
# 1. APPLICATION METADATA
# ==========================================
PROJECT_NAME = "SecureSphere AI"
TAGLINE = "AI-Powered Enterprise Cyber Risk Simulator"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Harshini Umesh"
PROJECT_YEAR = "2026"
LICENSE = "MIT"

# ==========================================
# 2. CYBER RISK SCORING WEIGHTS
# ==========================================
RISK_SCORE = {
    "MIN": 0,
    "MAX": 100,
    "DEFAULT": 100
}

CONTROL_WEIGHTS = {
    "mfa_enabled": 15,
    "immutable_backups": 15,
    "edr_deployed": 12,
    "firewall_active": 10,
    "automated_patching": 10,
    "employee_training": 8
}

# ==========================================
# 3. CYBER READINESS STAR MAPPING
# ==========================================
READINESS_TIERS = [
    {"max_score": 20,  "stars": 5, "label": "Enterprise Ready", "stars_display": "★★★★★"},
    {"max_score": 40,  "stars": 4, "label": "Strong",           "stars_display": "★★★★☆"},
    {"max_score": 60,  "stars": 3, "label": "Moderate",         "stars_display": "★★★☆☆"},
    {"max_score": 80,  "stars": 2, "label": "Vulnerable",       "stars_display": "★★☆☆☆"},
    {"max_score": 100, "stars": 1, "label": "Critical",         "stars_display": "★☆☆☆☆"}
]

# ==========================================
# 4. SIMULATION CATEGORIES & PERSONAS
# ==========================================
ATTACK_TYPES = [
    "Phishing", "Ransomware", "Insider Threat",
    "Data Breach", "DDoS", "Supply Chain Attack"
]

BUSINESS_PERSONAS = {
    "CEO": "Focuses on financial loss, business downtime, and high-level ROI.",
    "IT Manager": "Focuses on infrastructure failure points and operational impact.",
    "Security Analyst": "Focuses on detailed technical jargon and control failures.",
    "Student": "Focuses on educational explanations and the 'why' behind the attack."
}

# ==========================================
# 5. DEFAULT SIMULATIONS & SCENARIOS
# ==========================================
DEFAULT_SIMULATION = {
    "company_name": "Demo Corp",
    "annual_revenue": 5_000_000,
    "employee_count": 100,
    "industry": "Technology",
    "critical_asset": "Customer PII",
    "controls": {
        "mfa_enabled": False,
        "immutable_backups": False,
        "edr_deployed": False,
        "firewall_active": True,
        "automated_patching": False,
        "employee_training": False
    }
}

SCENARIOS = {
    "Startup": {
        "company_name": "NextGen Innovate",
        "annual_revenue": 2_500_000,
        "employee_count": 35,
        "industry": "Technology",
        "critical_asset": "Source Code / IP"
    },
    "Hospital": {
        "company_name": "Regional Medical Center",
        "annual_revenue": 85_000_000,
        "employee_count": 1200,
        "industry": "Healthcare",
        "critical_asset": "Customer PII"
    },
    "Bank": {
        "company_name": "Global Trust Bank",
        "annual_revenue": 500_000_000,
        "employee_count": 3500,
        "industry": "Finance",
        "critical_asset": "Financial Database"
    },
    "School": {
        "company_name": "Valley High School",
        "annual_revenue": 15_000_000,
        "employee_count": 150,
        "industry": "Education",
        "critical_asset": "Customer PII"
    },
    "Manufacturing Company": {
        "company_name": "Apex Industrial",
        "annual_revenue": 120_000_000,
        "employee_count": 850,
        "industry": "Manufacturing",
        "critical_asset": "Operational Technology (OT)"
    },
    "IT Services Company": {
        "company_name": "CloudSync Solutions",
        "annual_revenue": 45_000_000,
        "employee_count": 300,
        "industry": "Technology",
        "critical_asset": "Internal Memos"
    },
    "E-commerce Company": {
        "company_name": "ShopStream",
        "annual_revenue": 60_000_000,
        "employee_count": 450,
        "industry": "Retail",
        "critical_asset": "Customer PII"
    }
}

# ==========================================
# 6. LIMITS & MULTIPLIERS
# ==========================================
SIMULATION_LIMITS = {
    "employee_count_min": 1,
    "employee_count_max": 100_000,
    "annual_revenue_min": 0,
    "annual_revenue_max": 10_000_000_000
}

INDUSTRY_MULTIPLIERS = {
    "Healthcare": 2.5, "Finance": 2.8, "Technology": 1.8,
    "Retail": 1.5, "Education": 1.2, "Manufacturing": 2.0,
    "Government": 2.6, "Insurance": 2.7, "Telecommunications": 2.4
}

CRITICAL_ASSET_MULTIPLIERS = {
    "Customer PII": 2.5, "Financial Database": 2.0,
    "Source Code / IP": 1.8, "Internal Memos": 0.5,
    "Operational Technology (OT)": 2.2
}

ATTACK_TYPE_MULTIPLIERS = {
    "Ransomware": 3.0, "Data Breach": 2.5, "Supply Chain Attack": 2.2,
    "DDoS": 1.2, "Insider Threat": 1.8, "Phishing": 1.5
}

# ==========================================
# 7. UI CONSTANTS & DESIGN SYSTEM
# ==========================================
COLORS = {
    "background": "#FFFFFF",    # White Enterprise Theme
    "surface": "#F8FAFC",
    "primary": "#0A192F",       # Navy
    "accent": "#00B4D8",        # Cyan
    "success": "#10B981",       # Green
    "warning": "#F59E0B",       # Orange
    "critical": "#EF4444",      # Red
    "text_main": "#0F172A",
    "text_muted": "#64748B"
}