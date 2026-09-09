"""
Report Generator Module for Sobre

Ce module contient les fonctions pour générer des rapports (CSRD, résumé)
au format PDF ou texte.

Fonctionnalités:
    - Génération de rapports CSRD (conformité réglementaire)
    - Génération de rapports de résumé
    - Export en PDF
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from fpdf import FPDF


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


class PDFReport(FPDF):
    """
    Classe personnalisée pour générer des rapports PDF avec FPDF.
    """
    
    def header(self):
        """En-tête du rapport."""
        # Logo (optionnel)
        # self.image('logo.png', 10, 8, 33)
        
        # Police pour le titre
        self.set_font('Arial', 'B', 16)
        
        # Titre
        self.cell(0, 10, 'Rapport Sobre - GreenOps + FinOps', 0, 1, 'C')
        
        # Sous-titre
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Analyse de vos coûts et empreinte carbone IA', 0, 1, 'C')
        
        # Ligne de séparation
        self.ln(5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)
    
    def footer(self):
        """Pied de page du rapport."""
        # Position à 1.5 cm du bas
        self.set_y(-15)
        
        # Police
        self.set_font('Arial', 'I', 8)
        
        # Numéro de page
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')
    
    def chapter_title(self, title: str):
        """Titre de chapitre."""
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
    
    def section_title(self, title: str):
        """Titre de section."""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def add_metadata(self, company_name: str, date_range: str, generated_date: str):
        """Ajoute les métadonnées du rapport."""
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'Entreprise: {company_name}', 0, 1)
        self.cell(0, 10, f'Période: {date_range}', 0, 1)
        self.cell(0, 10, f'Date de génération: {generated_date}', 0, 1)
        self.ln(5)


def generate_csrd_report(
    company_name: str,
    total_cost: float,
    total_carbon_g: float,
    greenops_result: Dict,
    saas_subscriptions: List[Dict],
    dormant_licenses: List[Dict],
    recommendations: List[str],
    output_path: str = "rapport_csrd.pdf"
) -> Dict:
    """
    Génère un rapport CSRD (Corporate Sustainability Reporting Directive) au format PDF.
    
    Args:
        company_name: Nom de l'entreprise.
        total_cost: Coût total mensuel en €.
        total_carbon_g: Empreinte carbone totale en g.
        greenops_result: Résultat du calcul GreenOps.
        saas_subscriptions: Liste des abonnements SaaS.
        dormant_licenses: Liste des licences dormantes.
        recommendations: Liste des recommandations.
        output_path: Chemin pour sauvegarder le PDF.
        
    Returns:
        Dict: {
            "success": bool,
            "message": str,
            "file_path": str
        }
    """
    try:
        # Créer le PDF
        pdf = PDFReport()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # Ajouter les métadonnées
        generated_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_range = f"{datetime.now().strftime('%B %Y')}"
        pdf.add_metadata(company_name, date_range, generated_date)
        
        # Titre principal
        pdf.chapter_title("Rapport CSRD - Impact Environnemental et Financier de l'IA")
        
        # Section 1: Résumé exécutif
        pdf.section_title("1. Résumé Exécutif")
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 7, f"""
        Ce rapport présente l'analyse complète de l'impact environnemental et financier 
        lié à l'utilisation de l'intelligence artificielle par {company_name}.
        
        Score GreenOps: {greenops_result['grade']} - {greenops_result['grade_name']} ({greenops_result['score']}/100)
        Coût total mensuel: {total_cost:.2f} €
        Empreinte carbone totale: {total_carbon_g:.1f} g CO₂ (équivalent {total_carbon_g/0.2:.1f} km en voiture)
        """)
        pdf.ln(5)
        
        # Section 2: Analyse des coûts
        pdf.section_title("2. Analyse des Coûts")
        pdf.set_font('Arial', '', 10)
        
        # Tableau des coûts par SaaS
        pdf.cell(0, 10, "Détail des coûts par abonnement SaaS:", 0, 1)
        pdf.ln(2)
        
        # En-têtes du tableau
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 10, "Nom du SaaS", 1, 0, 'L')
        pdf.cell(40, 10, "Coût mensuel", 1, 0, 'R')
        pdf.cell(40, 10, "Type", 1, 0, 'L')
        pdf.cell(50, 10, "Statut", 1, 1, 'L')
        
        # Lignes du tableau
        pdf.set_font('Arial', '', 10)
        for sub in saas_subscriptions:
            is_dormant = any(d['name'] == sub.get('name') for d in dormant_licenses)
            status = "Dormant" if is_dormant else "Actif"
            
            pdf.cell(60, 10, sub.get('name', 'Inconnu'), 1, 0, 'L')
            pdf.cell(40, 10, f"{sub.get('monthly_cost', 0):.2f} €", 1, 0, 'R')
            pdf.cell(40, 10, sub.get('saas_type', 'Inconnu'), 1, 0, 'L')
            pdf.cell(50, 10, status, 1, 1, 'L')
        
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, f"Coût total: {total_cost:.2f} €", 0, 1)
        pdf.ln(5)
        
        # Section 3: Analyse de l'empreinte carbone
        pdf.section_title("3. Analyse de l'Empreinte Carbone")
        pdf.set_font('Arial', '', 10)
        
        pdf.multi_cell(0, 7, f"""
        L'utilisation de l'IA par {company_name} génère une empreinte carbone totale de 
        {total_carbon_g:.1f} g CO₂ par mois, ce qui équivaut à environ {total_carbon_g/0.2:.1f} km 
        parcourus en voiture (sur la base d'une moyenne de 200g CO₂/km).
        
        Cette empreinte provient principalement de:
        - L'entraînement des modèles (scope 3)
        - La consommation énergétique des data centers
        - Les requêtes API et l'utilisation des SaaS
        
        Coût par employé: {greenops_result['cost_per_employee']:.2f} €
        CO₂ par employé: {greenops_result['carbon_per_employee']:.1f} g
        """)
        pdf.ln(5)
        
        # Section 4: Score GreenOps
        pdf.section_title("4. Score GreenOps")
        pdf.set_font('Arial', '', 10)
        
        pdf.multi_cell(0, 7, f"""
        Le score GreenOps de {company_name} est: {greenops_result['grade']} - {greenops_result['grade_name']}
        
        Ce score est calculé en fonction de:
        - Coût par employé: {greenops_result['cost_per_employee']:.2f} € (seuil max: {CONFIG['greenops_scores'][greenops_result['grade']]['max_cost_per_employee']} €)
        - CO₂ par employé: {greenops_result['carbon_per_employee']:.1f} g (seuil max: {CONFIG['greenops_scores'][greenops_result['grade']]['max_co2_per_employee']} g)
        - Taux de licences actives: {greenops_result['active_licenses_percentage']:.1f}%
        
        Interprétation:
        {get_grade_interpretation(greenops_result['grade'])}
        """)
        pdf.ln(5)
        
        # Section 5: Licences dormantes
        if dormant_licenses:
            pdf.section_title("5. Licences Dormantes")
            pdf.set_font('Arial', '', 10)
            
            pdf.multi_cell(0, 7, f"""
            {len(dormant_licenses)} licence(s) ont été identifiées comme dormantes (inutilisées depuis plus de 30 jours).
            
            Désactiver ces licences permettrait d'économiser:
            - Coût: {calculate_potential_savings(total_cost, total_carbon_g, dormant_licenses, saas_subscriptions)['cost_savings']:.2f} €/mois
            - CO₂: {calculate_potential_savings(total_cost, total_carbon_g, dormant_licenses, saas_subscriptions)['carbon_savings_g']:.1f} g/mois
            """)
            pdf.ln(5)
        
        # Section 6: Recommandations
        pdf.section_title("6. Recommandations")
        pdf.set_font('Arial', '', 10)
        
        for i, rec in enumerate(recommendations, 1):
            pdf.multi_cell(0, 7, f"{i}. {rec}")
            pdf.ln(2)
        
        # Sauvegarder le PDF
        pdf.output(output_path)
        
        return {
            "success": True,
            "message": f"Rapport CSRD généré avec succès: {output_path}",
            "file_path": output_path
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Erreur lors de la génération du rapport: {str(e)}",
            "file_path": None
        }


def generate_summary_report(
    company_name: str,
    total_cost: float,
    total_carbon_g: float,
    greenops_result: Dict,
    saas_count: int,
    dormant_count: int,
    output_path: str = "rapport_resume.pdf"
) -> Dict:
    """
    Génère un rapport de résumé au format PDF.
    
    Args:
        company_name: Nom de l'entreprise.
        total_cost: Coût total mensuel en €.
        total_carbon_g: Empreinte carbone totale en g.
        greenops_result: Résultat du calcul GreenOps.
        saas_count: Nombre total d'abonnements SaaS.
        dormant_count: Nombre de licences dormantes.
        output_path: Chemin pour sauvegarder le PDF.
        
    Returns:
        Dict: {
            "success": bool,
            "message": str,
            "file_path": str
        }
    """
    try:
        # Créer le PDF
        pdf = PDFReport()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # Ajouter les métadonnées
        generated_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pdf.add_metadata(company_name, datetime.now().strftime('%B %Y'), generated_date)
        
        # Titre
        pdf.chapter_title("Rapport de Résumé - Sobre")
        
        # Contenu principal
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Indicateurs Clés:", 0, 1)
        pdf.ln(5)
        
        # Tableau des indicateurs
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(80, 10, "Métrique", 1, 0, 'L')
        pdf.cell(60, 10, "Valeur", 1, 0, 'R')
        pdf.cell(50, 10, "Unité", 1, 1, 'L')
        
        pdf.set_font('Arial', '', 10)
        
        # Coût total
        pdf.cell(80, 10, "Coût total mensuel", 1, 0, 'L')
        pdf.cell(60, 10, f"{total_cost:.2f}", 1, 0, 'R')
        pdf.cell(50, 10, "€", 1, 1, 'L')
        
        # CO2 total
        pdf.cell(80, 10, "Empreinte carbone totale", 1, 0, 'L')
        pdf.cell(60, 10, f"{total_carbon_g:.1f}", 1, 0, 'R')
        pdf.cell(50, 10, "g CO₂", 1, 1, 'L')
        
        # Équivalent km voiture
        pdf.cell(80, 10, "Équivalent km voiture", 1, 0, 'L')
        pdf.cell(60, 10, f"{total_carbon_g/0.2:.1f}", 1, 0, 'R')
        pdf.cell(50, 10, "km", 1, 1, 'L')
        
        # Nombre de SaaS
        pdf.cell(80, 10, "Nombre d'abonnements SaaS", 1, 0, 'L')
        pdf.cell(60, 10, f"{saas_count}", 1, 0, 'R')
        pdf.cell(50, 10, "", 1, 1, 'L')
        
        # Licences dormantes
        pdf.cell(80, 10, "Licences dormantes", 1, 0, 'L')
        pdf.cell(60, 10, f"{dormant_count}", 1, 0, 'R')
        pdf.cell(50, 10, "", 1, 1, 'L')
        
        # Score GreenOps
        pdf.cell(80, 10, "Score GreenOps", 1, 0, 'L')
        pdf.cell(60, 10, f"{greenops_result['grade']} ({greenops_result['score']}/100)", 1, 0, 'R')
        pdf.cell(50, 10, "", 1, 1, 'L')
        
        pdf.ln(10)
        
        # Graphique simple (représentation textuelle)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, "Répartition des coûts:", 0, 1)
        pdf.ln(2)
        
        # Barre de progression pour le score GreenOps
        pdf.set_font('Arial', '', 10)
        pdf.cell(50, 10, "Score GreenOps:", 0, 0)
        
        # Dessiner une barre de progression
        bar_width = 100
        filled_width = (greenops_result['score'] / 100) * bar_width
        
        # Barre de fond
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(bar_width, 5, "", 0, 0, 'L', True)
        
        # Barre remplie
        pdf.set_fill_color(34, 134, 193)  # Bleu #2E86C1
        if greenops_result['grade'] == 'A':
            pdf.set_fill_color(40, 180, 99)  # Vert #28B463
        elif greenops_result['grade'] == 'B':
            pdf.set_fill_color(40, 180, 99)  # Vert
        elif greenops_result['grade'] == 'C':
            pdf.set_fill_color(255, 193, 7)  # Jaune
        elif greenops_result['grade'] == 'D':
            pdf.set_fill_color(255, 152, 0)  # Orange
        else:  # E
            pdf.set_fill_color(220, 53, 69)  # Rouge
        
        pdf.cell(filled_width, 5, "", 0, 0, 'L', True)
        pdf.cell(10, 5, f"{greenops_result['score']}%", 0, 1, 'L')
        
        pdf.ln(10)
        
        # Recommandations
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, "Recommandations:", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        # Générer des recommandations basiques
        basic_recommendations = []
        if dormant_count > 0:
            basic_recommendations.append(f"Désactivez les {dormant_count} licences dormantes pour économiser.")
        if greenops_result['grade'] in ['D', 'E']:
            basic_recommendations.append("Passez à des modèles plus économiques (ex: Mistral-7B).")
        if greenops_result['grade'] in ['A', 'B']:
            basic_recommendations.append("Continuez à surveiller vos coûts et votre empreinte carbone.")
        
        for rec in basic_recommendations:
            pdf.multi_cell(0, 7, f"• {rec}")
            pdf.ln(2)
        
        # Sauvegarder le PDF
        pdf.output(output_path)
        
        return {
            "success": True,
            "message": f"Rapport de résumé généré avec succès: {output_path}",
            "file_path": output_path
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Erreur lors de la génération du rapport: {str(e)}",
            "file_path": None
        }


def get_grade_interpretation(grade: str) -> str:
    """
    Retourne l'interprétation d'un grade GreenOps.
    
    Args:
        grade: Grade (A, B, C, D, E).
        
    Returns:
        str: Interprétation du grade.
    """
    interpretations = {
        "A": "Excellent: Votre entreprise est un modèle en termes d'optimisation des coûts et de réduction de l'empreinte carbone liée à l'IA.",
        "B": "Bon: Votre entreprise a une bonne gestion de ses ressources IA, avec des marges d'amélioration.",
        "C": "Moyen: Votre entreprise a une gestion acceptable, mais des améliorations significatives sont possibles.",
        "D": "À améliorer: Votre entreprise doit prendre des mesures pour optimiser ses coûts et réduire son empreinte carbone.",
        "E": "Critique: Votre entreprise a un impact environnemental et financier élevé lié à l'IA. Des actions urgentes sont nécessaires."
    }
    
    return interpretations.get(grade, "Interprétation non disponible")


def calculate_potential_savings(
    total_cost: float,
    total_carbon_g: float,
    dormant_licenses: List[Dict],
    saas_subscriptions: List[Dict]
) -> Dict:
    """
    Calcule les économies potentielles (utilisé dans le rapport).
    
    Args:
        total_cost: Coût total mensuel en €.
        total_carbon_g: Empreinte carbone totale en g.
        dormant_licenses: Liste des licences dormantes.
        saas_subscriptions: Liste de tous les abonnements SaaS.
        
    Returns:
        Dict: {
            "cost_savings": float,
            "carbon_savings_g": float
        }
    """
    from .greenops_scoring import calculate_potential_savings as _calculate_potential_savings
    return _calculate_potential_savings(total_cost, total_carbon_g, dormant_licenses, saas_subscriptions)
