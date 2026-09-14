# Package utils pour Sobre
# Contient les modules de calcul, tracking et génération de rapports

from .carbon_calculator import (calculate_api_carbon, calculate_saas_carbon,
                                get_model_carbon_per_token,
                                get_saas_monthly_carbon)
from .cost_calculator import (calculate_api_cost, calculate_saas_cost,
                              get_model_cost_per_token, get_saas_monthly_cost)
from .greenops_scoring import calculate_greenops_score, get_greenops_grade
from .report_generator import generate_csrd_report, generate_summary_report
from .subscription_tracker import (detect_ai_subscriptions,
                                   identify_dormant_licenses,
                                   process_uploaded_file)

__all__ = [
    # Cost Calculator
    "calculate_api_cost",
    "calculate_saas_cost",
    "get_model_cost_per_token",
    "get_saas_monthly_cost",
    # Carbon Calculator
    "calculate_api_carbon",
    "calculate_saas_carbon",
    "get_model_carbon_per_token",
    "get_saas_monthly_carbon",
    # Subscription Tracker
    "detect_ai_subscriptions",
    "identify_dormant_licenses",
    "process_uploaded_file",
    # Report Generator
    "generate_csrd_report",
    "generate_summary_report",
    # GreenOps Scoring
    "calculate_greenops_score",
    "get_greenops_grade",
]
