"""
UI Components for Sobre

Ce module contient des composants réutilisables pour l'interface Streamlit,
notamment pour afficher les valeurs avec leur niveau de certitude (CERTAIN/ESTIMÉ).
"""

import streamlit as st
from typing import Optional, Dict, Any


class CertaintyLevel:
    """Niveaux de certitude pour les données affichées."""
    CERTAIN = "CERTAIN"
    ESTIMATED = "ESTIMÉ"


def display_metric_with_certainty(
    label: str,
    value: str,
    certainty: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    hypothesis: Optional[str] = None,
    help_text: Optional[str] = None,
) -> None:
    """
    Affiche une métrique avec son niveau de certitude, une fourchette (si ESTIMÉ),
    et un lien vers les hypothèses.

    Args:
        label: Libellé de la métrique (ex: "Coût total").
        value: Valeur à afficher (ex: "100 €").
        certainty: Niveau de certitude (CertaintyLevel.CERTAIN ou CertaintyLevel.ESTIMATED).
        min_value: Valeur minimale de la fourchette (pour ESTIMÉ).
        max_value: Valeur maximale de la fourchette (pour ESTIMÉ).
        hypothesis: Texte décrivant les hypothèses (ex: "Basé sur GPT-4").
        help_text: Texte d'aide supplémentaire.
    """
    # Déterminer la couleur et l'icône en fonction de la certitude
    if certainty == CertaintyLevel.CERTAIN:
        icon = "✅"
        color = "green"
        certainty_text = "Certaine"
    else:
        icon = "⚠️"
        color = "orange"
        certainty_text = "Estimée"

    # Créer le texte de la fourchette si disponible
    range_text = ""
    if certainty == CertaintyLevel.ESTIMATED and min_value is not None and max_value is not None:
        range_text = f" (fourchette: {min_value} - {max_value})"

    # Créer le texte d'hypothèse si disponible
    hypothesis_text = ""
    if hypothesis:
        hypothesis_text = f"\n\n*Hypothèses : {hypothesis}*"

    # Afficher la métrique avec Streamlit
    delta = None
    if certainty == CertaintyLevel.ESTIMATED:
        delta = "Estimé"

    # Utiliser st.metric pour afficher la valeur
    st.metric(
        label=f"{icon} {label} ({certainty_text}){range_text}",
        value=value,
        delta=delta,
        help=f"{help_text}{hypothesis_text}" if help_text or hypothesis else None,
    )


def display_value_with_certainty(
    label: str,
    value: str,
    certainty: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    hypothesis: Optional[str] = None,
    source: Optional[str] = None,
) -> None:
    """
    Affiche une valeur avec son niveau de certitude, une fourchette (si ESTIMÉ),
    et un lien vers les hypothèses/sources.

    Args:
        label: Libellé de la valeur (ex: "Coût total").
        value: Valeur à afficher (ex: "100 €").
        certainty: Niveau de certitude (CertaintyLevel.CERTAIN ou CertaintyLevel.ESTIMATED).
        min_value: Valeur minimale de la fourchette (pour ESTIMÉ).
        max_value: Valeur maximale de la fourchette (pour ESTIMÉ).
        hypothesis: Texte décrivant les hypothèses.
        source: Source des données (ex: "OpenAI Pricing").
    """
    # Déterminer la couleur et l'icône
    if certainty == CertaintyLevel.CERTAIN:
        icon = "✅"
        color = "#2E86C1"
        certainty_text = "Certaine"
        certainty_color = "green"
    else:
        icon = "⚠️"
        color = "#F39C12"
        certainty_text = "Estimée"
        certainty_color = "orange"

    # Créer le texte de la fourchette
    range_text = ""
    if certainty == CertaintyLevel.ESTIMATED and min_value is not None and max_value is not None:
        range_text = f" | Fourchette: **{min_value} - {max_value}**"

    # Créer le texte source/hypothèse
    details_text = ""
    if hypothesis or source:
        details = []
        if hypothesis:
            details.append(f"Hypothèses: {hypothesis}")
        if source:
            details.append(f"Source: {source}")
        details_text = f" (*{', '.join(details)}*)"

    # Afficher avec HTML pour plus de contrôle
    html = f"""
    <div style="border-left: 4px solid {color}; padding-left: 10px; margin: 10px 0;">
        <strong>{icon} {label}</strong>: {value} <span style="color: {certainty_color}; font-style: italic;">({certainty_text})</span>{range_text}{details_text}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_certainty_badge(certainty: str) -> str:
    """
    Retourne un badge HTML pour afficher le niveau de certitude.

    Args:
        certainty: Niveau de certitude (CertaintyLevel.CERTAIN ou CertaintyLevel.ESTIMATED).

    Returns:
        str: Code HTML du badge.
    """
    if certainty == CertaintyLevel.CERTAIN:
        return '<span style="background-color: #2E86C1; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em;">CERTAIN</span>'
    else:
        return '<span style="background-color: #F39C12; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.8em;">ESTIMÉ</span>'


def create_hypothesis_tooltip(
    hypothesis: str,
    source: Optional[str] = None,
    date: Optional[str] = None,
    confidence_level: Optional[str] = None,
) -> str:
    """
    Crée un tooltip (infobulle) avec les détails des hypothèses et sources.

    Args:
        hypothesis: Description des hypothèses.
        source: Source des données.
        date: Date de la source.
        confidence_level: Niveau de confiance (ex: "publie_par_fournisseur").

    Returns:
        str: Texte formaté pour le tooltip.
    """
    parts = []
    if hypothesis:
        parts.append(f"Hypothèses: {hypothesis}")
    if source:
        parts.append(f"Source: {source}")
    if date:
        parts.append(f"Date: {date}")
    if confidence_level:
        parts.append(f"Niveau de confiance: {confidence_level}")
    return "\n".join(parts)


def format_estimated_value(
    value: float,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    unit: str = "",
    decimals: int = 2,
) -> str:
    """
    Formate une valeur estimée avec sa fourchette.

    Args:
        value: Valeur centrale.
        min_value: Valeur minimale de la fourchette.
        max_value: Valeur maximale de la fourchette.
        unit: Unité (ex: "€", "g CO₂").
        decimals: Nombre de décimales.

    Returns:
        str: Valeur formatée avec fourchette.
    """
    formatted_value = f"{value:.{decimals}f} {unit}"
    if min_value is not None and max_value is not None:
        formatted_value += f" (min: {min_value:.{decimals}f} {unit}, max: {max_value:.{decimals}f} {unit})"
    return formatted_value


def get_certainty_level_from_source(source: Optional[str]) -> str:
    """
    Détermine le niveau de certitude en fonction de la source.

    Args:
        source: Source des données (ex: "mesure", "publie_par_fournisseur").

    Returns:
        str: Niveau de certitude (CertaintyLevel.CERTAIN ou CertaintyLevel.ESTIMATED).
    """
    if not source:
        return CertaintyLevel.ESTIMATED
    
    certain_sources = ["mesure"]
    if source in certain_sources:
        return CertaintyLevel.CERTAIN
    else:
        return CertaintyLevel.ESTIMATED
