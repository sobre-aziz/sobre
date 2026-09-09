"""
Tests unitaires pour le module greenops_scoring.

Exécutez avec: pytest tests/test_greenops_scoring.py -v
"""

import pytest
from utils.greenops_scoring import (
    calculate_greenops_score,
    get_greenops_grade,
    generate_greenops_recommendations,
    calculate_potential_savings
)


class TestCalculateGreenopsScore:
    """Tests pour calculate_greenops_score."""
    
    def test_grade_a(self):
        """Test pour obtenir le grade A."""
        result = calculate_greenops_score(
            total_cost=100.0,  # 10€/employé pour 10 employés
            total_carbon_g=500.0,  # 50g/employé pour 10 employés
            number_of_employees=10,
            number_of_licenses=10,
            dormant_licenses_count=0  # 100% de licences actives
        )
        
        assert result["grade"] == "A"
        assert result["grade_name"] == "A - Excellent"
        assert result["score"] == 100
        assert result["cost_per_employee"] == 10.0
        assert result["carbon_per_employee"] == 50.0
        assert result["active_licenses_percentage"] == 100.0
    
    def test_grade_b(self):
        """Test pour obtenir le grade B."""
        result = calculate_greenops_score(
            total_cost=200.0,  # 20€/employé pour 10 employés
            total_carbon_g=1000.0,  # 100g/employé pour 10 employés
            number_of_employees=10,
            number_of_licenses=10,
            dormant_licenses_count=0  # 100% de licences actives
        )
        
        assert result["grade"] == "B"
        assert result["grade_name"] == "B - Bon"
        assert result["score"] == 80
    
    def test_grade_c(self):
        """Test pour obtenir le grade C."""
        result = calculate_greenops_score(
            total_cost=400.0,  # 40€/employé pour 10 employés
            total_carbon_g=2000.0,  # 200g/employé pour 10 employés
            number_of_employees=10,
            number_of_licenses=10,
            dormant_licenses_count=1  # 90% de licences actives
        )
        
        assert result["grade"] == "C"
        assert result["grade_name"] == "C - Moyen"
        assert result["score"] == 60
    
    def test_grade_d(self):
        """Test pour obtenir le grade D."""
        result = calculate_greenops_score(
            total_cost=800.0,  # 80€/employé pour 10 employés
            total_carbon_g=4000.0,  # 400g/employé pour 10 employés
            number_of_employees=10,
            number_of_licenses=10,
            dormant_licenses_count=3  # 70% de licences actives
        )
        
        assert result["grade"] == "D"
        assert result["grade_name"] == "D - À améliorer"
        assert result["score"] == 40
    
    def test_grade_e(self):
        """Test pour obtenir le grade E."""
        result = calculate_greenops_score(
            total_cost=5000.0,  # 500€/employé pour 10 employés
            total_carbon_g=20000.0,  # 2000g/employé pour 10 employés
            number_of_employees=10,
            number_of_licenses=10,
            dormant_licenses_count=5  # 50% de licences actives
        )
        
        assert result["grade"] == "E"
        assert result["grade_name"] == "E - Critique"
        assert result["score"] == 20
    
    def test_zero_employees(self):
        """Test avec 0 employés (doit lever ValueError)."""
        with pytest.raises(ValueError):
            calculate_greenops_score(
                total_cost=100.0,
                total_carbon_g=500.0,
                number_of_employees=0,
                number_of_licenses=10,
                dormant_licenses_count=0
            )
    
    def test_with_dormant_licenses(self):
        """Test avec des licences dormantes."""
        result = calculate_greenops_score(
            total_cost=100.0,
            total_carbon_g=500.0,
            number_of_employees=10,
            number_of_licenses=20,
            dormant_licenses_count=5  # 75% de licences actives
        )
        
        assert result["active_licenses_percentage"] == 75.0


class TestGetGreenopsGrade:
    """Tests pour get_greenops_grade."""
    
    def test_grade_a(self):
        """Test pour le grade A."""
        grade, grade_name, score = get_greenops_grade(
            cost_per_employee=5.0,
            carbon_per_employee=25.0,
            active_licenses_percentage=100.0
        )
        
        assert grade == "A"
        assert "Excellent" in grade_name
        assert score == 100
    
    def test_grade_b(self):
        """Test pour le grade B."""
        grade, grade_name, score = get_greenops_grade(
            cost_per_employee=20.0,
            carbon_per_employee=100.0,
            active_licenses_percentage=95.0
        )
        
        assert grade == "B"
        assert "Bon" in grade_name
        assert score == 80
    
    def test_grade_e(self):
        """Test pour le grade E (par défaut)."""
        grade, grade_name, score = get_greenops_grade(
            cost_per_employee=1000.0,
            carbon_per_employee=5000.0,
            active_licenses_percentage=0.0
        )
        
        assert grade == "E"
        assert "Critique" in grade_name
        assert score == 20


class TestGenerateGreenopsRecommendations:
    """Tests pour generate_greenops_recommendations."""
    
    def test_grade_e_recommendations(self):
        """Test des recommandations pour le grade E."""
        greenops_result = {
            "grade": "E",
            "grade_name": "E - Critique",
            "score": 20,
            "cost_per_employee": 500.0,
            "carbon_per_employee": 2000.0,
            "active_licenses_percentage": 50.0
        }
        
        recommendations = generate_greenops_recommendations(
            greenops_result,
            total_cost=5000.0,
            total_carbon_g=20000.0,
            dormant_licenses=[{"name": "ChatGPT Plus"}]
        )
        
        assert len(recommendations) > 0
        assert any("Urgence" in rec for rec in recommendations)
        assert any("dormante" in rec.lower() for rec in recommendations)
    
    def test_grade_a_recommendations(self):
        """Test des recommandations pour le grade A."""
        greenops_result = {
            "grade": "A",
            "grade_name": "A - Excellent",
            "score": 100,
            "cost_per_employee": 5.0,
            "carbon_per_employee": 25.0,
            "active_licenses_percentage": 100.0
        }
        
        recommendations = generate_greenops_recommendations(
            greenops_result,
            total_cost=100.0,
            total_carbon_g=500.0,
            dormant_licenses=[]
        )
        
        assert len(recommendations) > 0
        assert any("Excellent" in rec for rec in recommendations)
    
    def test_with_dormant_licenses(self):
        """Test avec des licences dormantes."""
        greenops_result = {
            "grade": "C",
            "grade_name": "C - Moyen",
            "score": 60,
            "cost_per_employee": 40.0,
            "carbon_per_employee": 200.0,
            "active_licenses_percentage": 80.0
        }
        
        recommendations = generate_greenops_recommendations(
            greenops_result,
            total_cost=400.0,
            total_carbon_g=2000.0,
            dormant_licenses=[{"name": "SaaS 1"}, {"name": "SaaS 2"}]
        )
        
        assert any("2 licence" in rec for rec in recommendations)


class TestCalculatePotentialSavings:
    """Tests pour calculate_potential_savings."""
    
    def test_no_dormant_licenses(self):
        """Test sans licences dormantes."""
        result = calculate_potential_savings(
            total_cost=100.0,
            total_carbon_g=500.0,
            dormant_licenses=[],
            saas_subscriptions=[{"name": "ChatGPT Plus", "monthly_cost": 20.0, "monthly_carbon_kg": 0.3}]
        )
        
        assert result["cost_savings"] == 0.0
        assert result["carbon_savings_g"] == 0.0
        assert result["percentage_cost_savings"] == 0.0
        assert result["percentage_carbon_savings"] == 0.0
    
    def test_with_dormant_licenses(self):
        """Test avec des licences dormantes."""
        saas_subscriptions = [
            {"name": "ChatGPT Plus", "monthly_cost": 20.0, "monthly_carbon_kg": 0.3},
            {"name": "Copilot", "monthly_cost": 10.0, "monthly_carbon_kg": 0.15}
        ]
        
        dormant_licenses = [
            {"name": "Copilot"}  # Copilot est dormant
        ]
        
        result = calculate_potential_savings(
            total_cost=30.0,  # 20 + 10
            total_carbon_g=450.0,  # 300 + 150
            dormant_licenses=dormant_licenses,
            saas_subscriptions=saas_subscriptions
        )
        
        assert result["cost_savings"] == 10.0
        assert result["carbon_savings_g"] == 150.0
        assert result["percentage_cost_savings"] == pytest.approx(33.33, rel=1e-2)
        assert result["percentage_carbon_savings"] == pytest.approx(33.33, rel=1e-2)
    
    def test_all_dormant(self):
        """Test avec toutes les licences dormantes."""
        saas_subscriptions = [
            {"name": "ChatGPT Plus", "monthly_cost": 20.0, "monthly_carbon_kg": 0.3}
        ]
        
        dormant_licenses = [
            {"name": "ChatGPT Plus"}
        ]
        
        result = calculate_potential_savings(
            total_cost=20.0,
            total_carbon_g=300.0,
            dormant_licenses=dormant_licenses,
            saas_subscriptions=saas_subscriptions
        )
        
        assert result["cost_savings"] == 20.0
        assert result["carbon_savings_g"] == 300.0
        assert result["percentage_cost_savings"] == 100.0
        assert result["percentage_carbon_savings"] == 100.0
