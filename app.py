import streamlit as st
import pandas as pd
from scripts.sobre_calculator import calculate_cost_and_co2, get_matuity_badge, get_recommendations

st.set_page_config(page_title="Sobre - GreenOps + FinOps", page_icon="🌱")
st.title("🌱 Sobre - Mesurez le coût et l'empreinte carbone de votre IA")

model = st.selectbox("Sélectionnez un modèle", ["Mistral-7B", "GPT-4", "Llama-3"])
tokens = st.number_input("Nombre de tokens", min_value=1, value=1000000, step=100000)

if st.button("🔍 Calculer"):
    result = calculate_cost_and_co2(model, tokens)
    badge, score = get_matuity_badge(result["cost"], result["co2"])
    recommendations = get_recommendations(model, tokens, result["cost"])

    st.subheader(f"Résultats pour {tokens:,} tokens avec {model}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Coût", f"{result['cost']:.2f} €")
    with col2:
        st.metric("🌍 CO₂", f"{result['co2']:,.1f} g")
    with col3:
        st.metric("🏆 Score", f"{score}/100")

    st.markdown(f"### {badge}")
    if recommendations:
        st.subheader("💡 Recommandations")
        for rec in recommendations:
            st.info(rec)
