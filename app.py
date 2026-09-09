"""
Sobre - GreenOps + FinOps pour les PME

Application Streamlit pour aider les PME à réduire leurs coûts cachés liés à l'IA
(abonnements SaaS comme Copilot, Notion AI, ChatGPT Plus, ou APIs comme GPT-4, Mistral-7B)
et à mesurer leur empreinte carbone.

Fonctionnalités:
- Tracker de "Shadow AI" : Centraliser les abonnements SaaS
- Import de factures (CSV) pour identifier les coûts cachés
- Score GreenOps : Évaluer la performance des PME (de A à E)
- Calcul des licences dormantes
- Génération de rapports CSRD
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import tempfile
import os
from datetime import datetime
from typing import Dict, List, Optional

# Import des modules personnalisés
from utils.cost_calculator import (
    calculate_api_cost,
    calculate_saas_cost,
    calculate_total_cost,
    get_saas_monthly_cost
)
from utils.carbon_calculator import (
    calculate_api_carbon,
    calculate_saas_carbon,
    calculate_total_carbon
)
from utils.subscription_tracker import (
    detect_ai_subscriptions,
    identify_dormant_licenses,
    validate_uploaded_file,
    process_uploaded_file
)
from utils.greenops_scoring import (
    calculate_greenops_score,
    generate_greenops_recommendations,
    calculate_potential_savings
)
from utils.report_generator import (
    generate_csrd_report,
    generate_summary_report
)

# Configuration de la page
st.set_page_config(
    page_title="Sobre - GreenOps + FinOps pour les PME",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thème personnalisé
st.markdown("""
<style>
    .reportview-container .main .block-container {
        background-color: #f8f9fa;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #2E86C1;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #28B463;
    }
    .stSelectbox, .stNumberInput, .stTextInput {
        border-radius: 5px;
    }
    h1 {
        color: #2E86C1;
    }
    h2, h3 {
        color: #28B463;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Initialiser l'historique et les données dans la session
if "history" not in st.session_state:
    st.session_state.history = []
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None
if "detected_subscriptions" not in st.session_state:
    st.session_state.detected_subscriptions = []
if "greenops_results" not in st.session_state:
    st.session_state.greenops_results = None

# Tooltips pour expliquer les termes techniques
TOOLTIPS = {
    "token": "Un token est une unité de texte (mot ou partie de mot) utilisée par les modèles IA. "
             "En moyenne, 1 token ≈ 0.75 mot.",
    "co2": "Le CO₂ (dioxyde de carbone) est un gaz à effet de serre. "
           "L'IA consomme de l'énergie, ce qui génère des émissions de CO₂.",
    "greenops": "GreenOps est une approche pour optimiser les coûts et réduire l'impact environnemental "
               "des infrastructures IT et de l'IA.",
    "shadow_ai": "Le 'Shadow AI' désigne l'utilisation non contrôlée d'outils IA dans une entreprise, "
                "souvent sans que la direction en ait connaissance.",
    "dormant_license": "Une licence dormante est un abonnement SaaS payé mais non utilisé depuis plus de 30 jours."
}

# Titre et description
st.title("🌱 Sobre - GreenOps + FinOps pour les PME")
st.markdown("""
**Sobre** aide les **PME** à **comprendre, suivre et optimiser** leurs coûts liés à l'IA 
(abonnements SaaS, APIs) et à **mesurer leur empreinte carbone**.

💡 **Pourquoi c'est important pour votre PME ?**
- **Réduisez vos coûts cachés** : Identifiez les abonnements SaaS inutilisés (ex: Copilot, Notion AI).
- **Optimisez vos dépenses IA** : Comparez les modèles (GPT-4 vs Mistral-7B) pour économiser jusqu'à 90%.
- **Mesurez votre impact environnemental** : L'IA représente une part croissante de l'empreinte carbone des entreprises.
- **Conformité réglementaire** : Générez des rapports CSRD pour vos obligations légales.

📌 **Nouveauté** : Importez vos **factures QuickBooks/Pennylane** pour une analyse automatique !
""")

# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Sélection du mode
    mode = st.radio(
        "🔧 Mode",
        [
            "Tracker Shadow AI (Recommandé)",
            "Calculateur API",
            "Comparaison Modèles",
            "Générateur de Rapports"
        ],
        index=0,
        help="Choisissez le mode qui correspond à votre besoin"
    )
    
    st.markdown("---")
    
    # Informations sur l'entreprise (pour le score GreenOps)
    st.header("🏢 Informations Entreprise")
    number_of_employees = st.number_input(
        "Nombre d'employés",
        min_value=1,
        value=10,
        help="Nombre total d'employés dans votre PME (pour calculer le score GreenOps)"
    )
    
    st.markdown("---")
    
    # Afficher l'historique
    st.header("📜 Historique")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history[-5:][::-1]):  # Derniers 5
            st.markdown(f"""
            **{item.get('type', 'Calcul')}** - {item.get('date', '')}
            - Coût: **{item.get('cost', 0):.2f} €**
            - CO₂: **{item.get('carbon', 0):.1f} g**
            - Score: **{item.get('score', 'N/A')}**
            ---
            """)
    else:
        st.info("Aucun calcul dans l'historique.")
    
    # Bouton pour vider l'historique
    if st.button("🗑️ Vider l'historique"):
        st.session_state.history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    **📚 Ressources**
    - [Documentation](https://github.com/sobre-aziz/sobre)
    - [Tarifs OpenAI](https://openai.com/pricing)
    - [Tarifs Mistral AI](https://mistral.ai/pricing/)
    
    **📞 Contact**
    Projet développé par [Aziz](https://github.com/sobre-aziz)
    """)

# ============================================================================
# MODE 1: TRACKER SHADOW AI (Mode principal pour les PME)
# ============================================================================
if mode == "Tracker Shadow AI (Recommandé)":
    st.header("🕵️‍♂️ Tracker Shadow AI")
    st.markdown("""
    **Importez vos factures** (CSV) pour identifier automatiquement vos abonnements IA 
    et détecter les licences dormantes.
    
    📌 **Formats supportés** : CSV (QuickBooks, Pennylane, export manuel)
    📌 **Colonnes requises** : `Nom` (ou `Service`), `Coût` (ou `Montant`), `Date` (optionnel)
    """)
    
    # Upload de fichier
    uploaded_file = st.file_uploader(
        "📁 Importez votre fichier de factures",
        type=["csv"],
        help="Sélectionnez un fichier CSV contenant vos abonnements SaaS"
    )
    
    if uploaded_file is not None:
        try:
            # Lire le fichier CSV
            df = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='skip')
            
            # Afficher un aperçu
            st.subheader("📋 Aperçu du fichier importé")
            st.dataframe(df.head(), use_container_width=True)
            
            # Détecter les colonnes
            name_columns = [col for col in df.columns if col.lower() in ['nom', 'name', 'service', 'saas', 'abonnements']]
            cost_columns = [col for col in df.columns if col.lower() in ['coût', 'cost', 'montant', 'amount', 'prix', 'price']]
            date_columns = [col for col in df.columns if col.lower() in ['date', 'date_facture', 'invoice_date']]
            
            # Sélectionner les colonnes (si plusieurs options)
            if len(name_columns) > 1:
                selected_name_col = st.selectbox("Colonne du nom du SaaS", name_columns)
            else:
                selected_name_col = name_columns[0] if name_columns else None
            
            if len(cost_columns) > 1:
                selected_cost_col = st.selectbox("Colonne du coût", cost_columns)
            else:
                selected_cost_col = cost_columns[0] if cost_columns else None
            
            if len(date_columns) > 1:
                selected_date_col = st.selectbox("Colonne de la date (optionnel)", date_columns)
            else:
                selected_date_col = date_columns[0] if date_columns else None
            
            # Valider les colonnes
            if not selected_name_col or not selected_cost_col:
                st.error("❌ **Erreur** : Les colonnes 'Nom' et 'Coût' sont requises. Vérifiez votre fichier.")
            else:
                # Détecter les abonnements IA
                with st.spinner("🔍 Détection des abonnements IA en cours..."):
                    detected_subs = detect_ai_subscriptions(
                        df,
                        name_column=selected_name_col,
                        description_column=selected_date_col
                    )
                    
                    st.session_state.detected_subscriptions = detected_subs
                    st.session_state.uploaded_data = df
                
                if detected_subs:
                    st.success(f"✅ **{len(detected_subs)} abonnement(s) IA détecté(s)**")
                    
                    # Afficher les abonnements détectés
                    st.subheader("🎯 Abonnements IA Détectés")
                    
                    detected_df = pd.DataFrame(detected_subs)
                    if not detected_df.empty:
                        st.dataframe(detected_df, use_container_width=True)
                    
                    # Extraire les coûts et CO2 pour chaque abonnement
                    st.subheader("📊 Analyse des Coûts et CO₂")
                    
                    saas_results = []
                    for sub in detected_subs:
                        saas_name = sub.get('matched_saas', sub.get('name'))
                        
                        # Calculer le coût (si disponible dans le fichier)
                        cost_value = 0
                        if selected_cost_col in df.columns:
                            try:
                                cost_value = float(df.loc[df[selected_name_col] == sub['name'], selected_cost_col].iloc[0])
                            except:
                                cost_value = 0
                        
                        # Si pas de coût dans le fichier, utiliser la valeur par défaut
                        if cost_value == 0:
                            monthly_cost = get_saas_monthly_cost(saas_name)
                            if monthly_cost:
                                cost_value = monthly_cost
                        
                        # Calculer le CO2 (valeur par défaut du SaaS)
                        from utils.carbon_calculator import get_saas_monthly_carbon
                        carbon_value = get_saas_monthly_carbon(saas_name) or 0
                        
                        saas_results.append({
                            "name": sub['name'],
                            "matched_saas": saas_name,
                            "monthly_cost": cost_value,
                            "monthly_carbon_kg": carbon_value,
                            "monthly_carbon_g": carbon_value * 1000,
                            "confidence": sub.get('confidence', 'medium')
                        })
                    
                    saas_df = pd.DataFrame(saas_results)
                    
                    # Calculer les totaux
                    total_cost = saas_df['monthly_cost'].sum()
                    total_carbon_g = saas_df['monthly_carbon_g'].sum()
                    
                    # Afficher les métriques
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            "💰 Coût total mensuel",
                            f"{total_cost:.2f} €",
                            help="Somme des coûts de tous les abonnements IA détectés"
                        )
                    with col2:
                        st.metric(
                            "🌍 CO₂ total mensuel",
                            f"{total_carbon_g:.1f} g",
                            help=f"Équivalent à {total_carbon_g/0.2:.1f} km en voiture"
                        )
                    with col3:
                        st.metric(
                            "📦 Nombre d'abonnements",
                            len(saas_results),
                            help="Nombre total d'abonnements IA détectés"
                        )
                    
                    # Graphique de répartition
                    st.subheader("📈 Répartition des Coûts et CO₂")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if not saas_df.empty:
                            fig_cost = px.pie(
                                saas_df,
                                values='monthly_cost',
                                names='name',
                                title="Répartition des coûts par SaaS",
                                hole=0.3
                            )
                            st.plotly_chart(fig_cost, use_container_width=True)
                    
                    with col2:
                        if not saas_df.empty:
                            fig_carbon = px.pie(
                                saas_df,
                                values='monthly_carbon_g',
                                names='name',
                                title="Répartition du CO₂ par SaaS",
                                hole=0.3
                            )
                            st.plotly_chart(fig_carbon, use_container_width=True)
                    
                    # Détecter les licences dormantes (simplifié : toutes les licences sont considérées comme actives pour l'instant)
                    # En production, il faudrait des données d'utilisation
                    dormant_licenses = identify_dormant_licenses(
                        detected_subs,
                        usage_data=None,  # Pas de données d'utilisation pour l'instant
                        threshold_days=30
                    )
                    
                    if dormant_licenses:
                        st.warning(f"⚠️ **{len(dormant_licenses)} licence(s) dormante(s) détectée(s)**")
                        dormant_df = pd.DataFrame(dormant_licenses)
                        st.dataframe(dormant_df, use_container_width=True)
                    
                    # Calculer le score GreenOps
                    if number_of_employees > 0:
                        greenops_result = calculate_greenops_score(
                            total_cost=total_cost,
                            total_carbon_g=total_carbon_g,
                            number_of_employees=number_of_employees,
                            number_of_licenses=len(saas_results),
                            dormant_licenses_count=len(dormant_licenses)
                        )
                        st.session_state.greenops_results = greenops_result
                        
                        st.subheader("🏆 Score GreenOps")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(
                                "Score",
                                f"{greenops_result['grade']} - {greenops_result['grade_name']}",
                                help=f"Score: {greenops_result['score']}/100"
                            )
                        with col2:
                            st.metric(
                                "Coût/employé",
                                f"{greenops_result['cost_per_employee']:.2f} €",
                                help=f"Seuil max pour {greenops_result['grade']}: {greenops_result['cost_per_employee']:.2f} €"
                            )
                        with col3:
                            st.metric(
                                "CO₂/employé",
                                f"{greenops_result['carbon_per_employee']:.1f} g",
                                help=f"Seuil max pour {greenops_result['grade']}: {greenops_result['carbon_per_employee']:.1f} g"
                            )
                        
                        # Barre de progression
                        st.progress(greenops_result['score'] / 100)
                        st.caption(f"Score GreenOps: {greenops_result['score']}/100")
                        
                        # Recommandations
                        recommendations = generate_greenops_recommendations(
                            greenops_result,
                            total_cost,
                            total_carbon_g,
                            dormant_licenses
                        )
                        
                        if recommendations:
                            st.subheader("💡 Recommandations")
                            for rec in recommendations:
                                st.info(rec)
                        
                        # Calculer les économies potentielles
                        savings = calculate_potential_savings(
                            total_cost,
                            total_carbon_g,
                            dormant_licenses,
                            saas_results
                        )
                        
                        if savings['cost_savings'] > 0:
                            st.success(f"""
                            🎉 **Économies potentielles**
                            - **Coût** : {savings['cost_savings']:.2f} €/mois ({savings['percentage_cost_savings']:.1f}%)
                            - **CO₂** : {savings['carbon_savings_g']:.1f} g/mois ({savings['percentage_carbon_savings']:.1f}%)
                            """)
                        
                        # Ajouter à l'historique
                        st.session_state.history.append({
                            "type": "Tracker Shadow AI",
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "cost": total_cost,
                            "carbon": total_carbon_g,
                            "score": f"{greenops_result['grade']} ({greenops_result['score']}/100)",
                            "subscriptions_count": len(saas_results),
                            "dormant_count": len(dormant_licenses)
                        })
                    
                    # Bouton pour générer un rapport
                    st.subheader("📄 Générer un Rapport")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📊 Rapport de Résumé (PDF)", type="primary"):
                            with st.spinner("Génération du rapport en cours..."):
                                result = generate_summary_report(
                                    company_name="Votre Entreprise",
                                    total_cost=total_cost,
                                    total_carbon_g=total_carbon_g,
                                    greenops_result=greenops_result if 'greenops_result' in locals() else None,
                                    saas_count=len(saas_results),
                                    dormant_count=len(dormant_licenses),
                                    output_path="rapport_sobre_resume.pdf"
                                )
                                
                                if result["success"]:
                                    st.success(result["message"])
                                    
                                    # Lire et télécharger le fichier
                                    with open(result["file_path"], "rb") as f:
                                        st.download_button(
                                            label="⬇️ Télécharger le Rapport",
                                            data=f,
                                            file_name="rapport_sobre_resume.pdf",
                                            mime="application/pdf"
                                        )
                                    
                                    # Supprimer le fichier temporaire
                                    os.remove(result["file_path"])
                                else:
                                    st.error(result["message"])
                    
                    with col2:
                        if st.button("📋 Rapport CSRD (PDF)", type="primary"):
                            with st.spinner("Génération du rapport CSRD en cours..."):
                                result = generate_csrd_report(
                                    company_name="Votre Entreprise",
                                    total_cost=total_cost,
                                    total_carbon_g=total_carbon_g,
                                    greenops_result=greenops_result if 'greenops_result' in locals() else None,
                                    saas_subscriptions=saas_results,
                                    dormant_licenses=dormant_licenses,
                                    recommendations=recommendations if 'recommendations' in locals() else [],
                                    output_path="rapport_sobre_csrd.pdf"
                                )
                                
                                if result["success"]:
                                    st.success(result["message"])
                                    
                                    # Lire et télécharger le fichier
                                    with open(result["file_path"], "rb") as f:
                                        st.download_button(
                                            label="⬇️ Télécharger le Rapport CSRD",
                                            data=f,
                                            file_name="rapport_sobre_csrd.pdf",
                                            mime="application/pdf"
                                        )
                                    
                                    # Supprimer le fichier temporaire
                                    os.remove(result["file_path"])
                                else:
                                    st.error(result["message"])
                    
                else:
                    st.warning("⚠️ Aucun abonnement IA détecté. Vérifiez que votre fichier contient des données valides.")
        
        except Exception as e:
            st.error(f"❌ **Erreur** : {str(e)}")
            st.caption("Vérifiez que votre fichier est au format CSV et contient les colonnes nécessaires.")


# ============================================================================
# MODE 2: CALCULATEUR API (Mode existant amélioré)
# ============================================================================
elif mode == "Calculateur API":
    st.header("🧮 Calculateur API")
    st.markdown("""
    Calculez le coût et l'empreinte carbone pour l'utilisation d'**APIs IA** 
    (GPT-4, Mistral-7B, Llama-2, etc.).
    
    💡 **Conseil** : Utilisez ce mode si vous utilisez directement les APIs des fournisseurs d'IA.
    """)
    
    # Sélection du modèle
    from utils.cost_calculator import MODELS
    model_names = list(MODELS.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        model = st.selectbox(
            "Sélectionnez un modèle",
            model_names,
            index=0,
            help="Modèle IA utilisé (ex: GPT-4, Mistral-7B)"
        )
    with col2:
        input_tokens = st.number_input(
            "Nombre de tokens (entrée)",
            min_value=0,
            value=1000,
            step=100,
            help="Nombre de tokens dans la requête d'entrée"
        )
    
    output_tokens = st.number_input(
        "Nombre de tokens (sortie)",
        min_value=0,
        value=500,
        step=100,
        help="Nombre de tokens dans la réponse (sortie)"
    )
    
    if st.button("🔍 Calculer", type="primary", use_container_width=True):
        with st.spinner("Calcul en cours..."):
            # Calculer le coût
            cost_result = calculate_api_cost(
                model_name=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            
            # Calculer le CO2
            carbon_result = calculate_api_carbon(
                model_name=model,
                total_tokens=input_tokens + output_tokens
            )
            
            # Calculer le score de maturité (ancien système)
            from scripts.sobre_calculator import get_matuity_badge, get_recommendations
            badge, score = get_matuity_badge(cost_result['total_cost'], carbon_result['carbon_g'])
            recommendations = get_recommendations(model, input_tokens + output_tokens, cost_result['total_cost'])
        
        # Afficher les résultats
        st.subheader(f"📊 Résultats pour {input_tokens + output_tokens:,} tokens avec {model}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Coût total", f"{cost_result['total_cost']:.2f} €")
        with col2:
            st.metric("🌍 CO₂", f"{carbon_result['carbon_g']:.1f} g")
        with col3:
            st.metric("🚗 Équivalent voiture", f"{carbon_result['co2_car_km']:.1f} km")
        with col4:
            st.metric("🏆 Score", f"{score}/100")
        
        st.markdown(f"### {badge}")
        
        # Graphiques
        st.subheader("📈 Comparaison avec d'autres modèles")
        
        # Comparer avec tous les modèles pour le même nombre de tokens
        comparison_data = []
        for m in model_names:
            c = calculate_api_cost(m, input_tokens, output_tokens)
            comparison_data.append({
                "modèle": m,
                "coût": c['total_cost'],
                "coût_par_million": c['total_cost'] / (input_tokens + output_tokens) * 1_000_000
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                comparison_df,
                x="modèle",
                y="coût",
                title=f"Coût pour {input_tokens + output_tokens:,} tokens",
                color="coût",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                comparison_df.sort_values("coût_par_million"),
                x="modèle",
                y="coût_par_million",
                title="Coût par million de tokens",
                color="coût_par_million",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommandations
        if recommendations:
            st.subheader("💡 Recommandations")
            for rec in recommendations:
                st.info(rec)
        
        # Ajouter à l'historique
        st.session_state.history.append({
            "type": "Calcul API",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "model": model,
            "tokens": input_tokens + output_tokens,
            "cost": cost_result['total_cost'],
            "carbon": carbon_result['carbon_g'],
            "score": score
        })


# ============================================================================
# MODE 3: COMPARAISON MODÈLES (Mode existant amélioré)
# ============================================================================
elif mode == "Comparaison Modèles":
    st.header("🔄 Comparaison entre Modèles")
    st.markdown("""
    Comparez les **coûts** et **l'empreinte carbone** de différents modèles IA 
    pour un nombre de tokens donné.
    """)
    
    from utils.cost_calculator import MODELS
    model_names = list(MODELS.keys())
    
    tokens = st.number_input(
        "Nombre de tokens à comparer",
        min_value=1,
        value=10000,
        step=1000,
        help="Nombre total de tokens (input + output)"
    )
    
    if st.button("🔍 Comparer", type="primary", use_container_width=True):
        comparison_results = []
        
        for model_name in model_names:
            # Calculer le coût (on suppose 50% input / 50% output)
            input_tokens = tokens // 2
            output_tokens = tokens - input_tokens
            
            cost_result = calculate_api_cost(model_name, input_tokens, output_tokens)
            carbon_result = calculate_api_carbon(model_name, tokens)
            
            comparison_results.append({
                "modèle": model_name,
                "coût": cost_result['total_cost'],
                "coût_par_million": cost_result['total_cost'] / tokens * 1_000_000,
                "co2_g": carbon_result['carbon_g'],
                "co2_par_million": carbon_result['carbon_g'] / tokens * 1_000_000,
                "co2_car_km": carbon_result['co2_car_km']
            })
        
        comparison_df = pd.DataFrame(comparison_results)
        
        # Trier par coût croissant
        comparison_df = comparison_df.sort_values("coût")
        
        # Afficher le tableau
        st.subheader(f"📊 Comparaison pour {tokens:,} tokens")
        
        display_df = comparison_df.copy()
        display_df["coût"] = display_df["coût"].apply(lambda x: f"{x:.2f} €")
        display_df["co2_g"] = display_df["co2_g"].apply(lambda x: f"{x:.1f} g")
        display_df["coût_par_million"] = display_df["coût_par_million"].apply(lambda x: f"{x:.2f} €")
        display_df["co2_par_million"] = display_df["co2_par_million"].apply(lambda x: f"{x:.1f} g")
        display_df["co2_car_km"] = display_df["co2_car_km"].apply(lambda x: f"{x:.1f} km")
        
        st.dataframe(
            display_df[["modèle", "coût", "coût_par_million", "co2_g", "co2_par_million", "co2_car_km"]],
            use_container_width=True,
            hide_index=True
        )
        
        # Graphiques
        st.subheader("📈 Visualisations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_cost = px.bar(
                comparison_df,
                x="modèle",
                y="coût",
                title="Coût par modèle",
                labels={"coût": "Coût (€)", "modèle": "Modèle"},
                color="coût",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_cost, use_container_width=True)
        
        with col2:
            fig_co2 = px.bar(
                comparison_df,
                x="modèle",
                y="co2_g",
                title="CO₂ par modèle",
                labels={"co2_g": "CO₂ (g)", "modèle": "Modèle"},
                color="co2_g",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_co2, use_container_width=True)
        
        # Graphique scatter (coût vs CO2)
        fig_scatter = px.scatter(
            comparison_df,
            x="coût",
            y="co2_g",
            size="coût_par_million",
            color="modèle",
            hover_data=["co2_car_km"],
            title="Coût vs CO₂ (taille = coût par million de tokens)",
            labels={"coût": "Coût (€)", "co2_g": "CO₂ (g)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Meilleur choix
        best_model = comparison_df.iloc[0]
        st.subheader("🏆 Meilleur choix pour ce nombre de tokens")
        st.success(f"""
        **{best_model['modèle']}**
        - Coût: **{best_model['coût']:.2f} €**
        - CO₂: **{best_model['co2_g']:.1f} g** (équivalent {best_model['co2_car_km']:.1f} km en voiture)
        - Coût par million: **{best_model['coût_par_million']:.2f} €/M tokens**
        - CO₂ par million: **{best_model['co2_par_million']:.1f} g/M tokens**
        """)
        
        # Ajouter à l'historique
        st.session_state.history.append({
            "type": "Comparaison Modèles",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tokens": tokens,
            "best_model": best_model['modèle'],
            "best_cost": best_model['coût']
        })


# ============================================================================
# MODE 4: GÉNÉRATEUR DE RAPPORTS (Mode autonome)
# ============================================================================
elif mode == "Générateur de Rapports":
    st.header("📄 Générateur de Rapports")
    st.markdown("""
    Générez des **rapports professionnels** (PDF) pour vos analyses.
    
    📌 **Types de rapports disponibles** :
    - **Rapport de Résumé** : Vue d'ensemble des coûts et CO₂.
    - **Rapport CSRD** : Rapport complet pour la conformité réglementaire.
    """)
    
    # Options du rapport
    st.subheader("⚙️ Paramètres du Rapport")
    
    company_name = st.text_input(
        "Nom de l'entreprise",
        value="Votre Entreprise",
        help="Nom de votre entreprise pour le rapport"
    )
    
    # Données manuelles (si pas d'import de fichier)
    st.markdown("### 📊 Données Manuelles")
    
    col1, col2 = st.columns(2)
    with col1:
        manual_total_cost = st.number_input(
            "Coût total mensuel (€)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )
    with col2:
        manual_total_carbon = st.number_input(
            "CO₂ total mensuel (g)",
            min_value=0.0,
            value=0.0,
            step=1.0
        )
    
    manual_saas_count = st.number_input(
        "Nombre d'abonnements SaaS",
        min_value=0,
        value=0
    )
    
    manual_dormant_count = st.number_input(
        "Nombre de licences dormantes",
        min_value=0,
        value=0
    )
    
    # Calculer le score GreenOps
    if manual_total_cost > 0 or manual_total_carbon > 0:
        greenops_result = calculate_greenops_score(
            total_cost=manual_total_cost,
            total_carbon_g=manual_total_carbon,
            number_of_employees=number_of_employees,
            number_of_licenses=manual_saas_count,
            dormant_licenses_count=manual_dormant_count
        )
        
        st.subheader("🏆 Score GreenOps Estimé")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{greenops_result['grade']} - {greenops_result['grade_name']}")
        with col2:
            st.metric("Coût/employé", f"{greenops_result['cost_per_employee']:.2f} €")
        with col3:
            st.metric("CO₂/employé", f"{greenops_result['carbon_per_employee']:.1f} g")
    else:
        greenops_result = None
    
    # Génération des rapports
    st.subheader("📄 Générer un Rapport")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Rapport de Résumé (PDF)", type="primary", use_container_width=True):
            if greenops_result:
                with st.spinner("Génération du rapport en cours..."):
                    result = generate_summary_report(
                        company_name=company_name,
                        total_cost=manual_total_cost,
                        total_carbon_g=manual_total_carbon,
                        greenops_result=greenops_result,
                        saas_count=manual_saas_count,
                        dormant_count=manual_dormant_count,
                        output_path="rapport_manuel_resume.pdf"
                    )
                    
                    if result["success"]:
                        st.success(result["message"])
                        
                        with open(result["file_path"], "rb") as f:
                            st.download_button(
                                label="⬇️ Télécharger le Rapport",
                                data=f,
                                file_name="rapport_sobre_resume.pdf",
                                mime="application/pdf"
                            )
                        
                        os.remove(result["file_path"])
                    else:
                        st.error(result["message"])
            else:
                st.warning("⚠️ Veuillez entrer des données valides avant de générer un rapport.")
    
    with col2:
        if st.button("📋 Rapport CSRD (PDF)", type="primary", use_container_width=True):
            if greenops_result:
                with st.spinner("Génération du rapport CSRD en cours..."):
                    # Créer des données fictives pour le rapport CSRD
                    saas_subscriptions = []
                    for i in range(manual_saas_count):
                        saas_subscriptions.append({
                            "name": f"SaaS {i+1}",
                            "monthly_cost": manual_total_cost / manual_saas_count if manual_saas_count > 0 else 0,
                            "saas_type": "subscription"
                        })
                    
                    dormant_licenses = []
                    for i in range(manual_dormant_count):
                        dormant_licenses.append({
                            "name": f"SaaS Dormant {i+1}",
                            "status": "dormant"
                        })
                    
                    recommendations = []
                    if manual_dormant_count > 0:
                        recommendations.append(
                            f"Désactivez les {manual_dormant_count} licences dormantes pour économiser."
                        )
                    
                    result = generate_csrd_report(
                        company_name=company_name,
                        total_cost=manual_total_cost,
                        total_carbon_g=manual_total_carbon,
                        greenops_result=greenops_result,
                        saas_subscriptions=saas_subscriptions,
                        dormant_licenses=dormant_licenses,
                        recommendations=recommendations,
                        output_path="rapport_manuel_csrd.pdf"
                    )
                    
                    if result["success"]:
                        st.success(result["message"])
                        
                        with open(result["file_path"], "rb") as f:
                            st.download_button(
                                label="⬇️ Télécharger le Rapport CSRD",
                                data=f,
                                file_name="rapport_sobre_csrd.pdf",
                                mime="application/pdf"
                            )
                        
                        os.remove(result["file_path"])
                    else:
                        st.error(result["message"])
            else:
                st.warning("⚠️ Veuillez entrer des données valides avant de générer un rapport.")


# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>🌱 Sobre - GreenOps + FinOps pour les PME</strong></p>
    <p>Développé avec ❤️ par <a href="https://github.com/sobre-aziz" target="_blank">Aziz</a> | 
    <a href="https://github.com/sobre-aziz/sobre" target="_blank">GitHub</a></p>
    <p style="font-size: 0.9em;">
        Données basées sur des estimations publiques. Pour des valeurs précises, 
        consultez les fournisseurs (OpenAI, Mistral AI, etc.).
    </p>
    <p style="font-size: 0.8em; color: #999;">
        Version 2.0 - Ciblant les PME avec Tracker Shadow AI et rapports CSRD
    </p>
</div>
""", unsafe_allow_html=True)
