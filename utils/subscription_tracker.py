"""
Subscription Tracker Module for Sobre

Ce module contient les fonctions pour détecter et suivre les abonnements IA
dans les factures importées (CSV, PDF).

Fonctionnalités:
    - Détection des abonnements IA via mots-clés
    - Identification des licences dormantes
    - Import et traitement des fichiers CSV/PDF
"""

import yaml
import pandas as pd
import re
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta


def load_config() -> Dict:
    """
    Charge la configuration depuis le fichier YAML.
    
    Returns:
        Dict: Configuration complète.
    """
    config_path = Path(__file__).parent.parent / "config" / "models.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


CONFIG = load_config()
AI_KEYWORDS = CONFIG["ai_keywords"]
SAAS_SUBSCRIPTIONS = CONFIG["saas_subscriptions"]


def detect_ai_subscriptions(
    data: Union[pd.DataFrame, List[Dict]],
    name_column: str = "Nom",
    description_column: Optional[str] = None
) -> List[Dict]:
    """
    Détecte les abonnements IA dans un DataFrame ou une liste de dictionnaires.
    
    Args:
        data: DataFrame Pandas ou liste de dictionnaires contenant les factures.
        name_column: Nom de la colonne contenant le nom du SaaS.
        description_column: Nom de la colonne contenant la description (optionnel).
        
    Returns:
        List[Dict]: Liste des abonnements IA détectés avec leurs détails.
        
    Raises:
        ValueError: Si name_column n'existe pas dans les données.
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data.copy()
    
    # Vérifier que la colonne existe
    if name_column not in df.columns:
        raise ValueError(f"La colonne '{name_column}' n'existe pas dans les données")
    
    # Normaliser les noms de colonnes
    name_col = name_column
    desc_col = description_column if description_column and description_column in df.columns else None
    
    detected_subscriptions = []
    
    for _, row in df.iterrows():
        name = str(row[name_col]).lower() if pd.notna(row[name_col]) else ""
        description = str(row[desc_col]).lower() if desc_col and pd.notna(row[desc_col]) else ""
        
        # Combiner nom et description pour la recherche
        search_text = f"{name} {description}"
        
        # Vérifier si un mot-clé IA est présent
        is_ai = any(keyword.lower() in search_text for keyword in AI_KEYWORDS)
        
        if is_ai:
            # Trouver le SaaS correspondant dans la configuration
            matched_saas = None
            for saas_name, saas_data in SAAS_SUBSCRIPTIONS.items():
                # Vérifier si le nom du SaaS est dans le texte de recherche
                # ou si le nom détecté correspond au SaaS (en ignorant les tirets et espaces)
                saas_name_clean = saas_name.lower().replace("-", "").replace(" ", "")
                name_clean = name.replace("-", "").replace(" ", "")
                if saas_name.lower() in search_text or saas_name_clean in name_clean:
                    matched_saas = saas_name
                    break
            
            detected_subscriptions.append({
                "name": row[name_col],
                "description": row[desc_col] if desc_col else None,
                "matched_saas": matched_saas,
                "is_ai": True,
                "confidence": "high" if matched_saas else "medium"
            })
    
    return detected_subscriptions


def identify_dormant_licenses(
    subscriptions: List[Dict],
    usage_data: Optional[List[Dict]] = None,
    threshold_days: int = 30
) -> List[Dict]:
    """
    Identifie les licences dormantes (non utilisées) parmi les abonnements.
    
    Args:
        subscriptions: Liste des abonnements (résultat de detect_ai_subscriptions).
        usage_data: Liste de données d'utilisation (optionnel).
        threshold_days: Nombre de jours sans utilisation pour être considéré comme dormant.
        
    Returns:
        List[Dict]: Liste des licences dormantes avec détails.
    """
    dormant_licenses = []
    
    # Si pas de données d'utilisation, on ne peut pas détecter les licences dormantes
    if usage_data is None:
        return dormant_licenses
    
    # Convertir usage_data en DataFrame pour traitement
    usage_df = pd.DataFrame(usage_data)
    
    # Vérifier si la colonne 'last_used' existe
    if 'last_used' not in usage_df.columns:
        return dormant_licenses
    
    # Calculer la date seuil (aujourd'hui - threshold_days)
    threshold_date = datetime.now() - timedelta(days=threshold_days)
    
    for sub in subscriptions:
        # Vérifier si cet abonnement a une utilisation récente
        sub_usage = usage_df[usage_df['name'] == sub['name']]
        
        if sub_usage.empty:
            # Pas de données d'utilisation pour cet abonnement
            dormant_licenses.append({
                **sub,
                "status": "dormant",
                "reason": "no_usage_data",
                "days_inactive": None
            })
            continue
        
        # Trouver la date de dernière utilisation
        last_used = pd.to_datetime(sub_usage['last_used']).max()
        
        if pd.isna(last_used):
            dormant_licenses.append({
                **sub,
                "status": "dormant",
                "reason": "no_last_used_date",
                "days_inactive": None
            })
            continue
        
        # Calculer le nombre de jours d'inactivité
        days_inactive = (datetime.now() - last_used).days
        
        if days_inactive > threshold_days:
            dormant_licenses.append({
                **sub,
                "status": "dormant",
                "reason": "inactive",
                "days_inactive": days_inactive,
                "last_used": last_used.strftime('%Y-%m-%d')
            })
    
    return dormant_licenses


def process_uploaded_file(
    file_path: str,
    file_type: str = "csv",
    name_column: str = "Nom",
    cost_column: Optional[str] = None,
    date_column: Optional[str] = None
) -> Dict:
    """
    Traite un fichier uploadé (CSV ou PDF) et extrait les abonnements.
    
    Args:
        file_path: Chemin vers le fichier uploadé.
        file_type: Type de fichier ('csv' ou 'pdf').
        name_column: Nom de la colonne contenant le nom du SaaS.
        cost_column: Nom de la colonne contenant le coût (optionnel).
        date_column: Nom de la colonne contenant la date (optionnel).
        
    Returns:
        Dict: {
            "success": bool,
            "data": DataFrame ou None,
            "ai_subscriptions": List[Dict],
            "error": str ou None
        }
        
    Raises:
        ValueError: Si file_type n'est pas 'csv' ou 'pdf'.
        FileNotFoundError: Si le fichier n'existe pas.
    """
    if file_type not in ["csv", "pdf"]:
        raise ValueError("file_type doit être 'csv' ou 'pdf'")
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    
    try:
        if file_type == "csv":
            # Lire le fichier CSV
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
            
            # Vérifier les colonnes requises
            required_columns = [name_column]
            if cost_column:
                required_columns.append(cost_column)
            if date_column:
                required_columns.append(date_column)
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return {
                    "success": False,
                    "data": None,
                    "ai_subscriptions": [],
                    "error": f"Colonnes manquantes: {', '.join(missing_columns)}"
                }
            
            # Détecter les abonnements IA
            ai_subscriptions = detect_ai_subscriptions(df, name_column, date_column)
            
            return {
                "success": True,
                "data": df,
                "ai_subscriptions": ai_subscriptions,
                "error": None
            }
        
        elif file_type == "pdf":
            # Pour les PDF, on utilise une approche simplifiée (extraction de texte)
            # Note: En production, utiliser une librairie comme PyPDF2 ou pdfplumber
            try:
                import pdfplumber
            except ImportError:
                return {
                    "success": False,
                    "data": None,
                    "ai_subscriptions": [],
                    "error": "La librairie pdfplumber est requise pour lire les PDF. Installez-la avec: pip install pdfplumber"
                }
            
            # Extraire le texte du PDF
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            
            # Créer un DataFrame à partir du texte extrait
            # Cette partie est simplifiée - en production, utiliser une analyse plus sophistiquée
            lines = text.split('\n')
            data = []
            for line in lines:
                if line.strip():
                    data.append({"text": line.strip()})
            
            df = pd.DataFrame(data)
            
            # Détecter les abonnements IA (en utilisant la colonne 'text')
            ai_subscriptions = detect_ai_subscriptions(df, "text")
            
            return {
                "success": True,
                "data": df,
                "ai_subscriptions": ai_subscriptions,
                "error": None
            }
    
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "ai_subscriptions": [],
            "error": f"Erreur lors du traitement du fichier: {str(e)}"
        }


def validate_uploaded_file(
    file_path: str,
    file_type: str = "csv",
    required_columns: Optional[List[str]] = None
) -> Dict:
    """
    Valide un fichier uploadé avant traitement.
    
    Args:
        file_path: Chemin vers le fichier.
        file_type: Type de fichier ('csv' ou 'pdf').
        required_columns: Liste des colonnes requises (pour CSV).
        
    Returns:
        Dict: {
            "valid": bool,
            "message": str,
            "missing_columns": List[str] ou None
        }
    """
    if file_type not in ["csv", "pdf"]:
        return {
            "valid": False,
            "message": "Type de fichier non supporté. Utilisez CSV ou PDF.",
            "missing_columns": None
        }
    
    if not Path(file_path).exists():
        return {
            "valid": False,
            "message": "Fichier introuvable.",
            "missing_columns": None
        }
    
    if file_type == "csv" and required_columns:
        try:
            df = pd.read_csv(file_path, encoding='utf-8', nrows=5)  # Lire seulement 5 lignes pour validation
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return {
                    "valid": False,
                    "message": f"Colonnes manquantes: {', '.join(missing_columns)}",
                    "missing_columns": missing_columns
                }
            
            return {
                "valid": True,
                "message": "Fichier valide.",
                "missing_columns": None
            }
        except Exception as e:
            return {
                "valid": False,
                "message": f"Erreur de lecture du fichier: {str(e)}",
                "missing_columns": None
            }
    
    return {
        "valid": True,
        "message": "Fichier valide.",
        "missing_columns": None
    }
