"""
Tests unitaires pour le module subscription_tracker.

Exécutez avec: pytest tests/test_subscription_tracker.py -v
"""

import pytest
import pandas as pd
import tempfile
import os
from utils.subscription_tracker import (
    detect_ai_subscriptions,
    identify_dormant_licenses,
    validate_uploaded_file,
    process_uploaded_file,
    AI_KEYWORDS
)


class TestDetectAiSubscriptions:
    """Tests pour detect_ai_subscriptions."""
    
    def test_detect_chatgpt(self):
        """Test de détection de ChatGPT."""
        data = pd.DataFrame({
            "Nom": ["ChatGPT Plus", "Zoom", "Slack"],
            "Coût": [20, 15, 10]
        })
        
        result = detect_ai_subscriptions(data, name_column="Nom")
        
        assert len(result) == 1
        assert result[0]["name"] == "ChatGPT Plus"
        assert result[0]["is_ai"] is True
        assert result[0]["matched_saas"] == "ChatGPT-Plus"
    
    def test_detect_multiple_ai(self):
        """Test de détection de plusieurs SaaS IA."""
        data = pd.DataFrame({
            "Nom": ["ChatGPT Plus", "GitHub Copilot", "Notion AI", "Zoom"],
            "Coût": [20, 10, 10, 15]
        })
        
        result = detect_ai_subscriptions(data, name_column="Nom")
        
        assert len(result) == 3
        names = [sub["name"] for sub in result]
        assert "ChatGPT Plus" in names
        assert "GitHub Copilot" in names
        assert "Notion AI" in names
    
    def test_detect_with_description(self):
        """Test de détection avec la colonne description."""
        data = pd.DataFrame({
            "Nom": ["Abonnement 1", "Abonnement 2"],
            "Description": ["Accès à ChatGPT Plus", "Service de visioconférence"]
        })
        
        result = detect_ai_subscriptions(data, name_column="Nom", description_column="Description")
        
        assert len(result) == 1
        assert result[0]["name"] == "Abonnement 1"
    
    def test_no_ai_subscriptions(self):
        """Test avec aucun abonnement IA."""
        data = pd.DataFrame({
            "Nom": ["Zoom", "Slack", "Google Workspace"],
            "Coût": [15, 10, 5]
        })
        
        result = detect_ai_subscriptions(data, name_column="Nom")
        
        assert len(result) == 0
    
    def test_list_input(self):
        """Test avec une liste de dictionnaires en entrée."""
        data = [
            {"Nom": "ChatGPT Plus", "Coût": 20},
            {"Nom": "Zoom", "Coût": 15}
        ]
        
        result = detect_ai_subscriptions(data, name_column="Nom")
        
        assert len(result) == 1
        assert result[0]["name"] == "ChatGPT Plus"
    
    def test_missing_name_column(self):
        """Test avec une colonne 'Nom' manquante (doit lever ValueError)."""
        data = pd.DataFrame({
            "Service": ["ChatGPT Plus", "Zoom"],
            "Coût": [20, 15]
        })
        
        with pytest.raises(ValueError):
            detect_ai_subscriptions(data, name_column="Nom")
    
    def test_case_insensitive(self):
        """Test de détection insensible à la casse."""
        data = pd.DataFrame({
            "Nom": ["CHATGPT PLUS", "chatgpt", "GPT-4"],
            "Coût": [20, 15, 10]
        })
        
        result = detect_ai_subscriptions(data, name_column="Nom")
        
        assert len(result) == 3


class TestIdentifyDormantLicenses:
    """Tests pour identify_dormant_licenses."""
    
    def test_no_usage_data(self):
        """Test sans données d'utilisation (doit retourner liste vide)."""
        subscriptions = [
            {"name": "ChatGPT Plus"},
            {"name": "Copilot"}
        ]
        
        result = identify_dormant_licenses(subscriptions, usage_data=None)
        
        assert len(result) == 0
    
    def test_no_last_used_column(self):
        """Test sans colonne 'last_used' (doit retourner liste vide)."""
        subscriptions = [{"name": "ChatGPT Plus"}]
        usage_data = [{"name": "ChatGPT Plus", "other_column": "value"}]
        
        result = identify_dormant_licenses(subscriptions, usage_data=usage_data)
        
        assert len(result) == 0
    
    def test_active_license(self):
        """Test avec une licence active (utilisée récemment)."""
        from datetime import datetime, timedelta
        
        subscriptions = [{"name": "ChatGPT Plus"}]
        usage_data = [{"name": "ChatGPT Plus", "last_used": datetime.now().strftime('%Y-%m-%d')}]
        
        result = identify_dormant_licenses(subscriptions, usage_data=usage_data, threshold_days=30)
        
        assert len(result) == 0
    
    def test_dormant_license(self):
        """Test avec une licence dormante."""
        from datetime import datetime, timedelta
        
        subscriptions = [{"name": "ChatGPT Plus"}]
        old_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
        usage_data = [{"name": "ChatGPT Plus", "last_used": old_date}]
        
        result = identify_dormant_licenses(subscriptions, usage_data=usage_data, threshold_days=30)
        
        assert len(result) == 1
        assert result[0]["status"] == "dormant"
        assert result[0]["reason"] == "inactive"
        assert result[0]["days_inactive"] > 30


class TestValidateUploadedFile:
    """Tests pour validate_uploaded_file."""
    
    def test_valid_csv(self):
        """Test avec un CSV valide."""
        # Créer un fichier CSV temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Nom,Coût\nChatGPT Plus,20\nCopilot,10\n")
            temp_path = f.name
        
        try:
            result = validate_uploaded_file(temp_path, file_type="csv", required_columns=["Nom", "Coût"])
            assert result["valid"] is True
            assert "missing_columns" not in result or result["missing_columns"] is None
        finally:
            os.unlink(temp_path)
    
    def test_missing_columns(self):
        """Test avec des colonnes manquantes."""
        # Créer un fichier CSV sans la colonne 'Coût'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Nom\nChatGPT Plus\nCopilot\n")
            temp_path = f.name
        
        try:
            result = validate_uploaded_file(temp_path, file_type="csv", required_columns=["Nom", "Coût"])
            assert result["valid"] is False
            assert "Coût" in result["missing_columns"]
        finally:
            os.unlink(temp_path)
    
    def test_invalid_file_type(self):
        """Test avec un type de fichier invalide."""
        result = validate_uploaded_file("dummy.txt", file_type="txt")
        assert result["valid"] is False
        assert "non supporté" in result["message"]
    
    def test_nonexistent_file(self):
        """Test avec un fichier inexistant."""
        result = validate_uploaded_file("nonexistent.csv", file_type="csv")
        assert result["valid"] is False
        assert "introuvable" in result["message"]


class TestProcessUploadedFile:
    """Tests pour process_uploaded_file."""
    
    def test_process_csv(self):
        """Test de traitement d'un fichier CSV."""
        # Créer un fichier CSV temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Nom,Coût\nChatGPT Plus,20\nGitHub Copilot,10\nZoom,15\n")
            temp_path = f.name
        
        try:
            result = process_uploaded_file(
                temp_path,
                file_type="csv",
                name_column="Nom",
                cost_column="Coût"
            )
            
            assert result["success"] is True
            assert len(result["ai_subscriptions"]) == 2  # ChatGPT Plus et GitHub Copilot
            assert result["data"] is not None
        finally:
            os.unlink(temp_path)
    
    def test_process_csv_missing_columns(self):
        """Test de traitement d'un CSV avec des colonnes manquantes."""
        # Créer un fichier CSV sans la colonne 'Coût'
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Nom\nChatGPT Plus\nCopilot\n")
            temp_path = f.name
        
        try:
            result = process_uploaded_file(
                temp_path,
                file_type="csv",
                name_column="Nom",
                cost_column="Coût"
            )
            
            assert result["success"] is False
            assert "Colonnes manquantes" in result["error"]
        finally:
            os.unlink(temp_path)
    
    def test_process_nonexistent_file(self):
        """Test de traitement d'un fichier inexistant."""
        with pytest.raises(FileNotFoundError):
            process_uploaded_file("nonexistent.csv", file_type="csv")
    
    def test_process_invalid_file_type(self):
        """Test de traitement avec un type de fichier invalide."""
        with pytest.raises(ValueError):
            process_uploaded_file("dummy.txt", file_type="txt")
