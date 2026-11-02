"""
Tests de validation pour les modèles dans config/models.yaml.

Ce test vérifie que chaque modèle et SaaS dans config/models.yaml
contient les champs obligatoires : source, date_maj, niveau_confiance.
"""

import yaml
import pytest
from pathlib import Path


class TestModelsValidation:
    """Tests pour valider la structure des modèles dans config/models.yaml."""

    @pytest.fixture
    def models_config(self):
        """Charge la configuration des modèles depuis config/models.yaml."""
        config_path = Path(__file__).parent.parent / "config" / "models.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_all_models_have_required_fields(self, models_config):
        """Vérifie que tous les modèles ont les champs source, date_maj, niveau_confiance."""
        required_fields = ["source", "date_maj", "niveau_confiance"]
        models = models_config.get("models", {})
        
        for model_name, model_data in models.items():
            for field in required_fields:
                assert field in model_data, (
                    f"Modèle '{model_name}' manque le champ obligatoire '{field}'"
                )
                assert model_data[field] is not None, (
                    f"Modèle '{model_name}' a un champ '{field}' vide ou null"
                )

    def test_all_saas_have_required_fields(self, models_config):
        """Vérifie que tous les SaaS ont les champs source, date_maj, niveau_confiance."""
        required_fields = ["source", "date_maj", "niveau_confiance"]
        saas_subscriptions = models_config.get("saas_subscriptions", {})
        
        for saas_name, saas_data in saas_subscriptions.items():
            for field in required_fields:
                assert field in saas_data, (
                    f"SaaS '{saas_name}' manque le champ obligatoire '{field}'"
                )
                assert saas_data[field] is not None, (
                    f"SaaS '{saas_name}' a un champ '{field}' vide ou null"
                )

    def test_niveau_confiance_values(self, models_config):
        """Vérifie que les niveaux de confiance sont valides."""
        valid_confidence_levels = [
            "mesure",
            "publie_par_fournisseur",
            "estimation_par_analogie",
        ]
        
        # Vérifier les modèles
        models = models_config.get("models", {})
        for model_name, model_data in models.items():
            assert model_data["niveau_confiance"] in valid_confidence_levels, (
                f"Modèle '{model_name}' a un niveau de confiance invalide : "
                f"'{model_data['niveau_confiance']}'"
            )
        
        # Vérifier les SaaS
        saas_subscriptions = models_config.get("saas_subscriptions", {})
        for saas_name, saas_data in saas_subscriptions.items():
            assert saas_data["niveau_confiance"] in valid_confidence_levels, (
                f"SaaS '{saas_name}' a un niveau de confiance invalide : "
                f"'{saas_data['niveau_confiance']}'"
            )

    def test_source_urls_are_valid(self, models_config):
        """Vérifie que les URLs des sources sont des URLs valides (format basique)."""
        # Vérifier les modèles
        models = models_config.get("models", {})
        for model_name, model_data in models.items():
            source = model_data.get("source", "")
            if source and source != "Source inconnue":
                assert source.startswith("http"), (
                    f"Modèle '{model_name}' a une URL de source invalide : '{source}'"
                )
        
        # Vérifier les SaaS
        saas_subscriptions = models_config.get("saas_subscriptions", {})
        for saas_name, saas_data in saas_subscriptions.items():
            source = saas_data.get("source", "")
            if source and source != "Source inconnue":
                assert source.startswith("http"), (
                    f"SaaS '{saas_name}' a une URL de source invalide : '{source}'"
                )

    def test_date_maj_format(self, models_config):
        """Vérifie que les dates de mise à jour sont au format YYYY-MM-DD."""
        import re
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        
        # Vérifier les modèles
        models = models_config.get("models", {})
        for model_name, model_data in models.items():
            date_maj = model_data.get("date_maj", "")
            assert date_pattern.match(date_maj), (
                f"Modèle '{model_name}' a un format de date invalide : '{date_maj}'"
            )
        
        # Vérifier les SaaS
        saas_subscriptions = models_config.get("saas_subscriptions", {})
        for saas_name, saas_data in saas_subscriptions.items():
            date_maj = saas_data.get("date_maj", "")
            assert date_pattern.match(date_maj), (
                f"SaaS '{saas_name}' a un format de date invalide : '{date_maj}'"
            )


class TestCarbonFactorsValidation:
    """Tests pour valider les facteurs CO₂."""

    @pytest.fixture
    def models_config(self):
        """Charge la configuration des modèles depuis config/models.yaml."""
        config_path = Path(__file__).parent.parent / "config" / "models.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_all_models_have_co2_factor(self, models_config):
        """Vérifie que tous les modèles ont un facteur CO₂."""
        models = models_config.get("models", {})
        for model_name, model_data in models.items():
            assert "co2_per_million_tokens" in model_data, (
                f"Modèle '{model_name}' manque le champ 'co2_per_million_tokens'"
            )
            assert model_data["co2_per_million_tokens"] >= 0, (
                f"Modèle '{model_name}' a un facteur CO₂ négatif"
            )

    def test_all_saas_have_co2_factor(self, models_config):
        """Vérifie que tous les SaaS ont un facteur CO₂."""
        saas_subscriptions = models_config.get("saas_subscriptions", {})
        for saas_name, saas_data in saas_subscriptions.items():
            assert "co2_per_month" in saas_data or "co2_per_million_tokens" in saas_data, (
                f"SaaS '{saas_name}' manque un champ CO₂ (co2_per_month ou co2_per_million_tokens)"
            )
            co2_field = saas_data.get("co2_per_month") or saas_data.get("co2_per_million_tokens")
            assert co2_field >= 0, (
                f"SaaS '{saas_name}' a un facteur CO₂ négatif"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
