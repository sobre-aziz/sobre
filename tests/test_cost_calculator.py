"""
Tests unitaires pour le module cost_calculator.

Exécutez avec: pytest tests/test_cost_calculator.py -v
"""

import pytest
from utils.cost_calculator import (
    calculate_api_cost,
    calculate_saas_cost,
    calculate_total_cost,
    get_model_cost_per_token,
    get_saas_monthly_cost,
    MODELS,
    SAAS_SUBSCRIPTIONS
)


class TestGetModelCostPerToken:
    """Tests pour get_model_cost_per_token."""
    
    def test_gpt4_input_cost(self):
        """Test du coût par token d'entrée pour GPT-4."""
        cost = get_model_cost_per_token("GPT-4", "input")
        assert cost == 0.00003  # 0.03€ par 1k tokens
    
    def test_gpt4_output_cost(self):
        """Test du coût par token de sortie pour GPT-4."""
        cost = get_model_cost_per_token("GPT-4", "output")
        assert cost == 0.00006  # 0.06€ par 1k tokens
    
    def test_mistral7b_cost(self):
        """Test du coût par token pour Mistral-7B (pas de distinction input/output)."""
        input_cost = get_model_cost_per_token("Mistral-7B", "input")
        output_cost = get_model_cost_per_token("Mistral-7B", "output")
        assert input_cost == 0.000002
        assert output_cost == 0.000002
    
    def test_unknown_model(self):
        """Test avec un modèle inconnu (doit retourner None)."""
        cost = get_model_cost_per_token("Unknown-Model", "input")
        assert cost is None
    
    def test_invalid_token_type(self):
        """Test avec un type de token invalide (doit lever ValueError)."""
        with pytest.raises(ValueError):
            get_model_cost_per_token("GPT-4", "invalid")


class TestCalculateApiCost:
    """Tests pour calculate_api_cost."""
    
    def test_basic_calculation(self):
        """Test de calcul de base pour GPT-4."""
        result = calculate_api_cost("GPT-4", input_tokens=1000, output_tokens=500)
        
        expected_input_cost = 1000 * 0.00003  # 0.03€
        expected_output_cost = 500 * 0.00006  # 0.03€
        expected_total = expected_input_cost + expected_output_cost
        
        assert result["model"] == "GPT-4"
        assert result["input_tokens"] == 1000
        assert result["output_tokens"] == 500
        assert result["total_tokens"] == 1500
        assert result["input_cost"] == pytest.approx(expected_input_cost, rel=1e-6)
        assert result["output_cost"] == pytest.approx(expected_output_cost, rel=1e-6)
        assert result["total_cost"] == pytest.approx(expected_total, rel=1e-2)
    
    def test_zero_output_tokens(self):
        """Test avec 0 tokens de sortie."""
        result = calculate_api_cost("GPT-4", input_tokens=1000, output_tokens=0)
        
        expected_cost = 1000 * 0.00003  # Seulement le coût d'entrée
        
        assert result["total_cost"] == pytest.approx(expected_cost, rel=1e-2)
    
    def test_custom_costs(self):
        """Test avec des coûts personnalisés."""
        result = calculate_api_cost(
            "GPT-4",
            input_tokens=1000,
            output_tokens=500,
            custom_input_cost=0.00001,
            custom_output_cost=0.00002
        )
        
        expected_input_cost = 1000 * 0.00001  # 0.01€
        expected_output_cost = 500 * 0.00002  # 0.01€
        expected_total = 0.02
        
        assert result["total_cost"] == pytest.approx(expected_total, rel=1e-2)
    
    def test_negative_tokens(self):
        """Test avec des tokens négatifs (doit lever ValueError)."""
        with pytest.raises(ValueError):
            calculate_api_cost("GPT-4", input_tokens=-100, output_tokens=0)
        
        with pytest.raises(ValueError):
            calculate_api_cost("GPT-4", input_tokens=100, output_tokens=-50)
    
    def test_unknown_model_default(self):
        """Test avec un modèle inconnu (doit utiliser GPT-4 par défaut)."""
        result = calculate_api_cost("Unknown-Model", input_tokens=1000, output_tokens=0)
        assert result["model"] == "GPT-4"


class TestGetSaasMonthlyCost:
    """Tests pour get_saas_monthly_cost."""
    
    def test_chatgpt_plus(self):
        """Test du coût mensuel de ChatGPT Plus."""
        cost = get_saas_monthly_cost("ChatGPT-Plus")
        assert cost == 20.00
    
    def test_copilot(self):
        """Test du coût mensuel de Copilot."""
        cost = get_saas_monthly_cost("Copilot")
        assert cost == 10.00
    
    def test_unknown_saas(self):
        """Test avec un SaaS inconnu (doit retourner None)."""
        cost = get_saas_monthly_cost("Unknown-SaaS")
        assert cost is None


class TestCalculateSaasCost:
    """Tests pour calculate_saas_cost."""
    
    def test_basic_calculation(self):
        """Test de calcul de base pour ChatGPT Plus."""
        result = calculate_saas_cost("ChatGPT-Plus", quantity=1, duration_months=1)
        
        assert result["saas_name"] == "ChatGPT-Plus"
        assert result["monthly_cost"] == 20.00
        assert result["quantity"] == 1
        assert result["duration_months"] == 1
        assert result["total_cost"] == 20.00
    
    def test_multiple_users(self):
        """Test avec plusieurs utilisateurs."""
        result = calculate_saas_cost("ChatGPT-Plus", quantity=5, duration_months=1)
        
        assert result["total_cost"] == 100.00  # 20€ * 5 utilisateurs
    
    def test_multiple_months(self):
        """Test sur plusieurs mois."""
        result = calculate_saas_cost("ChatGPT-Plus", quantity=1, duration_months=12)
        
        assert result["total_cost"] == 240.00  # 20€ * 12 mois
    
    def test_negative_values(self):
        """Test avec des valeurs négatives (doit lever ValueError)."""
        with pytest.raises(ValueError):
            calculate_saas_cost("ChatGPT-Plus", quantity=-1, duration_months=1)
        
        with pytest.raises(ValueError):
            calculate_saas_cost("ChatGPT-Plus", quantity=1, duration_months=-1)


class TestCalculateTotalCost:
    """Tests pour calculate_total_cost."""
    
    def test_api_only(self):
        """Test avec uniquement des coûts API."""
        api_usage = {"total_cost": 50.00}
        result = calculate_total_cost(api_usage=api_usage, saas_subscriptions=None)
        
        assert result["api_cost"] == 50.00
        assert result["saas_cost"] == 0.00
        assert result["total_cost"] == 50.00
    
    def test_saas_only(self):
        """Test avec uniquement des coûts SaaS."""
        saas_subscriptions = [
            {"total_cost": 20.00},
            {"total_cost": 30.00}
        ]
        result = calculate_total_cost(api_usage=None, saas_subscriptions=saas_subscriptions)
        
        assert result["api_cost"] == 0.00
        assert result["saas_cost"] == 50.00
        assert result["total_cost"] == 50.00
    
    def test_combined(self):
        """Test avec des coûts API et SaaS combinés."""
        api_usage = {"total_cost": 50.00}
        saas_subscriptions = [
            {"total_cost": 20.00},
            {"total_cost": 30.00}
        ]
        result = calculate_total_cost(api_usage=api_usage, saas_subscriptions=saas_subscriptions)
        
        assert result["api_cost"] == 50.00
        assert result["saas_cost"] == 50.00
        assert result["total_cost"] == 100.00
    
    def test_empty_inputs(self):
        """Test avec des entrées vides."""
        result = calculate_total_cost(api_usage=None, saas_subscriptions=None)
        
        assert result["api_cost"] == 0.00
        assert result["saas_cost"] == 0.00
        assert result["total_cost"] == 0.00
