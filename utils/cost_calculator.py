"""
Cost Calculator Module for Sobre

Ce module contient les fonctions pour calculer les coûts liés à l'utilisation
des modèles IA (APIs) et des abonnements SaaS.

Sources:
    - OpenAI Pricing: https://openai.com/pricing
    - Mistral AI Pricing: https://mistral.ai/pricing/
    - Meta Llama Pricing: https://aws.amazon.com/bedrock/llama/
"""

import yaml
from pathlib import Path
from typing import Dict, Union, Optional


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


def get_model_cost_per_token(model_name: str, token_type: str = "input") -> Optional[float]:
    """
    Récupère le coût par token pour un modèle donné.
    
    Args:
        model_name: Nom du modèle (ex: "GPT-4").
        token_type: Type de token ("input" ou "output").
        
    Returns:
        float: Coût par token en €, ou None si le modèle n'est pas trouvé.
        
    Raises:
        ValueError: Si token_type n'est pas "input" ou "output".
    """
    if token_type not in ["input", "output"]:
        raise ValueError("token_type doit être 'input' ou 'output'")
    
    if model_name not in MODELS:
        return None
    
    model_data = MODELS[model_name]
    cost_key = f"cost_per_token_{token_type}"
    
    if cost_key in model_data:
        return model_data[cost_key]
    
    # Si pas de distinction input/output, retourner la valeur par défaut
    if "cost_per_token" in model_data:
        return model_data["cost_per_token"]
    
    return None


def calculate_api_cost(
    model_name: str,
    input_tokens: int,
    output_tokens: int = 0,
    custom_input_cost: Optional[float] = None,
    custom_output_cost: Optional[float] = None
) -> Dict:
    """
    Calcule le coût pour l'utilisation d'une API IA.
    
    Args:
        model_name: Nom du modèle (ex: "GPT-4").
        input_tokens: Nombre de tokens en entrée.
        output_tokens: Nombre de tokens en sortie (par défaut: 0).
        custom_input_cost: Coût personnalisé par token d'entrée (€).
        custom_output_cost: Coût personnalisé par token de sortie (€).
        
    Returns:
        Dict: {
            "model": str,
            "input_tokens": int,
            "output_tokens": int,
            "total_tokens": int,
            "input_cost": float,
            "output_cost": float,
            "total_cost": float (arrondi à 2 décimales)
        }
        
    Raises:
        ValueError: Si input_tokens ou output_tokens sont négatifs.
    """
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("input_tokens et output_tokens doivent être positifs ou nuls")
    
    if model_name not in MODELS:
        model_name = "GPT-4"  # Modèle par défaut
    
    # Récupérer les coûts
    input_cost = custom_input_cost if custom_input_cost is not None else get_model_cost_per_token(model_name, "input")
    output_cost = custom_output_cost if custom_output_cost is not None else get_model_cost_per_token(model_name, "output")
    
    if input_cost is None:
        input_cost = 0.00003  # Valeur par défaut (GPT-4 input)
    if output_cost is None:
        output_cost = 0.00006  # Valeur par défaut (GPT-4 output)
    
    # Calculer les coûts
    calculated_input_cost = input_tokens * input_cost
    calculated_output_cost = output_tokens * output_cost
    total_cost = calculated_input_cost + calculated_output_cost
    
    return {
        "model": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": round(calculated_input_cost, 6),
        "output_cost": round(calculated_output_cost, 6),
        "total_cost": round(total_cost, 2)
    }


def get_saas_monthly_cost(saas_name: str) -> Optional[float]:
    """
    Récupère le coût mensuel d'un abonnement SaaS.
    
    Args:
        saas_name: Nom du SaaS (ex: "ChatGPT-Plus").
        
    Returns:
        float: Coût mensuel en €, ou None si non trouvé.
    """
    if saas_name not in SAAS_SUBSCRIPTIONS:
        return None
    
    return SAAS_SUBSCRIPTIONS[saas_name]["monthly_cost"]


def calculate_saas_cost(
    saas_name: str,
    quantity: int = 1,
    duration_months: int = 1
) -> Dict:
    """
    Calcule le coût total pour un abonnement SaaS.
    
    Args:
        saas_name: Nom du SaaS (ex: "ChatGPT-Plus").
        quantity: Nombre d'utilisateurs/licences.
        duration_months: Durée en mois.
        
    Returns:
        Dict: {
            "saas_name": str,
            "monthly_cost": float,
            "quantity": int,
            "duration_months": int,
            "total_cost": float (arrondi à 2 décimales)
        }
        
    Raises:
        ValueError: Si quantity ou duration_months sont négatifs.
    """
    if quantity < 0 or duration_months < 0:
        raise ValueError("quantity et duration_months doivent être positifs ou nuls")
    
    monthly_cost = get_saas_monthly_cost(saas_name)
    if monthly_cost is None:
        monthly_cost = 0  # Si SaaS non trouvé, coût = 0
    
    total_cost = monthly_cost * quantity * duration_months
    
    return {
        "saas_name": saas_name,
        "monthly_cost": monthly_cost,
        "quantity": quantity,
        "duration_months": duration_months,
        "total_cost": round(total_cost, 2)
    }


def calculate_total_cost(
    api_usage: Optional[Dict] = None,
    saas_subscriptions: Optional[list] = None
) -> Dict:
    """
    Calcule le coût total combiné (APIs + SaaS).
    
    Args:
        api_usage: Résultat de calculate_api_cost ou None.
        saas_subscriptions: Liste de résultats de calculate_saas_cost ou None.
        
    Returns:
        Dict: {
            "api_cost": float,
            "saas_cost": float,
            "total_cost": float (arrondi à 2 décimales)
        }
    """
    api_cost = api_usage["total_cost"] if api_usage else 0
    saas_cost = sum(sub["total_cost"] for sub in saas_subscriptions) if saas_subscriptions else 0
    
    return {
        "api_cost": api_cost,
        "saas_cost": round(saas_cost, 2),
        "total_cost": round(api_cost + saas_cost, 2)
    }
