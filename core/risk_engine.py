"""
risk_engine.py
Core logic module for SecureSphere AI.
Responsible for calculating cyber risk scores, evaluating readiness levels,
and estimating financial loss based on configurable multipliers.
"""

import config
from typing import Dict, Tuple


class RiskEngine:
    """
    Expert system for evaluating cyber risk based on enterprise firmographics
    and implemented security controls.
    """

    def calculate_risk_score(self, controls: Dict[str, bool]) -> int:
        """
        Calculates the enterprise risk score using a base-subtraction model.
        Starts at the maximum default risk and subtracts points for active controls.

        Args:
            controls (Dict[str, bool]): A dictionary where keys are control names
                                        and values are boolean indicating if active.

        Returns:
            int: The clamped risk score between MIN and MAX limits.
        """
        score = config.RISK_SCORE["DEFAULT"]

        # Subtract weights for active security controls
        for control_name, is_active in controls.items():
            if is_active and control_name in config.CONTROL_WEIGHTS:
                score -= config.CONTROL_WEIGHTS[control_name]

        # Enforce MIN and MAX constraints
        score = max(config.RISK_SCORE["MIN"], score)
        score = min(config.RISK_SCORE["MAX"], score)

        return score

    def get_readiness_level(self, risk_score: int) -> Dict[str, str]:
        """
        Maps a calculated risk score to a 5-star cyber readiness tier.

        Args:
            risk_score (int): The calculated risk score (0-100).

        Returns:
            Dict[str, str]: Dictionary containing 'stars' (int), 'label' (str),
                            and 'stars_display' (str).
        """
        # Sort tiers to safely evaluate thresholds from lowest score to highest
        sorted_tiers = sorted(config.READINESS_TIERS, key=lambda x: x["max_score"])

        for tier in sorted_tiers:
            if risk_score <= tier["max_score"]:
                return {
                    "stars": tier["stars"],
                    "label": tier["label"],
                    "stars_display": tier["stars_display"]
                }

        # Fallback to the worst-case tier (should not be reached if clamped properly)
        worst_tier = sorted_tiers[-1]
        return {
            "stars": worst_tier["stars"],
            "label": worst_tier["label"],
            "stars_display": worst_tier["stars_display"]
        }

    def estimate_financial_loss(
            self,
            annual_revenue: float,
            industry: str,
            attack_type: str,
            critical_asset: str
    ) -> Tuple[float, float]:
        """
        Estimates the minimum and maximum financial loss of an attack.
        Applies configured multipliers to a baseline revenue percentage.

        Args:
            annual_revenue (float): The company's total annual revenue.
            industry (str): The company's industry sector.
            attack_type (str): The specific cyber attack vector.
            critical_asset (str): The primary asset targeted by the attack.

        Returns:
            Tuple[float, float]: (minimum_loss, maximum_loss) in dollars.
        """
        # Fetch multipliers, defaulting to 1.0 if not found
        ind_mult = config.INDUSTRY_MULTIPLIERS.get(industry, 1.0)
        att_mult = config.ATTACK_TYPE_MULTIPLIERS.get(attack_type, 1.0)
        ass_mult = config.CRITICAL_ASSET_MULTIPLIERS.get(critical_asset, 1.0)

        # Calculate a base impact value (e.g., representing 0.5% of revenue at baseline risk)
        base_impact = annual_revenue * 0.005

        # Apply multidimensional multipliers
        calculated_impact = base_impact * ind_mult * att_mult * ass_mult

        # Create a realistic variance range for min/max
        minimum_loss = calculated_impact * 0.7
        maximum_loss = calculated_impact * 1.4

        return minimum_loss, maximum_loss