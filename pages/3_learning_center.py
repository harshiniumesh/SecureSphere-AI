"""
3_learning_center.py
Interactive educational hub for SecureSphere AI.
"""

import random
import streamlit as st
from data.db_manager import DatabaseManager
import config
from components.sidebar import render_sidebar

st.set_page_config(page_title=f"Learning Center | {config.PROJECT_NAME}", page_icon="🎓", layout="wide")
render_sidebar()

# ==========================================
# EXTENDED KNOWLEDGE MAPPINGS
# ==========================================
EXTENDED_DATA = {
    "Multi-Factor Authentication": {
        "example": "2021 Colonial Pipeline attack could have been prevented with MFA on their VPN.",
        "prevention": "Enforce FIDO2 or app-based tokens across all external portals.",
        "takeaway": "Passwords alone are functionally obsolete.",
        "severity": "Critical", "mitre": "TA0006 - Credential Access"
    },
    "Firewalls": {
        "example": "Target's 2013 breach involved lateral movement that internal firewalls failed to segment.",
        "prevention": "Implement Zero Trust Network Access (ZTNA) and strict port rules.",
        "takeaway": "Perimeter defense is necessary but insufficient without internal segmentation.",
        "severity": "High", "mitre": "TA0008 - Lateral Movement"
    },
    "Endpoint Protection": {
        "example": "SolarWinds hackers bypassed traditional AV, requiring EDR behavioral analysis to detect.",
        "prevention": "Deploy NGAV and EDR agents on all corporate devices.",
        "takeaway": "Behavioral detection catches what signature-based AV misses.",
        "severity": "Critical", "mitre": "TA0005 - Defense Evasion"
    },
    "Patch Management": {
        "example": "Equifax's 2017 breach was caused by an unpatched Apache Struts vulnerability.",
        "prevention": "Automate patch deployment for critical CVEs within 48 hours.",
        "takeaway": "Delaying patches is equivalent to leaving the front door open.",
        "severity": "High", "mitre": "TA0001 - Initial Access"
    },
    "Phishing": {
        "example": "RSA Security was breached in 2011 via a malicious Excel spreadsheet emailed to staff.",
        "prevention": "Deploy anti-phishing gateways and conduct weekly simulation tests.",
        "takeaway": "Human psychology is the hardest vulnerability to patch.",
        "severity": "Critical", "mitre": "TA0001 - Initial Access"
    },
    "Password Hygiene": {
        "example": "The 2012 LinkedIn breach exposed millions of weak, reused passwords.",
        "prevention": "Mandate enterprise password managers and ban dictionary words.",
        "takeaway": "Complexity and uniqueness are non-negotiable.",
        "severity": "Medium", "mitre": "TA0006 - Credential Access"
    },
    "Cloud Security": {
        "example": "Capital One's 2019 breach resulted from a misconfigured AWS Web Application Firewall.",
        "prevention": "Use Cloud Security Posture Management (CSPM) tools.",
        "takeaway": "The cloud is only as secure as your configuration of it.",
        "severity": "High", "mitre": "TA0009 - Collection"
    },
    "Data Backups": {
        "example": "Maersk recovered from the NotPetya ransomware solely because of offline backups.",
        "prevention": "Implement the 3-2-1 backup rule with immutable storage.",
        "takeaway": "Backups are your ultimate fail-safe against ransomware.",
        "severity": "Critical", "mitre": "TA0040 - Impact"
    }
}

# ==========================================
# PAGE HEADER & STATS
# ==========================================
st.title("📚 Learning Center")
st.write("Explore foundational cybersecurity concepts, industry statistics, and interactive educational tools.")

col1, col2, col3 = st.columns(3)
with col1: st.metric("Initial Breaches via Phishing", "95%")
with col2: st.metric("Avg. Ransomware Recovery", "21 Days")
with col3: st.metric("Avg. Cost of Data Breach", "$4.45M")
st.markdown("---")


# ==========================================
# DATA FETCHING
# ==========================================
@st.cache_data
def load_topics():
    db = DatabaseManager()
    return [dict(row) for row in db.fetch_all("SELECT * FROM learning_topics ORDER BY title ASC")]


topics = load_topics()
if not topics:
    st.info("No learning topics found.")
    st.stop()

# ==========================================
# INTERACTIVE UI TABS
# ==========================================
tab_hub, tab_attacks, tab_controls, tab_quiz = st.tabs([
    "Knowledge Hub", "Cyber Attack Explorer", "Security Controls Explorer", "Cyber Knowledge Quiz"
])

# ----------------- KNOWLEDGE HUB -----------------
with tab_hub:
    categories = sorted(list(set(t["category"] for t in topics)))
    categories.insert(0, "All Categories")

    # Kept category filter, removed search bar
    selected_category = st.selectbox("📁 Filter Knowledge Cards by Category", categories)

    filtered_topics = [t for t in topics if selected_category == "All Categories" or t["category"] == selected_category]
    st.write("")

    for topic in filtered_topics:
        extended = EXTENDED_DATA.get(topic["title"], {})
        severity = extended.get("severity", "Medium")
        color = config.COLORS["critical"] if severity == "Critical" else config.COLORS[
            "warning"] if severity == "High" else config.COLORS["success"]

        with st.expander(f"📘 {topic['title']}"):
            st.markdown(
                f"**Category:** {topic['category']} | **Severity:** <span style='color:{color}; font-weight:bold;'>{severity}</span>",
                unsafe_allow_html=True)
            st.markdown(f"**Definition:** {topic['description']}")
            st.markdown(f"**Why it matters:** {topic['importance']}")

            if extended:
                st.markdown("---")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**🌍 Real-World Example:** {extended.get('example')}")
                    st.markdown(f"**🛡️ Prevention:** {extended.get('prevention')}")
                with col_b:
                    st.markdown(f"**🎯 MITRE ATT&CK:** {extended.get('mitre')}")
                    st.markdown(f"**💡 Key Takeaway:** {extended.get('takeaway')}")

# ----------------- SECTION 1: CYBER ATTACK EXPLORER -----------------
with tab_attacks:
    st.subheader("Cyber Attack Explorer")
    st.write("Select an attack vector to understand how it operates and impacts a business.")

    attack_data = {
        "Phishing": {
            "definition": "A social engineering attack where an attacker sends a fraudulent message designed to trick a person into revealing sensitive information or deploying malicious software.",
            "flow": "1. Deceptive Email Sent ➔ 2. User Clicks Malicious Link ➔ 3. Fake Login Portal ➔ 4. Credentials Harvested ➔ 5. Unauthorized Network Access",
            "impact": "Account compromises, data breaches, and serving as the initial foothold for ransomware deployment.",
            "prevent": "Conduct continuous employee training, enforce MFA, and implement email filtering gateways."
        },
        "Ransomware": {
            "definition": "Malicious software designed to block access to a computer system or encrypt its data until a sum of money is paid.",
            "flow": "1. Initial Access Gained ➔ 2. Lateral Movement & Reconnaissance ➔ 3. Data Exfiltration ➔ 4. Payload Execution & Encryption ➔ 5. Extortion Demand",
            "impact": "Complete operational halt, severe financial loss, reputational damage, and potential regulatory fines.",
            "prevent": "Maintain immutable and air-gapped backups, deploy EDR solutions, and ensure rapid patch management."
        },
        "DDoS": {
            "definition": "Distributed Denial of Service (DDoS) is a malicious attempt to disrupt the normal traffic of a targeted server, service, or network by overwhelming it with a flood of Internet traffic.",
            "flow": "1. Botnet Mobilized ➔ 2. Targeted Volumetric Traffic Sent ➔ 3. Bandwidth/Resources Exhausted ➔ 4. Legitimate Traffic Denied",
            "impact": "Loss of revenue from downtime, customer dissatisfaction, and disruption of critical web services.",
            "prevent": "Utilize cloud-based scrubbing centers, rate limiting, and web application firewalls (WAF)."
        },
        "Insider Threat": {
            "definition": "A security risk that originates from within the targeted organization, typically by a disgruntled or compromised employee or contractor.",
            "flow": "1. Authorized Access Granted ➔ 2. Privilege Escalation or Abuse ➔ 3. Data Harvesting ➔ 4. Covert Exfiltration or Sabotage",
            "impact": "Theft of intellectual property, exposure of confidential internal memos, and severe compliance violations.",
            "prevent": "Implement Zero Trust Network Access (ZTNA), Principle of Least Privilege, and User Entity Behavior Analytics (UEBA)."
        },
        "Supply Chain Attack": {
            "definition": "A cyberattack that seeks to damage an organization by targeting less-secure elements in the supply chain, such as third-party software vendors.",
            "flow": "1. Third-Party Vendor Compromised ➔ 2. Malicious Update Signed and Distributed ➔ 3. Target Installs Update ➔ 4. Backdoor Established",
            "impact": "Widespread compromise bypassing perimeter defenses, massive IP theft, and loss of vendor trust.",
            "prevent": "Conduct rigorous third-party risk assessments, monitor vendor software behavior via EDR, and segment external integrations."
        }
    }

    selected_attack = st.selectbox("Select Attack Vector", list(attack_data.keys()))

    if selected_attack:
        data = attack_data[selected_attack]
        with st.container(border=True):
            st.markdown(f"### {selected_attack}")
            st.markdown(f"**Definition:** {data['definition']}")
            st.markdown("---")
            st.markdown(f"**Attack Flow:**  \n`{data['flow']}`")
            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Business Impact:**  \n{data['impact']}")
            with col_b:
                st.markdown(f"**How to Prevent:**  \n{data['prevent']}")

# ----------------- SECTION 2: SECURITY CONTROLS EXPLORER -----------------
with tab_controls:
    st.subheader("Security Controls Explorer")
    st.write("Learn the strengths and limitations of primary enterprise security mechanisms.")

    controls_data = {
        "MFA": {
            "purpose": "Requires multiple independent forms of evidence (factors) to authenticate a user's identity.",
            "advantages": "Blocks 99% of automated credential stuffing and mitigates the risk of stolen passwords.",
            "limitations": "Can be bypassed via MFA fatigue attacks or Adversary-in-the-Middle (AiTM) phishing.",
            "best_practice": "Use hardware security keys or FIDO2-compliant authenticators instead of SMS codes."
        },
        "Firewall": {
            "purpose": "Monitors and filters incoming and outgoing network traffic based on predefined security rules.",
            "advantages": "Acts as the first line of defense; segments untrusted external networks from internal assets.",
            "limitations": "Cannot detect threats that bypass the perimeter (e.g., malicious USBs, insider threats).",
            "best_practice": "Deploy Next-Generation Firewalls (NGFW) with deep packet inspection and intrusion prevention."
        },
        "EDR": {
            "purpose": "Continuously monitors endpoints to detect and respond to advanced cyber threats.",
            "advantages": "Identifies malicious behavior rather than just known virus signatures; enables rapid incident response.",
            "limitations": "Requires skilled analysts to tune rules and respond to alerts; can be resource-intensive.",
            "best_practice": "Integrate EDR telemetry into a centralized SIEM for organization-wide visibility."
        },
        "Immutable Backups": {
            "purpose": "Stores copies of data in a format that cannot be altered, encrypted, or deleted by anyone.",
            "advantages": "Provides a guaranteed recovery path during a ransomware attack without paying the ransom.",
            "limitations": "Does not prevent data from being stolen and published (double extortion).",
            "best_practice": "Follow the 3-2-1 backup rule and ensure backups are physically and logically air-gapped."
        },
        "Employee Training": {
            "purpose": "Educates staff on security policies, phishing identification, and safe digital practices.",
            "advantages": "Turns the workforce into a 'human firewall,' significantly reducing the success rate of social engineering.",
            "limitations": "Humans are fallible; a single mistake by one employee can still lead to a breach.",
            "best_practice": "Conduct brief, continuous micro-learning modules combined with monthly simulated phishing campaigns."
        },
        "Automated Patching": {
            "purpose": "Automatically distributes and applies software updates to close known security vulnerabilities.",
            "advantages": "Drastically reduces the attack surface and prevents exploitation of known flaws (N-days).",
            "limitations": "Automated updates can sometimes conflict with legacy systems or cause operational downtime.",
            "best_practice": "Implement a tiered rollout strategy: test in staging, deploy to a pilot group, then push organization-wide."
        }
    }

    selected_control = st.selectbox("Select Security Control", list(controls_data.keys()))

    if selected_control:
        data = controls_data[selected_control]
        with st.container(border=True):
            st.markdown(f"### {selected_control}")
            st.markdown(f"**Purpose:** {data['purpose']}")
            st.markdown("---")
            st.markdown(f"**✅ Advantages:** {data['advantages']}")
            st.markdown(f"**⚠️ Limitations:** {data['limitations']}")
            st.markdown("---")
            st.markdown(f"**🏆 Best Practice:** {data['best_practice']}")

# ----------------- SECTION 3: CYBER KNOWLEDGE QUIZ -----------------
with tab_quiz:
    st.subheader("Cyber Knowledge Quiz")

    # Quiz Data
    raw_questions = [
        {
            "q": "Which attack vector is responsible for the vast majority of initial enterprise breaches?",
            "options": ["Zero-day exploits", "Phishing", "Insider Threats", "DDoS"],
            "answer": "Phishing",
            "explanation": "Over 90% of cyber attacks begin with a phishing email, exploiting human psychology rather than software flaws."
        },
        {
            "q": "What is the primary goal of a DDoS attack?",
            "options": ["Steal customer data", "Encrypt files for ransom", "Exhaust resources to cause downtime",
                        "Escalate user privileges"],
            "answer": "Exhaust resources to cause downtime",
            "explanation": "Distributed Denial of Service (DDoS) attacks flood a system with traffic to make it unavailable to legitimate users."
        },
        {
            "q": "What does EDR stand for in cybersecurity?",
            "options": ["Encrypted Data Recovery", "Endpoint Detection and Response", "Enterprise Defense Routing",
                        "External Domain Resolution"],
            "answer": "Endpoint Detection and Response",
            "explanation": "EDR tools monitor endpoints (laptops, servers) for suspicious behavior and facilitate incident response."
        },
        {
            "q": "What is the primary benefit of an Immutable Backup?",
            "options": ["It compresses data to save space", "It syncs to the cloud instantly",
                        "It cannot be altered or deleted by ransomware", "It prevents data from being stolen"],
            "answer": "It cannot be altered or deleted by ransomware",
            "explanation": "Immutable backups are 'write-once, read-many', ensuring that even if ransomware encrypts the network, the backups remain safe."
        },
        {
            "q": "In a Supply Chain Attack, the threat actor targets:",
            "options": ["A company's third-party software vendor", "The company's HR department",
                        "The physical supply chain of goods", "The company's firewall directly"],
            "answer": "A company's third-party software vendor",
            "explanation": "Attackers compromise a less secure vendor and use their trusted connection/software updates to infiltrate the main target."
        },
        {
            "q": "Which control best mitigates the risk of an attacker using a stolen password?",
            "options": ["Antivirus", "Multi-Factor Authentication (MFA)", "Data Encryption", "Firewalls"],
            "answer": "Multi-Factor Authentication (MFA)",
            "explanation": "MFA requires a second form of verification, making a stolen password useless on its own."
        },
        {
            "q": "What is a Zero-Day vulnerability?",
            "options": ["A flaw that has been patched for zero days", "An attack that takes zero days to execute",
                        "A software flaw unknown to the vendor with no patch available",
                        "A virus that deletes data in zero seconds"],
            "answer": "A software flaw unknown to the vendor with no patch available",
            "explanation": "A Zero-Day is a vulnerability that the software creator is unaware of, meaning there are 'zero days' of protection."
        },
        {
            "q": "What is the core principle of a Zero Trust Architecture?",
            "options": ["Never trust, always verify", "Trust internal traffic, verify external traffic",
                        "Verify once, trust permanently", "Trust users with admin privileges"],
            "answer": "Never trust, always verify",
            "explanation": "Zero Trust assumes threats exist both inside and outside the network, requiring strict identity verification for every access request."
        },
        {
            "q": "Ransomware attacks almost always culminate in:",
            "options": ["A DDoS attack", "An extortion demand", "A phishing email", "A hardware failure"],
            "answer": "An extortion demand",
            "explanation": "Ransomware operators encrypt data (and often steal it) to extort a financial payment in exchange for the decryption key."
        },
        {
            "q": "Which of the following is an example of an Insider Threat?",
            "options": ["A nation-state hacking group", "A misconfigured cloud bucket",
                        "An employee copying proprietary data to a personal USB drive",
                        "A botnet scanning for open ports"],
            "answer": "An employee copying proprietary data to a personal USB drive",
            "explanation": "Insider threats come from individuals within the organization who misuse their authorized access."
        }
    ]

    # Initialize Quiz Session State
    if "quiz_initialized" not in st.session_state:
        # Shuffle questions once per session
        random.shuffle(raw_questions)
        st.session_state.quiz_questions = raw_questions
        st.session_state.quiz_step = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected = None
        st.session_state.quiz_initialized = True

    # Quiz Logic
    step = st.session_state.quiz_step

    if step < 10:
        st.write(f"**Question {step + 1} of 10**")
        st.progress((step) / 10)

        current_q = st.session_state.quiz_questions[step]

        with st.container(border=True):
            st.markdown(f"#### {current_q['q']}")

            # Form to handle selection
            if not st.session_state.quiz_answered:
                selected_option = st.radio("Select an answer:", current_q['options'], key=f"radio_{step}", index=None)
                if st.button("Submit Answer", type="primary"):
                    if selected_option:
                        st.session_state.quiz_selected = selected_option
                        st.session_state.quiz_answered = True
                        if selected_option == current_q['answer']:
                            st.session_state.quiz_score += 1
                        st.rerun()
                    else:
                        st.warning("Please select an answer.")

            # Display Result and Explanation
            else:
                # Keep the radio button visible but disabled to show what they selected
                st.radio("Your selection:", current_q['options'], key=f"radio_disabled_{step}",
                         index=current_q['options'].index(st.session_state.quiz_selected), disabled=True)

                if st.session_state.quiz_selected == current_q['answer']:
                    st.success("✅ **Correct!**")
                else:
                    st.error(f"❌ **Incorrect.** The correct answer is: **{current_q['answer']}**")

                st.info(f"**Explanation:** {current_q['explanation']}")

                if st.button("Next Question"):
                    st.session_state.quiz_step += 1
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None
                    st.rerun()
    else:
        # Quiz Complete
        st.progress(1.0)
        st.success("🎉 **Quiz Complete!**")

        score = st.session_state.quiz_score

        with st.container(border=True):
            st.markdown(f"### Your Final Score: {score} / 10")

            if score == 10:
                st.markdown("🏆 **Outstanding!** You have an expert understanding of cybersecurity fundamentals.")
            elif score >= 7:
                st.markdown("👍 **Great job!** You have a solid grasp of cyber risk and defenses.")
            else:
                st.markdown("📚 **Good effort!** Review the Attack and Control Explorers to sharpen your knowledge.")

            if st.button("Restart Quiz", type="primary"):
                del st.session_state.quiz_initialized
                st.rerun()