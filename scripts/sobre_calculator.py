import yaml
from typing import Dict, Tuple, List
from pathlib import Path

# Charger la configuration depuis le fichier YAML
def load_config() -> Dict:
    config_path = Path(__file__).parent.parent / "config" / "models.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

CONFIG = load_config()
MODELS = CONFIG["models"]
CO2_TO_CAR_KM_FACTOR = CONFIG["co2_to_car_km_factor"]
BADGES_CONFIG = CONFIG["badges"]


def calculate_cost_and_co2(model: str, tokens: int, cost_per_token: float = None, co2_per_token: float = None) -> Dict:
    """
    Calcule le coût et l'empreinte carbone pour un modèle et un nombre de tokens.
    
    Args:
        model: Nom du modèle (ex: "Mistral-7B").
        tokens: Nombre de tokens.
        cost_per_token: Coût par token (€). Si None, utilise la config.
        co2_per_token: CO2 par token (g). Si None, utilise la config.
        
    Returns:
        Dict avec : model, cost (€), co2 (g), co2_car_km (km équivalent voiture)
    """
    if model not in MODELS:
        model = "Mistral-7B"
    
    model_data = MODELS[model]
    if cost_per_token is None:
        cost_per_token = model_data["cost_per_token"]
    if co2_per_token is None:
        co2_per_token = model_data["co2_per_token"]
    
    cost = tokens * cost_per_token
    co2 = tokens * co2_per_token
    co2_car_km = co2 / CO2_TO_CAR_KM_FACTOR
    
    return {
        "model": model,
        "cost": cost,
        "co2": co2,
        "co2_car_km": co2_car_km,
    }


def get_matuity_badge(cost: float, co2: float) -> Tuple[str, int]:
    """
    Retourne un badge de maturité et un score basé sur le coût et le CO2.
    
    Args:
        cost: Coût en €
        co2: Empreinte carbone en g
        
    Returns:
        Tuple: (nom_badge, score)
    """
    for badge_name, badge_config in BADGES_CONFIG.items():
        if cost <= badge_config["max_cost"] and co2 <= badge_config["max_co2"]:
            return badge_config["name"], badge_config["score"]
    
    # Si aucun badge ne correspond, retourner le plus bas (rouge)
    return BADGES_CONFIG["red"]["name"], BADGES_CONFIG["red"]["score"]


def get_recommendations(model: str, tokens: int, cost: float) -> List[str]:
    """
    Génère des recommandations personnalisées pour optimiser le coût et le CO2.
    
    Args:
        model: Modèle utilisé
        tokens: Nombre de tokens
        cost: Coût calculé en €
        
    Returns:
        Liste de recommandations
    """
    recommendations = []
    
    # Recommandation pour changer de modèle si trop cher
    if model == "GPT-4" and cost > 10:
        recommendations.append("💡 Passez à Mistral-7B : -90% de coûts et -80% de CO₂.")
    elif model == "GPT-3.5-turbo" and cost > 5:
        recommendations.append("💡 Passez à Llama-3 : -50% de coûts pour des performances similaires.")
    
    # Recommandations sur la taille des prompts
    if tokens > 10000:
        recommendations.append(f"⚠️ Vos prompts sont très longs ({tokens:,} tokens). Essayez de les réduire.")
    elif tokens > 5000:
        recommendations.append(f"📝 Vos prompts sont longs ({tokens:,} tokens). Optimisez-les pour réduire les coûts.")
    elif tokens > 1000:
        recommendations.append(f"🔍 Vos prompts font {tokens:,} tokens. Pensez à utiliser le batching.")
    
    # Recommandations générales
    if tokens > 500:
        recommendations.append("🚀 Utilisez le batching pour vos requêtes répétitives.")
    
    recommendations.append("💾 Activez le cache pour les requêtes identiques.")
    
    # Recommandation spécifique pour les modèles open-source
    if MODELS[model]["category"] == "open-source":
        recommendations.append("✅ Bon choix ! Les modèles open-source sont souvent plus économes et écologiques.")
    
    return recommendations


def get_all_models() -> List[str]:
    """Retourne la liste de tous les modèles disponibles."""
    return list(MODELS.keys())


def compare_models(tokens: int) -> List[Dict]:
    """
    Compare tous les modèles pour un nombre de tokens donné.
    
    Args:
        tokens: Nombre de tokens à comparer
        
    Returns:
        Liste de dictionnaires avec les résultats pour chaque modèle
    """
    results = []
    for model_name in MODELS:
        result = calculate_cost_and_co2(model_name, tokens)
        badge, score = get_matuity_badge(result["cost"], result["co2"])
        results.append({
            "model": model_name,
            "cost": result["cost"],
            "co2": result["co2"],
            "co2_car_km": result["co2_car_km"],
            "badge": badge,
            "score": score,
            "provider": MODELS[model_name]["provider"],
            "category": MODELS[model_name]["category"]
        })
    
    # Trier par coût croissant
    results.sort(key=lambda x: x["cost"])
    return results
