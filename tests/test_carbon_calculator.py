"""
Tests unitaires pour le module carbon_calculator.

Exécutez avec: pytest tests/test_carbon_calculator.py -v
"""

import pytest
from utils.carbon_calculator import (
    calculate_api_carbon,
    calculate_saas_carbon,
    calculate_total_carbon,
    get_model_carbon_per_token,
    get_saas_monthly_carbon,
    MODELS,
    SAAS_SUBSCRIPTIONS
)


class TestGetModelCarbonPerToken:
    """Tests pour get_model_carbon_per_token."""
    
    def test_gpt4_carbon(self):
        """Test de l'empreinte carbone par million de tokens pour GPT-4."""
        carbon = get_model_carbon_per_token("GPT-4")
        assert carbon == 0.3  # 0.3 kg CO2 par 1M tokens
    
    def test_mistral7b_carbon(self):
        """Test de l'empreinte carbone par million de tokens pour Mistral-7B."""
        carbon = get_model_carbon_per_token("Mistral-7B")
        assert carbon == 0.05  # 0.05 kg CO2 par 1M tokens
    
    def test_llama2_70b_carbon(self):
        """Test de l'empreinte carbone par million de tokens pour Llama-2-70B."""
        carbon = get_model_carbon_per_token("Llama-2-70B")
        assert carbon == 0.03  # 0.03 kg CO2 par 1M tokens
    
    def test_unknown_model(self):
        """Test avec un modèle inconnu (doit retourner None)."""
        carbon = get_model_carbon_per_token("Unknown-Model")
        assert carbon is None


class TestCalculateApiCarbon:
    """Tests pour calculate_api_carbon."""
    
    def test_basic_calculation(self):
        """Test de calcul de base pour GPT-4."""
        result = calculate_api_carbon("GPT-4", total_tokens=1_000_000)
        
        # 1M tokens * 0.3 kg CO2 / 1M tokens = 0.3 kg = 300 g
        assert result["model"] == "GPT-4"
        assert result["total_tokens"] == 1_000_000
        assert result["carbon_kg"] == pytest.approx(0.3, rel=1e-4)
        assert result["carbon_g"] == pytest.approx(300.0, rel=1e-1)
        assert result["co2_car_km"] == pytest.approx(1500.0, rel=1e-1)  # 300g / 0.2 = 1500 km
    
    def test_mistral7b_calculation(self):
        """Test de calcul pour Mistral-7B."""
        result = calculate_api_carbon("Mistral-7B", total_tokens=1_000_000)
        
        # 1M tokens * 0.05 kg CO2 / 1M tokens = 0.05 kg = 50 g
        assert result["carbon_kg"] == pytest.approx(0.05, rel=1e-4)
        assert result["carbon_g"] == pytest.approx(50.0, rel=1e-1)
        assert result["co2_car_km"] == pytest.approx(250.0, rel=1e-1)  # 50g / 0.2 = 250 km
    
    def test_custom_carbon(self):
        """Test avec une valeur de CO2 personnalisée."""
        result = calculate_api_carbon(
            "GPT-4",
            total_tokens=1_000_000,
            custom_carbon_per_million=0.5
        )
        
        # 1M tokens * 0.5 kg CO2 / 1M tokens = 0.5 kg = 500 g
        assert result["carbon_kg"] == pytest.approx(0.5, rel=1e-4)
        assert result["carbon_g"] == pytest.approx(500.0, rel=1e-1)
    
    def test_zero_tokens(self):
        """Test avec 0 tokens."""
        result = calculate_api_carbon("GPT-4", total_tokens=0)
        
        assert result["carbon_kg"] == 0.0
        assert result["carbon_g"] == 0.0
        assert result["co2_car_km"] == 0.0
    
    def test_negative_tokens(self):
        """Test avec des tokens négatifs (doit lever ValueError)."""
        with pytest.raises(ValueError):
            calculate_api_carbon("GPT-4", total_tokens=-100)
    
    def test_unknown_model_default(self):
        """Test avec un modèle inconnu (doit utiliser GPT-4 par défaut)."""
        result = calculate_api_carbon("Unknown-Model", total_tokens=1_000_000)
        assert result["model"] == "GPT-4"


class TestGetSaasMonthlyCarbon:
    """Tests pour get_saas_monthly_carbon."""
    
    def test_chatgpt_plus(self):
        """Test de l'empreinte carbone mensuelle de ChatGPT Plus."""
        carbon = get_saas_monthly_carbon("ChatGPT-Plus")
        assert carbon == 0.3  # 0.3 kg CO2/mois
    
    def test_copilot(self):
        """Test de l'empreinte carbone mensuelle de Copilot."""
        carbon = get_saas_monthly_carbon("Copilot")
        assert carbon == 0.15  # 0.15 kg CO2/mois
    
    def test_midjourney(self):
        """Test de l'empreinte carbone mensuelle de Midjourney."""
        carbon = get_saas_monthly_carbon("Midjourney")
        assert carbon == 0.5  # 0.5 kg CO2/mois
    
    def test_unknown_saas(self):
        """Test avec un SaaS inconnu (doit retourner None)."""
        carbon = get_saas_monthly_carbon("Unknown-SaaS")
        assert carbon is None


class TestCalculateSaasCarbon:
    """Tests pour calculate_saas_carbon."""
    
    def test_basic_calculation(self):
        """Test de calcul de base pour ChatGPT Plus."""
        result = calculate_saas_carbon("ChatGPT-Plus", quantity=1, duration_months=1)
        
        assert result["saas_name"] == "ChatGPT-Plus"
        assert result["monthly_carbon_kg"] == 0.3
        assert result["quantity"] == 1
        assert result["duration_months"] == 1
        assert result["total_carbon_kg"] == pytest.approx(0.3, rel=1e-4)
        assert result["total_carbon_g"] == pytest.approx(300.0, rel=1e-1)
        assert result["co2_car_km"] == pytest.approx(1500.0, rel=1e-1)  # 300g / 0.2 = 1500 km
    
    def test_multiple_users(self):
        """Test avec plusieurs utilisateurs."""
        result = calculate_saas_carbon("ChatGPT-Plus", quantity=5, duration_months=1)
        
        # 5 utilisateurs * 0.3 kg = 1.5 kg = 1500 g
        assert result["total_carbon_kg"] == pytest.approx(1.5, rel=1e-4)
        assert result["total_carbon_g"] == pytest.approx(1500.0, rel=1e-1)
    
    def test_multiple_months(self):
        """Test sur plusieurs mois."""
        result = calculate_saas_carbon("ChatGPT-Plus", quantity=1, duration_months=12)
        
        # 12 mois * 0.3 kg = 3.6 kg = 3600 g
        assert result["total_carbon_kg"] == pytest.approx(3.6, rel=1e-4)
        assert result["total_carbon_g"] == pytest.approx(3600.0, rel=1e-1)
    
    def test_negative_values(self):
        """Test avec des valeurs négatives (doit lever ValueError)."""
        with pytest.raises(ValueError):
            calculate_saas_carbon("ChatGPT-Plus", quantity=-1, duration_months=1)
        
        with pytest.raises(ValueError):
            calculate_saas_carbon("ChatGPT-Plus", quantity=1, duration_months=-1)


class TestCalculateTotalCarbon:
    """Tests pour calculate_total_carbon."""
    
    def test_api_only(self):
        """Test avec uniquement des émissions API."""
        api_usage = {"carbon_g": 500.0}
        result = calculate_total_carbon(api_usage=api_usage, saas_subscriptions=None)
        
        assert result["api_carbon_g"] == 500.0
        assert result["saas_carbon_g"] == 0.0
        assert result["total_carbon_g"] == 500.0
        assert result["total_co2_car_km"] == pytest.approx(2500.0, rel=1e-1)  # 500g / 0.2
    
    def test_saas_only(self):
        """Test avec uniquement des émissions SaaS."""
        saas_subscriptions = [
            {"total_carbon_g": 200.0},
            {"total_carbon_g": 300.0}
        ]
        result = calculate_total_carbon(api_usage=None, saas_subscriptions=saas_subscriptions)
        
        assert result["api_carbon_g"] == 0.0
        assert result["saas_carbon_g"] == 500.0
        assert result["total_carbon_g"] == 500.0
    
    def test_combined(self):
        """Test avec des émissions API et SaaS combinées."""
        api_usage = {"carbon_g": 200.0}
        saas_subscriptions = [
            {"total_carbon_g": 300.0}
        ]
        result = calculate_total_carbon(api_usage=api_usage, saas_subscriptions=saas_subscriptions)
        
        assert result["api_carbon_g"] == 200.0
        assert result["saas_carbon_g"] == 300.0
        assert result["total_carbon_g"] == 500.0
    
    def test_empty_inputs(self):
        """Test avec des entrées vides."""
        result = calculate_total_carbon(api_usage=None, saas_subscriptions=None)
        
        assert result["api_carbon_g"] == 0.0
        assert result["saas_carbon_g"] == 0.0
        assert result["total_carbon_g"] == 0.0
        assert result["total_co2_car_km"] == 0.0
