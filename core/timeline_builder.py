"""
timeline_builder.py
Generates chronological cyber attack narratives for SecureSphere AI.
Constructs step-by-step timelines based on the chosen attack vector.
"""

from typing import List, Dict


class TimelineBuilder:
    """
    Constructs narrative timelines for various cyber attack scenarios.
    Outputs a list of chronological events demonstrating how a specific
    threat actor might compromise an enterprise over a 7-day period.
    """

    def build_timeline(self, attack_type: str) -> List[Dict[str, str]]:
        """
        Generates a 4-step placeholder timeline for the specified attack type.

        Args:
            attack_type (str): The specific cyber attack vector
                               (e.g., 'Phishing', 'Ransomware').

        Returns:
            List[Dict[str, str]]: A list of timeline events, where each event
                                  is a dictionary with 'day', 'title', and 'description'.
        """
        # Normalize the attack type string for safer matching
        normalized_attack = attack_type.strip().lower()

        # Dictionary of predefined attack narratives
        timelines = {
            "phishing": [
                {
                    "day": "Day 1",
                    "title": "Initial Email Delivery",
                    "description": "An employee receives a highly targeted spear-phishing email impersonating the IT department."
                },
                {
                    "day": "Day 3",
                    "title": "Credential Theft",
                    "description": "The employee clicks the malicious link and enters their credentials into a fake login portal."
                },
                {
                    "day": "Day 5",
                    "title": "Account Takeover",
                    "description": "The attacker successfully logs into the corporate network using the stolen credentials."
                },
                {
                    "day": "Day 7",
                    "title": "Data Exfiltration",
                    "description": "Sensitive internal communications and customer records are forwarded to an external server."
                }
            ],

            "ransomware": [
                {
                    "day": "Day 1",
                    "title": "Initial Compromise",
                    "description": "An attacker exploits an unpatched vulnerability in an outward-facing VPN gateway."
                },
                {
                    "day": "Day 3",
                    "title": "Lateral Movement",
                    "description": "The malware spreads silently across the internal network, mapping servers and endpoints."
                },
                {
                    "day": "Day 5",
                    "title": "Payload Deployment",
                    "description": "Encryption payloads are simultaneously executed on all infected hosts."
                },
                {
                    "day": "Day 7",
                    "title": "Operations Halted",
                    "description": "Business operations completely freeze, and a ransom demand is displayed on all screens."
                }
            ],

            "insider threat": [
                {
                    "day": "Day 1",
                    "title": "Privilege Escalation",
                    "description": "A disgruntled employee requests and is improperly granted access to restricted financial databases."
                },
                {
                    "day": "Day 3",
                    "title": "Data Harvesting",
                    "description": "The employee begins quietly downloading large volumes of sensitive company data to a personal drive."
                },
                {
                    "day": "Day 5",
                    "title": "Covering Tracks",
                    "description": "The employee attempts to delete network audit logs to hide their unauthorized downloads."
                },
                {
                    "day": "Day 7",
                    "title": "Data Leak",
                    "description": "The stolen proprietary information is leaked or sold to a direct competitor."
                }
            ],

            "data breach": [
                {
                    "day": "Day 1",
                    "title": "Vulnerability Scanning",
                    "description": "Attackers identify a misconfigured, public-facing cloud storage bucket."
                },
                {
                    "day": "Day 3",
                    "title": "Database Access",
                    "description": "An automated script gains read-access to the exposed customer database."
                },
                {
                    "day": "Day 5",
                    "title": "Data Extraction",
                    "description": "Millions of customer records, including PII, are quietly extracted over an encrypted channel."
                },
                {
                    "day": "Day 7",
                    "title": "Dark Web Sale",
                    "description": "The breached data is published for sale on an underground hacker forum."
                }
            ],

            "ddos": [
                {
                    "day": "Day 1",
                    "title": "Botnet Mobilization",
                    "description": "A threat actor commands a global botnet to target the company's primary web servers."
                },
                {
                    "day": "Day 3",
                    "title": "Traffic Spike",
                    "description": "A massive influx of junk traffic begins to overwhelm the company's network bandwidth."
                },
                {
                    "day": "Day 5",
                    "title": "Service Outage",
                    "description": "Customer-facing portals, applications, and APIs become completely unresponsive."
                },
                {
                    "day": "Day 7",
                    "title": "Mitigation and Recovery",
                    "description": "Cloud scrubbing centers and ISPs successfully filter the malicious traffic, restoring service."
                }
            ],

            "supply chain attack": [
                {
                    "day": "Day 1",
                    "title": "Vendor Compromise",
                    "description": "A trusted third-party software vendor's infrastructure is breached by a state-sponsored group."
                },
                {
                    "day": "Day 3",
                    "title": "Malicious Update",
                    "description": "The company downloads and installs a seemingly legitimate software update containing a hidden backdoor."
                },
                {
                    "day": "Day 5",
                    "title": "Backdoor Activation",
                    "description": "The hidden malware establishes a reverse shell, giving attackers a foothold inside the network."
                },
                {
                    "day": "Day 7",
                    "title": "Corporate Espionage",
                    "description": "Attackers silently exfiltrate highly classified source code and intellectual property."
                }
            ]
        }

        # Fallback generic timeline for unknown attack types
        generic_timeline = [
            {
                "day": "Day 1",
                "title": "Initial Vector",
                "description": "A security vulnerability is exploited to gain unauthorized access."
            },
            {
                "day": "Day 3",
                "title": "Network Penetration",
                "description": "Attackers establish a persistent foothold and escalate privileges."
            },
            {
                "day": "Day 5",
                "title": "Objective Execution",
                "description": "Malicious activities, such as data theft or system disruption, are carried out."
            },
            {
                "day": "Day 7",
                "title": "Impact Realized",
                "description": "The breach is discovered as critical business operations are impacted."
            }
        ]

        # Return the specific timeline if found, otherwise return the generic one
        return timelines.get(normalized_attack, generic_timeline)