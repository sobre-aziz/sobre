def calculate_cost_and_co2(model, tokens, cost_per_token=None, co2_per_token=None):
    MODEL_DEFAULT = {
        "Mistral-7B": {"cost": 0.000002, "co2": 0.0005},
        "GPT-4": {"cost": 0.00003, "co2": 0.001},
        "Llama-3": {"cost": 0.0000015, "co2": 0.0004},
    }
    if model not in MODEL_DEFAULT:
        model = "Mistral-7B"
    model_data = MODEL_DEFAULT[model]
    if cost_per_token is None:
        cost_per_token = model_data["cost"]
    if co2_per_token is None:
        co2_per_token = model_data["co2"]
    cost = tokens * cost_per_token
    co2 = tokens * co2_per_token
    co2_car_km = co2 / 0.2
    return {
        "model": model,
        "cost": cost,
        "co2": co2,
        "co2_car_km": co2_car_km,
    }

def get_matuity_badge(cost, co2):
    if cost < 100 and co2 < 100:
        return "🥇 Or - Expert", 100
    elif cost < 500 and co2 < 500:
        return "🥈 Argent - Intermédiaire", 75
    elif cost < 1000 and co2 < 1000:
        return "🥉 Bronze - Débutant", 50
    else:
        return "⚠️ Rouge - À améliorer", 25

def get_recommendations(model, tokens, cost):
    recommendations = []
    if model == "GPT-4" and cost > 10:
        recommendations.append("💡 Passez à Mistral-7B : -90% de coûts et -80% de CO₂.")
    if tokens > 500:
        recommendations.append(f"✂️ Réduisez vos prompts (actuellement {tokens} tokens).")
    if tokens > 1000:
        recommendations.append("🔄 Utilisez le batching pour vos requêtes répétitives.")
    recommendations.append("💾 Activez le cache pour les requêtes identiques.")
    return recommendations

