import streamlit as st
import pandas as pd
import plotly.express as px
from scripts.sobre_calculator import (
    calculate_cost_and_co2, 
    get_matuity_badge, 
    get_recommendations,
    get_all_models,
    compare_models
)

# Configuration de la page
st.set_page_config(
    page_title="Sobre - GreenOps + FinOps", 
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre et description
st.title("🌱 Sobre - Mesurez le coût et l'empreinte carbone de votre IA")
st.markdown("""
**Sobre** vous aide à **comprendre, comparer et optimiser** le coût et l'impact environnemental de vos requêtes IA.

💡 **Pourquoi c'est important ?**
- L'IA représente **~1% de la consommation électrique mondiale** (2024).
- Une seule requête GPT-4 peut émettre **autant de CO₂ que 10 km en voiture**. 
- Les coûts peuvent **exploser** si non maîtrisés (ex: 1M tokens = ~30€ avec GPT-4).
""")

# Initialiser l'historique dans la session
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Sélection du mode
    mode = st.radio(
        "Mode",
        ["Calcul simple", "Comparaison entre modèles"],
        index=0
    )
    
    # Afficher l'historique
    st.header("📜 Historique")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history[-5:][::-1]):  # Derniers 5
            st.markdown(f"""
            **{item['model']}** - {item['tokens']:,} tokens
            - Coût: **{item['cost']:.2f} €**
            - CO₂: **{item['co2']:,.1f} g** ({item['co2_car_km']:,.1f} km voiture)
            - Score: **{item['score']}/100** {item['badge']}
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
    **À propos**  
    Projet développé par [Aziz](https://github.com/sobre-aziz)  
    [GitHub](https://github.com/sobre-aziz/sobre) | [Documentation](#)
    """)

# Mode Calcul Simple
if mode == "Calcul simple":
    st.header("🧮 Calculateur")
    
    col1, col2 = st.columns(2)
    with col1:
        model = st.selectbox(
            "Sélectionnez un modèle",
            get_all_models(),
            index=0,
            help="Choisissez le modèle IA que vous utilisez"
        )
    with col2:
        tokens = st.number_input(
            "Nombre de tokens",
            min_value=1,
            value=10000,
            step=1000,
            help="Nombre de tokens dans votre requête (input + output)"
        )
    
    if st.button("🔍 Calculer", type="primary", use_container_width=True):
        with st.spinner("Calcul en cours..."):
            result = calculate_cost_and_co2(model, tokens)
            badge, score = get_matuity_badge(result["cost"], result["co2"])
            recommendations = get_recommendations(model, tokens, result["cost"])
            
            # Ajouter à l'historique
            st.session_state.history.append({
                "model": model,
                "tokens": tokens,
                "cost": result["cost"],
                "co2": result["co2"],
                "co2_car_km": result["co2_car_km"],
                "badge": badge,
                "score": score
            })
        
        # Afficher les résultats
        st.subheader(f"📊 Résultats pour {tokens:,} tokens avec {model}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Coût", f"{result['cost']:.2f} €")
        with col2:
            st.metric("🌍 CO₂", f"{result['co2']:,.1f} g")
        with col3:
            st.metric("🚗 Équivalent voiture", f"{result['co2_car_km']:,.1f} km")
        with col4:
            st.metric("🏆 Score", f"{score}/100")
        
        # Afficher le badge
        st.markdown(f"### {badge}")
        
        # Graphique de comparaison visuelle
        st.subheader("📈 Visualisation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique coût par modèle (comparaison)
            comparison_data = compare_models(tokens)
            df_cost = pd.DataFrame(comparison_data)
            fig_cost = px.bar(
                df_cost,
                x="model",
                y="cost",
                title=f"Comparaison des coûts pour {tokens:,} tokens",
                labels={"cost": "Coût (€)", "model": "Modèle"},
                color="model",
                text="cost"
            )
            fig_cost.update_traces(texttemplate="€%{text:.2f}", textposition="outside")
            st.plotly_chart(fig_cost, use_container_width=True)
        
        with col2:
            # Graphique CO2 par modèle
            fig_co2 = px.bar(
                df_cost,
                x="model",
                y="co2",
                title=f"Comparaison CO₂ pour {tokens:,} tokens",
                labels={"co2": "CO₂ (g)", "model": "Modèle"},
                color="model",
                text="co2"
            )
            fig_co2.update_traces(texttemplate="%{text:,.1f} g", textposition="outside")
            st.plotly_chart(fig_co2, use_container_width=True)
        
        # Recommandations
        if recommendations:
            st.subheader("💡 Recommandations")
            for rec in recommendations:
                st.info(rec)

# Mode Comparaison entre modèles
elif mode == "Comparaison entre modèles":
    st.header("🔄 Comparaison entre modèles")
    
    tokens_compare = st.number_input(
        "Nombre de tokens à comparer",
        min_value=1,
        value=10000,
        step=1000,
        help="Nombre de tokens pour la comparaison"
    )
    
    if st.button("🔍 Comparer", type="primary", use_container_width=True):
        comparison_results = compare_models(tokens_compare)
        
        # Afficher les résultats sous forme de tableau
        st.subheader(f"📊 Comparaison pour {tokens_compare:,} tokens")
        
        df = pd.DataFrame(comparison_results)
        df_display = df.copy()
        df_display["cost"] = df_display["cost"].apply(lambda x: f"{x:.2f} €")
        df_display["co2"] = df_display["co2"].apply(lambda x: f"{x:,.1f} g")
        df_display["co2_car_km"] = df_display["co2_car_km"].apply(lambda x: f"{x:,.1f} km")
        
        st.dataframe(
            df_display[["model", "cost", "co2", "co2_car_km", "badge", "score", "provider"]],
            use_container_width=True,
            hide_index=True
        )
        
        # Graphiques
        st.subheader("📈 Visualisations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique coût
            fig_cost = px.bar(
                df,
                x="model",
                y="cost",
                title="Coût par modèle",
                labels={"cost": "Coût (€)", "model": "Modèle"},
                color="cost",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_cost, use_container_width=True)
        
        with col2:
            # Graphique CO2
            fig_co2 = px.bar(
                df,
                x="model",
                y="co2",
                title="Émissions CO₂ par modèle",
                labels={"co2": "CO₂ (g)", "model": "Modèle"},
                color="co2",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_co2, use_container_width=True)
        
        # Graphique score
        fig_score = px.bar(
            df,
            x="model",
            y="score",
            title="Score de maturité par modèle",
            labels={"score": "Score /100", "model": "Modèle"},
            color="score",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig_score, use_container_width=True)
        
        # Graphique combiné coût/CO2
        fig_scatter = px.scatter(
            df,
            x="cost",
            y="co2",
            size="score",
            color="model",
            hover_data=["provider", "category"],
            title="Coût vs CO₂ (taille = score)",
            labels={"cost": "Coût (€)", "co2": "CO₂ (g)"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Meilleur choix
        best_model = df.iloc[0]
        st.subheader("🏆 Meilleur choix pour ce nombre de tokens")
        st.success(f"""
        **{best_model['model']}** ({best_model['provider']})
        - Coût: **{best_model['cost']:.2f} €**
        - CO₂: **{best_model['co2']:,.1f} g**
        - Score: **{best_model['score']}/100** {best_model['badge']}
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🌱 Sobre - GreenOps + FinOps pour l'IA | Développé avec ❤️ par Aziz</p>
    <p>Données basées sur des estimations publiques. Pour des valeurs précises, consultez les fournisseurs.</p>
</div>
""", unsafe_allow_html=True)
