

# ============================================================================
# MODE 5: METHODOLOGIE
# ============================================================================
elif mode == "Methodologie":
    st.header("Methodologie")
    st.markdown("""
    Cette page detaille **toutes les sources, formules, hypotheses et limites** utilisees par Sobre.
    
    Pour plus de details, consultez [docs/METHODOLOGIE.md](docs/METHODOLOGIE.md).
    """)
    
    # Charger la methodologie depuis docs/METHODOLOGIE.md
    try:
        with open("docs/METHODOLOGIE.md", "r", encoding="utf-8") as f:
            methodology_content = f.read()
        
        # Afficher le contenu
        st.markdown(methodology_content)
    except FileNotFoundError:
        st.error("Le fichier docs/METHODOLOGIE.md est introuvable.")
