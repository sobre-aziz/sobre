"""
GreenOps Scoring Module for Sobre

Ce module contient les fonctions pour calculer le score GreenOps des PME
selon leur usage de l'IA (coûts, CO2, licences dormantes).

Le score GreenOps va de A (Excellent) à E (Critique).
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_config() -> Dict:
    """
    Charge la configuration depuis le fichier YAML.
    
    Returns:
        Dict: Configuration complète.
    """
    config_path = Path(__file__).parent.parent / "config" / "models.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


CONFIG = load_config()
GREENOPS_SCORES = CONFIG["greenops_scores"]


def calculate_greenops_score(
    total_cost: float,
    total_carbon_g: float,
    number_of_employees: int,
    number_of_licenses: int,
    dormant_licenses_count: int = 0
) -> Dict:
    """
    Calcule le score GreenOps pour une PME.
    
    Args:
        total_cost: Coût total mensuel en €.
        total_carbon_g: Empreinte carbone totale en g.
        number_of_employees: Nombre d'employés dans la PME.
        number_of_licenses: Nombre total de licences abonnements.
        dormant_licenses_count: Nombre de licences dormantes.
        
    Returns:
        Dict: {
            "cost_per_employee": float,
            "carbon_per_employee": float,
            "active_licenses_percentage": float,
            "grade": str (A, B, C, D, E),
            "grade_name": str,
            "score": int (0-100)
        }
        
    Raises:
        ValueError: Si number_of_employees est 0.
    """
    if number_of_employees <= 0:
        raise ValueError("number_of_employees doit être supérieur à 0")
    
    # Calculer les métriques par employé
    cost_per_employee = total_cost / number_of_employees
    carbon_per_employee = total_carbon_g / number_of_employees
    
    # Calculer le pourcentage de licences actives
    if number_of_licenses > 0:
        active_licenses_percentage = ((number_of_licenses - dormant_licenses_count) / number_of_licenses) * 100
    else:
        active_licenses_percentage = 100
    
    # Déterminer le grade en fonction des seuils
    grade = "E"
    grade_name = "E - Critique"
    score = 0
    
    for grade_key, grade_config in GREENOPS_SCORES.items():
        if (cost_per_employee <= grade_config["max_cost_per_employee"] and
            carbon_per_employee <= grade_config["max_co2_per_employee"] and
            active_licenses_percentage >= grade_config["min_dormant_licenses"]):
            grade = grade_key
            grade_name = grade_config["name"]
            # Calculer le score (100 pour A, 80 pour B, etc.)
            score_map = {"A": 100, "B": 80, "C": 60, "D": 40, "E": 20}
            score = score_map.get(grade, 20)
            break
    
    return {
        "cost_per_employee": round(cost_per_employee, 2),
        "carbon_per_employee": round(carbon_per_employee, 2),
        "active_licenses_percentage": round(active_licenses_percentage, 1),
        "grade": grade,
        "grade_name": grade_name,
        "score": score
    }


def get_greenops_grade(
    cost_per_employee: float,
    carbon_per_employee: float,
    active_licenses_percentage: float
) -> Tuple[str, str, int]:
    """
    Retourne le grade GreenOps basé sur les métriques.
    
    Args:
        cost_per_employee: Coût par employé en €.
        carbon_per_employee: CO2 par employé en g.
        active_licenses_percentage: Pourcentage de licences actives.
        
    Returns:
        Tuple: (grade, grade_name, score)
    """
    grade = "E"
    grade_name = "E - Critique"
    score = 20
    
    for grade_key, grade_config in GREENOPS_SCORES.items():
        if (cost_per_employee <= grade_config["max_cost_per_employee"] and
            carbon_per_employee <= grade_config["max_co2_per_employee"] and
            active_licenses_percentage >= grade_config["min_dormant_licenses"]):
            grade = grade_key
            grade_name = grade_config["name"]
            score_map = {"A": 100, "B": 80, "C": 60, "D": 40, "E": 20}
            score = score_map.get(grade, 20)
            break
    
    return grade, grade_name, score


def generate_greenops_recommendations(
    greenops_result: Dict,
    total_cost: float,
    total_carbon_g: float,
    dormant_licenses: List[Dict]
) -> List[str]:
    """
    Génère des recommandations personnalisées basé sur le score GreenOps.
    
    Args:
        greenops_result: Résultat de calculate_greenops_score.
        total_cost: Coût total mensuel en €.
        total_carbon_g: Empreinte carbone totale en g.
        dormant_licenses: Liste des licences dormantes.
        
    Returns:
        List[str]: Liste de recommandations.
    """
    recommendations = []
    grade = greenops_result["grade"]
    
    # Recommandations générales selon le grade
    if grade == "E":
        recommendations.append(
            "🚨 **Urgence** : Votre score GreenOps est critique. "
            "Réduisez immédiatement vos coûts et votre empreinte carbone."
        )
        recommendations.append(
            "💡 **Priorité** : Identifiez et désactivez toutes les licences dormantes."
        )
    elif grade == "D":
        recommendations.append(
            "⚠️ **À améliorer** : Votre score GreenOps peut être significativement amélioré."
        )
        recommendations.append(
            "💡 **Conseil** : Passez à des modèles plus économiques (ex: Mistral-7B au lieu de GPT-4)."
        )
    elif grade == "C":
        recommendations.append(
            "✅ **Moyen** : Votre score GreenOps est acceptable, mais peut être optimisé."
        )
        recommendations.append(
            "💡 **Conseil** : Optimisez vos prompts et utilisez le batching."
        )
    elif grade == "B":
        recommendations.append(
            "👍 **Bon** : Votre score GreenOps est bon !"
        )
        recommendations.append(
            "💡 **Conseil** : Continuez à surveiller vos coûts et votre empreinte carbone."
        )
    else:  # A
        recommendations.append(
            "🎉 **Excellent** : Votre score GreenOps est optimal !"
        )
        recommendations.append(
            "💡 **Conseil** : Partagez vos bonnes pratiques avec d'autres entreprises."
        )
    
    # Recommandations spécifiques
    if dormant_licenses:
        recommendations.append(
            f"🗑️ **Licences dormantes** : Vous avez {len(dormant_licenses)} licence(s) inutilisée(s). "
            "Désactivez-les pour économiser jusqu'à 30% de vos coûts."
        )
    
    if total_cost > 1000:
        recommendations.append(
            "💰 **Coûts élevés** : Vos coûts IA sont supérieurs à 1000€/mois. "
            "Envisagez de négocier des tarifs entreprise avec vos fournisseurs."
        )
    
    if total_carbon_g > 10000:
        recommendations.append(
            "🌍 **Empreinte carbone élevée** : Votre empreinte carbone dépasse 10kg CO2/mois. "
            "Passez à des modèles plus écologiques (ex: Mistral-7B, Llama-2-70B)."
        )
    
    if greenops_result["active_licenses_percentage"] < 80:
        recommendations.append(
            f"📉 **Taux d'utilisation faible** : Seulement {greenops_result['active_licenses_percentage']}% "
            "de vos licences sont actives. Optimisez votre portefeuille SaaS."
        )
    
    return recommendations


def calculate_potential_savings(
    total_cost: float,
    total_carbon_g: float,
    dormant_licenses: List[Dict],
    saas_subscriptions: List[Dict]
) -> Dict:
    """
    Calcule les économies potentielles (coût et CO2) si les licences dormantes sont désactivées.
    
    Args:
        total_cost: Coût total mensuel en €.
        total_carbon_g: Empreinte carbone totale en g.
        dormant_licenses: Liste des licences dormantes.
        saas_subscriptions: Liste de tous les abonnements SaaS.
        
    Returns:
        Dict: {
            "cost_savings": float,
            "carbon_savings_g": float,
            "percentage_cost_savings": float,
            "percentage_carbon_savings": float
        }
    """
    # Calculer le coût des licences dormantes
    dormant_cost = 0
    dormant_carbon = 0
    
    for dormant in dormant_licenses:
        # Trouver le SaaS correspondant dans les abonnements
        for sub in saas_subscriptions:
            if sub.get("name") == dormant.get("name"):
                dormant_cost += sub.get("monthly_cost", 0)
                dormant_carbon += sub.get("monthly_carbon_kg", 0) * 1000  # Convertir kg en g
                break
    
    # Calculer les économies
    cost_savings = dormant_cost
    carbon_savings_g = dormant_carbon
    
    if total_cost > 0:
        percentage_cost_savings = (cost_savings / total_cost) * 100
    else:
        percentage_cost_savings = 0
    
    if total_carbon_g > 0:
        percentage_carbon_savings = (carbon_savings_g / total_carbon_g) * 100
    else:
        percentage_carbon_savings = 0
    
    return {
        "cost_savings": round(cost_savings, 2),
        "carbon_savings_g": round(carbon_savings_g, 1),
        "percentage_cost_savings": round(percentage_cost_savings, 1),
        "percentage_carbon_savings": round(percentage_carbon_savings, 1)
    }
