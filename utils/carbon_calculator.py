"""
Carbon Calculator Module for Sobre

Ce module contient les fonctions pour calculer l'empreinte carbone liée à
l'utilisation des modèles IA (APIs) et des abonnements SaaS.

Sources:
    - "Carbon Footprint of AI Models" (arXiv:2111.02186)
    - Microsoft Sustainability Report 2023
    - ADEME - Impact environnemental du numérique
"""

import yaml
from pathlib import Path
from typing import Dict, Optional, Union


def load_config() -> Dict:
    """
    Charge la configuration depuis le fichier YAML.
    
    Returns:
        Dict: Configuration complète des modèles et SaaS.
    """
    config_path = Path(__file__).parent.parent / "config" / "models.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


CONFIG = load_config()
MODELS = CONFIG["models"]
SAAS_SUBSCRIPTIONS = CONFIG["saas_subscriptions"]
CO2_TO_CAR_KM_FACTOR = CONFIG["co2_to_car_km_factor"]


def get_model_carbon_per_token(model_name: str) -> Optional[float]:
    """
    Récupère l'empreinte carbone par million de tokens pour un modèle donné.
    
    Args:
        model_name: Nom du modèle (ex: "GPT-4").
        
    Returns:
        float: kg CO2 par million de tokens, ou None si le modèle n'est pas trouvé.
    """
    if model_name not in MODELS:
        return None
    
    model_data = MODELS[model_name]
    if "co2_per_million_tokens" in model_data:
        return model_data["co2_per_million_tokens"]
    
    return None


def calculate_api_carbon(
    model_name: str,
    total_tokens: int,
    custom_carbon_per_million: Optional[float] = None
) -> Dict:
    """
    Calcule l'empreinte carbone pour l'utilisation d'une API IA.
    
    Args:
        model_name: Nom du modèle (ex: "GPT-4").
        total_tokens: Nombre total de tokens (input + output).
        custom_carbon_per_million: Empreinte carbone personnalisée par million de tokens (kg).
        
    Returns:
        Dict: {
            "model": str,
            "total_tokens": int,
            "carbon_kg": float,
            "carbon_g": float (arrondi à 1 décimale),
            "co2_car_km": float (km équivalent voiture, arrondi à 1 décimale)
        }
        
    Raises:
        ValueError: Si total_tokens est négatif.
    """
    if total_tokens < 0:
        raise ValueError("total_tokens doit être positif ou nul")
    
    if model_name not in MODELS:
        model_name = "GPT-4"  # Modèle par défaut
    
    # Récupérer l'empreinte carbone
    carbon_per_million = custom_carbon_per_million if custom_carbon_per_million is not None else get_model_carbon_per_token(model_name)
    
    if carbon_per_million is None:
        carbon_per_million = 0.3  # Valeur par défaut (GPT-4)
    
    # Calculer l'empreinte carbone en kg
    carbon_kg = (total_tokens / 1_000_000) * carbon_per_million
    carbon_g = carbon_kg * 1000
    
    # Convertir en km voiture
    co2_car_km = carbon_g / CO2_TO_CAR_KM_FACTOR
    
    return {
        "model": model_name,
        "total_tokens": total_tokens,
        "carbon_kg": round(carbon_kg, 4),
        "carbon_g": round(carbon_g, 1),
        "co2_car_km": round(co2_car_km, 1)
    }


def get_saas_monthly_carbon(saas_name: str) -> Optional[float]:
    """
    Récupère l'empreinte carbone mensuelle d'un abonnement SaaS.
    
    Args:
        saas_name: Nom du SaaS (ex: "ChatGPT-Plus").
        
    Returns:
        float: kg CO2 par mois, ou None si non trouvé.
    """
    if saas_name not in SAAS_SUBSCRIPTIONS:
        return None
    
    return SAAS_SUBSCRIPTIONS[saas_name]["co2_per_month"]


def calculate_saas_carbon(
    saas_name: str,
    quantity: int = 1,
    duration_months: int = 1
) -> Dict:
    """
    Calcule l'empreinte carbone totale pour un abonnement SaaS.
    
    Args:
        saas_name: Nom du SaaS (ex: "ChatGPT-Plus").
        quantity: Nombre d'utilisateurs/licences.
        duration_months: Durée en mois.
        
    Returns:
        Dict: {
            "saas_name": str,
            "monthly_carbon_kg": float,
            "quantity": int,
            "duration_months": int,
            "total_carbon_kg": float,
            "total_carbon_g": float (arrondi à 1 décimale),
            "co2_car_km": float (km équivalent voiture, arrondi à 1 décimale)
        }
        
    Raises:
        ValueError: Si quantity ou duration_months sont négatifs.
    """
    if quantity < 0 or duration_months < 0:
        raise ValueError("quantity et duration_months doivent être positifs ou nuls")
    
    monthly_carbon_kg = get_saas_monthly_carbon(saas_name)
    if monthly_carbon_kg is None:
        monthly_carbon_kg = 0  # Si SaaS non trouvé, CO2 = 0
    
    total_carbon_kg = monthly_carbon_kg * quantity * duration_months
    total_carbon_g = total_carbon_kg * 1000
    co2_car_km = total_carbon_g / CO2_TO_CAR_KM_FACTOR
    
    return {
        "saas_name": saas_name,
        "monthly_carbon_kg": monthly_carbon_kg,
        "quantity": quantity,
        "duration_months": duration_months,
        "total_carbon_kg": round(total_carbon_kg, 4),
        "total_carbon_g": round(total_carbon_g, 1),
        "co2_car_km": round(co2_car_km, 1)
    }


def calculate_total_carbon(
    api_usage: Optional[Dict] = None,
    saas_subscriptions: Optional[list] = None
) -> Dict:
    """
    Calcule l'empreinte carbone totale combinée (APIs + SaaS).
    
    Args:
        api_usage: Résultat de calculate_api_carbon ou None.
        saas_subscriptions: Liste de résultats de calculate_saas_carbon ou None.
        
    Returns:
        Dict: {
            "api_carbon_g": float,
            "saas_carbon_g": float,
            "total_carbon_g": float (arrondi à 1 décimale),
            "total_co2_car_km": float (km équivalent voiture, arrondi à 1 décimale)
        }
    """
    api_carbon_g = api_usage["carbon_g"] if api_usage else 0
    saas_carbon_g = sum(sub["total_carbon_g"] for sub in saas_subscriptions) if saas_subscriptions else 0
    
    total_carbon_g = api_carbon_g + saas_carbon_g
    total_co2_car_km = total_carbon_g / CO2_TO_CAR_KM_FACTOR
    
    return {
        "api_carbon_g": api_carbon_g,
        "saas_carbon_g": round(saas_carbon_g, 1),
        "total_carbon_g": round(total_carbon_g, 1),
        "total_co2_car_km": round(total_co2_car_km, 1)
    }
