# 🌱 Sobre - GreenOps + FinOps pour l'IA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sobre.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Sobre** est une **plateforme open-source** qui permet de **mesurer, comparer et optimiser** le coût et l'empreinte carbone de vos requêtes IA.

## 📌 À propos

### **Pourquoi Sobre ?**
L'intelligence artificielle révolutionne de nombreux secteurs, mais son utilisation a un **coût financier et environnemental important** :

- 💰 **Coût** : Une requête à GPT-4 peut coûter **0.03€ par 1k tokens** (soit ~30€ pour 1M tokens).
- 🌍 **Environnement** : L'IA pourrait représenter **20% de la consommation électrique mondiale d'ici 2030** (source : [MIT](https://news.mit.edu/2023/ai-energy-consumption-0301)).
- 🚗 **Impact concret** : Une seule requête GPT-4 émet **autant de CO₂ que 10 km en voiture**.

Sobre vous aide à **comprendre ces impacts** et à **prendre des décisions éclairées** pour vos projets IA.

### **Fonctionnalités**

| Fonctionnalité | Description |
|---------------|-------------|
| ✅ **Calculateur** | Calculez le coût et le CO₂ pour un modèle et un nombre de tokens. |
| ✅ **Comparaison** | Comparez tous les modèles pour un nombre de tokens donné. |
| ✅ **Badges de maturité** | Évaluez votre usage avec un score (Or, Argent, Bronze, Rouge). |
| ✅ **Recommandations** | Obtenez des conseils personnalisés pour optimiser vos coûts et votre impact. |
| ✅ **Historique** | Conservez un historique de vos calculs. |
| ✅ **Visualisations** | Graphiques interactifs (Plotly) pour comparer les modèles. |

## 🚀 Installation

### **Prérequis**
- Python **3.9 ou supérieur**
- pip (généralement inclus avec Python)

### **Installation locale**

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/sobre-aziz/sobre.git
   cd sobre
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application** :
   ```bash
   streamlit run app.py
   ```

4. **Ouvrir dans votre navigateur** :
   L'application sera disponible à l'adresse : [http://localhost:8501](http://localhost:8501)

### **Déploiement sur Streamlit Cloud**

1. **Forker le dépôt** sur GitHub.
2. **Créer un compte** sur [Streamlit Cloud](https://streamlit.io/cloud).
3. **Déployer** :
   - Cliquez sur **"New App"**.
   - Sélectionnez votre dépôt forké.
   - Choisissez **Python 3.9+** comme version.
   - Cliquez sur **"Deploy"**.

4. **Votre application sera disponible** à une URL du type : `https://votre-nom-sobre.streamlit.app`

## 📊 Utilisation

### **Mode Calcul Simple**
1. Sélectionnez un **modèle IA** (ex: Mistral-7B, GPT-4, Llama-3).
2. Entrez le **nombre de tokens** (input + output).
3. Cliquez sur **"Calculer"**.
4. Obtenez :
   - Le **coût en €**.
   - L'**empreinte carbone en g**.
   - L'**équivalent en km voiture**.
   - Un **score de maturité** (Or, Argent, Bronze, Rouge).
   - Des **recommandations personnalisées**.

### **Mode Comparaison**
1. Entrez un **nombre de tokens**.
2. Cliquez sur **"Comparer"**.
3. Obtenez :
   - Un **tableau comparatif** de tous les modèles.
   - Des **graphiques** (coût, CO₂, score).
   - Le **meilleur choix** pour votre usage.

### **Historique**
- Tous vos calculs sont **enregistrés** dans la sidebar.
- Vous pouvez **vider l'historique** à tout moment.

## 📁 Structure du Projet

```
sobre/
├── app.py                      # Interface Streamlit
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── config/
│   └── models.yaml             # Configuration des modèles (coût, CO₂)
└── scripts/
    └── sobre_calculator.py      # Logique métier (calculs, recommandations)
```

### **Configuration des Modèles**
Les données des modèles (coût par token, CO₂ par token) sont stockées dans `config/models.yaml`. Vous pouvez :

- **Ajouter un modèle** :
  ```yaml
  models:
    Nouveau-Modèle:
      name: "Nouveau-Modèle"
      description: "Description du modèle"
      cost_per_token: 0.000001
      co2_per_token: 0.0003
      provider: "Fournisseur"
      category: "open-source"
  ```

- **Modifier les seuils des badges** :
  ```yaml
  badges:
    gold:
      name: "🥇 Or - Expert"
      max_cost: 10
      max_co2: 50
      score: 100
  ```

## 🔧 Dépendances

| Dépendance | Version | Usage |
|------------|---------|-------|
| streamlit | 1.28.0+ | Interface web |
| pandas | 2.0.3+ | Manipulation de données |
| plotly | 5.15.0+ | Graphiques interactifs |
| pyyaml | 6.0+ | Lecture du fichier YAML |
| requests | 2.31.0+ | Requêtes HTTP (futur) |

## 🤝 Contribution

Les contributions sont **les bienvenues** ! Voici comment contribuer :

1. **Forker le dépôt**.
2. **Créer une branche** (`git checkout -b feature/ma-fonctionnalité`).
3. **Commiter vos changements** (`git commit -m "Ajout de ma fonctionnalité"`).
4. **Pousser vers la branche** (`git push origin feature/ma-fonctionnalité`).
5. **Ouvrir une Pull Request**.

### **Idées de Contributions**
- [ ] Ajouter plus de modèles (ex: Claude, Gemini, etc.).
- [ ] Intégrer des **APIs officielles** pour récupérer les tarifs en temps réel.
- [ ] Ajouter un **mode "Projet"** pour calculer le coût/CO₂ d'un projet entier.
- [ ] Implémenter une **API REST** pour une intégration facile.
- [ ] Ajouter des **alertes** (ex: "Votre coût a augmenté de 20% ce mois-ci").
- [ ] Créer un **système de labels "Green AI"** pour les entreprises.

## 📜 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **Streamlit** pour son framework incroyable.
- **Mistral AI**, **OpenAI**, **Meta** pour leurs modèles.
- **La communauté open-source** pour ses contributions.

## 📞 Contact

- **Auteur** : [Aziz](https://github.com/sobre-aziz)
- **Email** : [aziz@example.com](mailto:aziz@example.com) *(à remplacer)*
- **LinkedIn** : [LinkedIn](https://linkedin.com/in/aziz) *(à remplacer)*
- **Projet** : [GitHub](https://github.com/sobre-aziz/sobre)

---

**✨ Sobre - Parce que l'IA peut être à la fois puissante et responsable.**
