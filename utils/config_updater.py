"""
Config Updater Module for Sobre

Ce module permet de mettre à jour automatiquement les tarifs des modèles IA
et les facteurs d'émission CO2 depuis les sources officielles.

Fonctionnalités:
    - Récupération des tarifs depuis les API des fournisseurs
    - Mise à jour des facteurs CO2 depuis les rapports scientifiques
    - Validation et sauvegarde des données dans models.yaml
    - Système de cache pour éviter les requêtes inutiles
    - Notifications en cas de mise à jour
"""

import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import requests
import yaml

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ConfigUpdater:
    """
    Classe principale pour la mise à jour de la configuration.
    """

    def __init__(self):
        """
        Initialise le ConfigUpdater avec les chemins et configurations.
        """
        self.config_path = Path(__file__).parent.parent / "config" / "models.yaml"
        self.sources_path = Path(__file__).parent.parent / "config" / "sources.json"
        self.cache_path = Path(__file__).parent.parent / ".cache" / "config_cache.json"
        self.last_update_path = (
            Path(__file__).parent.parent / ".cache" / "last_update.txt"
        )

        # Créer le dossier cache si inexistant
        self.cache_path.parent.mkdir(exist_ok=True)

        # Charger les sources
        self.sources = self._load_sources()
        self.current_config = self._load_config()
        self.cache = self._load_cache()

    def _load_sources(self) -> Dict:
        """Charge les sources depuis sources.json."""
        try:
            with open(self.sources_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement des sources: {e}")
            return {}

    def _load_config(self) -> Dict:
        """Charge la configuration actuelle depuis models.yaml."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la config: {e}")
            return {}

    def _load_cache(self) -> Dict:
        """Charge le cache depuis le fichier cache."""
        try:
            if self.cache_path.exists():
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Erreur lors du chargement du cache: {e}")
        return {"models": {}, "saas": {}, "last_update": None}

    def _save_cache(self, cache: Dict):
        """Sauvegarde le cache dans le fichier."""
        try:
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du cache: {e}")

    def _save_config(self, config: Dict):
        """Sauvegarde la configuration dans models.yaml."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    config,
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                )

            # Sauvegarder la date de dernière mise à jour
            with open(self.last_update_path, "w", encoding="utf-8") as f:
                f.write(datetime.now().isoformat())

            logger.info(f"Configuration mise à jour: {datetime.now().isoformat()}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la config: {e}")
            raise

    def _get_last_update_time(self) -> Optional[datetime]:
        """Récupère la date de dernière mise à jour."""
        try:
            if self.last_update_path.exists():
                with open(self.last_update_path, "r", encoding="utf-8") as f:
                    return datetime.fromisoformat(f.read().strip())
        except Exception as e:
            logger.warning(f"Erreur lors de la lecture de last_update: {e}")
        return None

    def _is_cache_valid(self, cache_key: str, max_age_hours: int = 24) -> bool:
        """Vérifie si le cache est encore valide."""
        if cache_key not in self.cache:
            return False

        if "timestamp" not in self.cache[cache_key]:
            return False

        cache_time = datetime.fromisoformat(self.cache[cache_key]["timestamp"])
        return (datetime.now() - cache_time) < timedelta(hours=max_age_hours)

    def _fetch_with_cache(
        self, url: str, cache_key: str, max_age_hours: int = 24
    ) -> Optional[str]:
        """
        Récupère des données depuis une URL avec cache.
        """
        # Vérifier le cache
        if self._is_cache_valid(cache_key, max_age_hours):
            logger.info(f"Utilisation du cache pour {cache_key}")
            return self.cache[cache_key]["data"]

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Mettre à jour le cache
            self.cache[cache_key] = {
                "data": response.text,
                "timestamp": datetime.now().isoformat(),
                "url": url,
            }
            self._save_cache(self.cache)

            return response.text
        except Exception as e:
            logger.warning(f"Erreur lors de la récupération de {url}: {e}")
            return None

    def _extract_price_from_text(self, text: str, pattern: str) -> Optional[float]:
        """
        Extrait un prix depuis un texte en utilisant un pattern regex.
        """
        try:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                price_str = match.group(1)
                # Nettoyer la chaîne (supprimer les symboles, espaces)
                price_str = re.sub(r"[^\d.]", "", price_str)
                if price_str:
                    return float(price_str)
        except Exception as e:
            logger.warning(f"Erreur lors de l'extraction du prix: {e}")
        return None

    def _scrape_pricing_page(self, url: str, model_name: str) -> Optional[Dict]:
        """
        Extrait les informations de tarification depuis une page web.
        """
        try:
            html = self._fetch_with_cache(url, f"pricing_{model_name}", max_age_hours=1)
            if not html:
                return None

            # Patterns pour extraire les prix (en $ ou €)
            # Exemple: "$0.03 per 1K tokens" ou "0.003€/1k tokens"
            patterns = {
                "input": r"input[\s\S]*?([\d.]+)\s*(?:\$|€|USD|EUR)",
                "output": r"output[\s\S]*?([\d.]+)\s*(?:\$|€|USD|EUR)",
                "monthly": r"([\d.]+)\s*(?:\$|€|USD|EUR)\s*(?:per\s*)?month",
            }

            result = {}
            for key, pattern in patterns.items():
                price = self._extract_price_from_text(html, pattern)
                if price:
                    result[key] = price

            return result if result else None

        except Exception as e:
            logger.warning(f"Erreur lors du scraping de {url}: {e}")
            return None

    def update_model_pricing(self, provider: str, model_name: str) -> bool:
        """
        Met à jour les tarifs pour un modèle spécifique.
        """
        if provider not in self.sources.get("sources", {}):
            logger.warning(f"Fournisseur inconnu: {provider}")
            return False

        provider_info = self.sources["sources"][provider]

        # Récupérer les informations depuis l'API ou la page web
        pricing_info = self._scrape_pricing_page(
            provider_info.get("pricing_page", ""), model_name
        )

        if not pricing_info:
            logger.warning(f"Impossible de récupérer les tarifs pour {model_name}")
            return False

        # Mettre à jour la configuration
        if "models" not in self.current_config:
            self.current_config["models"] = {}

        if model_name not in self.current_config["models"]:
            self.current_config["models"][model_name] = {}

        model_config = self.current_config["models"][model_name]

        # Mettre à jour les coûts
        if "input" in pricing_info:
            model_config["cost_per_token_input"] = (
                pricing_info["input"] / 1000
            )  # Convertir $/1K en $/token
        if "output" in pricing_info:
            model_config["cost_per_token_output"] = pricing_info["output"] / 1000

        # Sauvegarder
        self._save_config(self.current_config)
        logger.info(f"Tarifs mis à jour pour {model_name}: {pricing_info}")
        return True

    def update_all_models_pricing(self) -> Dict[str, List[str]]:
        """
        Met à jour les tarifs pour tous les modèles.

        Returns:
            Dict: {"success": List[str], "failed": List[str]}
        """
        results = {"success": [], "failed": []}

        for provider, provider_info in self.sources.get("sources", {}).items():
            if provider == "SaaS":
                continue  # On gère les SaaS séparément

            models = provider_info.get("models", [])
            for model in models:
                if self.update_model_pricing(provider, model):
                    results["success"].append(f"{provider}/{model}")
                else:
                    results["failed"].append(f"{provider}/{model}")

        return results

    def update_saas_pricing(self, saas_name: str) -> bool:
        """
        Met à jour les tarifs pour un SaaS spécifique.
        """
        saas_info = self.sources.get("sources", {}).get("SaaS", {}).get(saas_name, {})
        if not saas_info:
            logger.warning(f"SaaS inconnu: {saas_name}")
            return False

        pricing_page = saas_info.get("pricing_page", "")
        if not pricing_page:
            logger.warning(f"Pas de page de tarification pour {saas_name}")
            return False

        # Récupérer le prix mensuel
        html = self._fetch_with_cache(
            pricing_page, f"saas_pricing_{saas_name}", max_age_hours=24
        )
        if not html:
            return False

        # Extraire le prix mensuel
        # Pattern pour trouver un prix mensuel (ex: "$20/month" ou "20€/mois")
        monthly_price = self._extract_price_from_text(
            html, r"([\d.]+)\s*(?:\$|€|USD|EUR)\s*(?:per\s*)?month|mois"
        )

        if not monthly_price:
            logger.warning(f"Impossible d'extraire le prix pour {saas_name}")
            return False

        # Mettre à jour la configuration
        if "saas_subscriptions" not in self.current_config:
            self.current_config["saas_subscriptions"] = {}

        if saas_name not in self.current_config["saas_subscriptions"]:
            self.current_config["saas_subscriptions"][saas_name] = {}

        saas_config = self.current_config["saas_subscriptions"][saas_name]
        saas_config["monthly_cost"] = monthly_price

        # Sauvegarder
        self._save_config(self.current_config)
        logger.info(f"Tarif SaaS mis à jour pour {saas_name}: {monthly_price}")
        return True

    def update_all_saas_pricing(self) -> Dict[str, List[str]]:
        """
        Met à jour les tarifs pour tous les SaaS.

        Returns:
            Dict: {"success": List[str], "failed": List[str]}
        """
        results = {"success": [], "failed": []}

        saas_list = self.sources.get("sources", {}).get("SaaS", {})
        for saas_name in saas_list:
            if self.update_saas_pricing(saas_name):
                results["success"].append(saas_name)
            else:
                results["failed"].append(saas_name)

        return results

    def update_co2_factors(self) -> Dict[str, List[str]]:
        """
        Met à jour les facteurs d'émission CO2 depuis les sources scientifiques.

        Returns:
            Dict: {"success": List[str], "failed": List[str]}
        """
        results = {"success": [], "failed": []}

        # Pour l'instant, on utilise des valeurs par défaut basées sur des études
        # Dans une version future, on pourrait récupérer ces données depuis des API

        # Facteurs CO2 par million de tokens (kg)
        co2_factors = {
            "GPT-4": 0.3,
            "GPT-3.5-turbo": 0.2,
            "Mistral-7B": 0.05,
            "Mistral-8x7B": 0.03,
            "Llama-2-70B": 0.03,
            "Llama-3": 0.04,
            "Gemini-1.5-Pro": 0.25,
            "Claude-3-Sonnet": 0.22,
            "Claude-3-Haiku": 0.15,
            "Command-R": 0.18,
        }

        # Mettre à jour les modèles
        if "models" not in self.current_config:
            self.current_config["models"] = {}

        for model_name, co2_factor in co2_factors.items():
            if model_name in self.current_config["models"]:
                self.current_config["models"][model_name][
                    "co2_per_million_tokens"
                ] = co2_factor
                results["success"].append(model_name)
            else:
                results["failed"].append(model_name)

        # Facteurs CO2 pour les SaaS (kg/mois)
        saas_co2_factors = {
            "ChatGPT-Plus": 0.3,
            "ChatGPT-Enterprise": 1.5,
            "Copilot": 0.15,
            "Copilot-Business": 0.3,
            "Notion-AI": 0.075,
            "Midjourney": 0.5,
            "Canva-Magic": 0.06,
        }

        if "saas_subscriptions" not in self.current_config:
            self.current_config["saas_subscriptions"] = {}

        for saas_name, co2_factor in saas_co2_factors.items():
            if saas_name in self.current_config["saas_subscriptions"]:
                self.current_config["saas_subscriptions"][saas_name][
                    "co2_per_month"
                ] = co2_factor
                results["success"].append(saas_name)
            else:
                results["failed"].append(saas_name)

        # Sauvegarder
        self._save_config(self.current_config)
        logger.info(f"Facteurs CO2 mis à jour: {len(results['success'])} succès")

        return results

    def update_all(self) -> Dict:
        """
        Met à jour tous les tarifs et facteurs CO2.

        Returns:
            Dict: {
                "models_pricing": {"success": [], "failed": []},
                "saas_pricing": {"success": [], "failed": []},
                "co2_factors": {"success": [], "failed": []},
                "timestamp": str
            }
        """
        logger.info("Début de la mise à jour complète de la configuration...")

        results = {
            "models_pricing": self.update_all_models_pricing(),
            "saas_pricing": self.update_all_saas_pricing(),
            "co2_factors": self.update_co2_factors(),
            "timestamp": datetime.now().isoformat(),
        }

        # Calculer les statistiques
        total_success = (
            len(results["models_pricing"]["success"])
            + len(results["saas_pricing"]["success"])
            + len(results["co2_factors"]["success"])
        )
        total_failed = (
            len(results["models_pricing"]["failed"])
            + len(results["saas_pricing"]["failed"])
            + len(results["co2_factors"]["failed"])
        )

        logger.info(
            f"Mise à jour terminée: {total_success} succès, {total_failed} échecs"
        )

        return results

    def get_update_status(self) -> Dict:
        """
        Retourne le statut de la dernière mise à jour.

        Returns:
            Dict: {
                "last_update": str,
                "models_updated": int,
                "saas_updated": int,
                "co2_updated": int
            }
        """
        last_update = self._get_last_update_time()

        return {
            "last_update": last_update.isoformat() if last_update else "Jamais",
            "models_count": len(self.current_config.get("models", {})),
            "saas_count": len(self.current_config.get("saas_subscriptions", {})),
            "next_update": (datetime.now() + timedelta(hours=24)).isoformat(),
        }


def update_config():
    """
    Fonction principale pour mettre à jour la configuration.

    Returns:
        Dict: Résultats de la mise à jour
    """
    updater = ConfigUpdater()
    return updater.update_all()


def get_update_status():
    """
    Retourne le statut de la dernière mise à jour.

    Returns:
        Dict: Statut de la mise à jour
    """
    updater = ConfigUpdater()
    return updater.get_update_status()


if __name__ == "__main__":
    # Exemple d'utilisation
    results = update_config()
    print("Résultats de la mise à jour:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
