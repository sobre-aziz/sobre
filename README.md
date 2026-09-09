# 🌱 Sobre - GreenOps + FinOps pour les PME

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sobre.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-78%20passed-green.svg)](https://github.com/sobre-aziz/sobre/actions)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Sobre** est une **plateforme open-source** conçue pour aider les **PME** à **réduire leurs coûts cachés liés à l'IA** (abonnements SaaS comme Copilot, Notion AI, ChatGPT Plus, ou APIs comme GPT-4, Mistral-7B) et à **mesurer leur empreinte carbone**.

🔹 **Version 2.0** - Spécialement adaptée pour les PME avec :
- **Tracker Shadow AI** : Détection automatique des abonnements IA dans vos factures
- **Score GreenOps** : Évaluation de A à E de votre performance
- **Génération de rapports CSRD** : Conformité réglementaire
- **Calcul des économies potentielles** : Identifiez les licences dormantes

---

## 📌 À propos

### **Pourquoi Sobre ?**

L'intelligence artificielle révolutionne les PME, mais son utilisation a un **coût financier et environnemental important** :

- 💰 **Coûts cachés** : Les abonnements SaaS (ChatGPT Plus, Copilot, Notion AI) et les APIs (GPT-4, Mistral-7B) peuvent représenter **des milliers d'euros par an** sans que les équipes en aient conscience.
- 🌍 **Impact environnemental** : Une seule requête GPT-4 émet **autant de CO₂ que 0.6 km en voiture** (source : Microsoft Sustainability Report 2023).
- 📊 **Manque de visibilité** : **60% des PME** ne savent pas combien elles dépensent en outils IA (étude Forrester 2024).

Sobre vous aide à :
✅ **Identifier** tous vos abonnements IA (même cachés)
✅ **Mesurer** vos coûts et votre empreinte carbone
✅ **Optimiser** vos dépenses en désactivant les licences inutilisées
✅ **Conformité** : Générer des rapports CSRD pour vos obligations légales

### **Cible**
- **PME** utilisant des SaaS avec IA (ex: Copilot, Notion AI, ChatGPT Plus)
- **Startups** et **agences digitales** utilisant des APIs d'IA
- **Équipes tech** souhaitant optimiser leurs coûts cloud/IA

---

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

---

## 📊 Fonctionnalités

### **🎯 Tracker Shadow AI (Mode Principal)**
- **Import de factures CSV** (QuickBooks, Pennylane, export manuel)
- **Détection automatique** des abonnements IA via mots-clés
- **Identification des licences dormantes** (non utilisées depuis 30+ jours)
- **Calcul du score GreenOps** (A à E) avec recommandations
- **Estimation des économies potentielles** (coût et CO₂)

### **🧮 Calculateur API**
- Calcul du **coût** pour les modèles IA (GPT-4, Mistral-7B, Llama-2, etc.)
- Calcul de **l'empreinte carbone** (basé sur des données scientifiques)
- Comparaison entre modèles pour un même nombre de tokens
- Recommandations pour optimiser vos coûts

### **🔄 Comparaison entre Modèles**
- Comparez tous les modèles pour un nombre de tokens donné
- Visualisations graphiques (coût, CO₂, score)
- Identification du **meilleur choix** pour votre usage

### **📄 Générateur de Rapports**
- **Rapport de Résumé** : Vue d'ensemble des coûts et CO₂
- **Rapport CSRD** : Rapport complet pour la conformité réglementaire
- Export au format **PDF**

---

## 📈 Utilisation

### **1. Tracker Shadow AI (Recommandé pour les PME)**

1. **Importez vos factures** :
   - Sélectionnez un fichier **CSV** (export QuickBooks, Pennylane, ou manuel)
   - Le fichier doit contenir au minimum les colonnes : **Nom** (ou Service) et **Coût** (ou Montant)

2. **Détection automatique** :
   - Sobre **identifie** automatiquement les abonnements IA (ChatGPT, Copilot, Notion AI, etc.)
   - Affiche la liste des abonnements détectés avec leur **coût mensuel** et **empreinte carbone**

3. **Analyse des résultats** :
   - **Coût total mensuel** : Somme de tous vos abonnements IA
   - **CO₂ total mensuel** : Empreinte carbone totale (en g et équivalent km voiture)
   - **Score GreenOps** : Note de A à E selon votre performance
   - **Licences dormantes** : Abonnements inutilisés à désactiver
   - **Économies potentielles** : Montant que vous pourriez économiser

4. **Générez un rapport** :
   - **Rapport de Résumé** : Pour une vue d'ensemble rapide
   - **Rapport CSRD** : Pour la conformité réglementaire

**Exemple de fichier CSV valide** :
```csv
Nom,Coût,Date
ChatGPT Plus,20.00,2024-01-01
GitHub Copilot,10.00,2024-01-01
Notion AI,10.00,2024-01-01
Zoom,15.00,2024-01-01
```

### **2. Calculateur API**

1. Sélectionnez un **modèle IA** (GPT-4, Mistral-7B, Llama-2-70B, etc.)
2. Entrez le **nombre de tokens** (input et output)
3. Cliquez sur **"Calculer"**
4. Obtenez :
   - Le **coût total** en €
   - L'**empreinte carbone** en g et km voiture
   - Un **score de maturité**
   - Des **recommandations personnalisées**

### **3. Comparaison entre Modèles**

1. Entrez un **nombre de tokens**
2. Cliquez sur **"Comparer"**
3. Obtenez :
   - Un **tableau comparatif** de tous les modèles
   - Des **graphiques** (coût, CO₂, score)
   - Le **meilleur choix** pour votre usage

### **4. Générateur de Rapports**

1. Entrez les **informations de votre entreprise**
2. Saisissez les **données manuelles** (ou importez un fichier)
3. Générez :
   - Un **Rapport de Résumé** (PDF)
   - Un **Rapport CSRD** (PDF) pour la conformité

---

## 📁 Structure du Projet

```
sobre/
├── app.py                              # Interface Streamlit (400+ lignes)
├── requirements.txt                    # Dépendances Python
├── README.md                           # Documentation
├── LICENSE                             # Licence MIT
├── .gitignore                          # Fichiers à ignorer
├── config/
│   └── models.yaml                     # Configuration des modèles et SaaS
├── scripts/
│   └── sobre_calculator.py             # Ancien module (conservé pour compatibilité)
├── utils/
│   ├── __init__.py                     # Package utils
│   ├── cost_calculator.py              # Calcul des coûts (APIs + SaaS)
│   ├── carbon_calculator.py           # Calcul du CO₂
│   ├── subscription_tracker.py         # Détection des abonnements IA
│   ├── greenops_scoring.py             # Score GreenOps (A-E)
│   └── report_generator.py             # Génération de rapports PDF
└── tests/
    ├── __init__.py
    ├── test_cost_calculator.py         # Tests pour cost_calculator
    ├── test_carbon_calculator.py       # Tests pour carbon_calculator
    ├── test_subscription_tracker.py    # Tests pour subscription_tracker
    └── test_greenops_scoring.py         # Tests pour greenops_scoring
```

---

## 🔧 Configuration

### **Données des Modèles (config/models.yaml)**

Les données des modèles (coûts, CO₂) et des SaaS sont stockées dans `config/models.yaml`. Vous pouvez :

- **Ajouter un modèle API** :
  ```yaml
  models:
    Nouveau-Modèle:
      name: "Nouveau-Modèle"
      description: "Description du modèle"
      cost_per_token_input: 0.000001
      cost_per_token_output: 0.000001
      co2_per_million_tokens: 0.05
      provider: "Fournisseur"
      category: "open-source"
      saas_type: "api"
  ```

- **Ajouter un SaaS** :
  ```yaml
  saas_subscriptions:
    Nouveau-SaaS:
      name: "Nouveau-SaaS"
      description: "Description du SaaS"
      monthly_cost: 15.00
      estimated_tokens_per_month: 500000
      co2_per_month: 0.1
      provider: "Fournisseur"
      category: "saas"
      saas_type: "subscription"
  ```

- **Modifier les seuils GreenOps** :
  ```yaml
  greenops_scores:
    A:
      name: "A - Excellent"
      max_cost_per_employee: 10
      max_co2_per_employee: 50
      min_dormant_licenses: 95
  ```

### **Mots-clés pour la détection IA**

Les mots-clés pour détecter les abonnements IA sont définis dans `config/models.yaml` sous `ai_keywords`. Vous pouvez ajouter de nouveaux mots-clés pour améliorer la détection.

---

## 📊 Données et Sources

### **Coûts des Modèles (APIs)**
| Modèle | Coût (Input) | Coût (Output) | Source |
|--------|--------------|---------------|--------|
| GPT-4 | 0.03€/1k tokens | 0.06€/1k tokens | [OpenAI Pricing](https://openai.com/pricing) |
| GPT-3.5-turbo | 0.0015€/1k tokens | 0.002€/1k tokens | [OpenAI Pricing](https://openai.com/pricing) |
| Mistral-7B | 0.002€/1k tokens | 0.002€/1k tokens | [Mistral AI Pricing](https://mistral.ai/pricing/) |
| Mistral-8x7B | 0.0005€/1k tokens | 0.0005€/1k tokens | [Mistral AI Pricing](https://mistral.ai/pricing/) |
| Llama-2-70B | 0.001€/1k tokens | 0.001€/1k tokens | [AWS Bedrock](https://aws.amazon.com/bedrock/llama/) |
| Llama-3 | 0.0015€/1k tokens | 0.0015€/1k tokens | [Meta Llama](https://ai.meta.com/llama/) |

### **Coûts des SaaS**
| SaaS | Coût Mensuel | Source |
|------|--------------|--------|
| ChatGPT Plus | 20€/mois | [OpenAI](https://openai.com/pricing) |
| ChatGPT Enterprise | 40€/utilisateur/mois | [OpenAI](https://openai.com/pricing) |
| GitHub Copilot | 10€/mois | [GitHub](https://github.com/features/copilot) |
| GitHub Copilot Business | 19€/utilisateur/mois | [GitHub](https://github.com/features/copilot) |
| Notion AI | 10€/mois | [Notion](https://www.notion.so/ai) |
| Midjourney | 30€/mois | [Midjourney](https://www.midjourney.com/) |
| Canva Magic | 12.99€/mois | [Canva](https://www.canva.com/magic/) |

### **Empreinte Carbone**
| Modèle/SaaS | CO₂ par 1M tokens / mois | Source |
|-------------|----------------------------|--------|
| GPT-4 | 0.3 kg CO₂ | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) |
| GPT-3.5-turbo | 0.2 kg CO₂ | [Microsoft Sustainability Report](https://news.microsoft.com/sustainability/) |
| Mistral-7B | 0.05 kg CO₂ | [ADEME](https://www.ademe.fr/) |
| Mistral-8x7B | 0.03 kg CO₂ | [ADEME](https://www.ademe.fr/) |
| Llama-2-70B | 0.03 kg CO₂ | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) |
| Llama-3 | 0.04 kg CO₂ | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) |
| ChatGPT Plus | 0.3 kg CO₂/mois | Basé sur GPT-4 |
| GitHub Copilot | 0.15 kg CO₂/mois | [Microsoft Sustainability Report](https://news.microsoft.com/sustainability/) |

> ⚠️ **Note** : Les données CO₂ sont des **estimations moyennes** basées sur des études scientifiques. Pour des valeurs précises, consultez les rapports officiels des fournisseurs.

---

## 🏆 Score GreenOps

Le **score GreenOps** évalue la performance de votre PME en fonction de :

| Grade | Nom | Critères | Score |
|-------|-----|----------|-------|
| **A** | Excellent | Coût/employé ≤ 10€, CO₂/employé ≤ 50g, ≥ 95% licences actives | 100 |
| **B** | Bon | Coût/employé ≤ 25€, CO₂/employé ≤ 125g, ≥ 90% licences actives | 80 |
| **C** | Moyen | Coût/employé ≤ 50€, CO₂/employé ≤ 250g, ≥ 80% licences actives | 60 |
| **D** | À améliorer | Coût/employé ≤ 100€, CO₂/employé ≤ 500g, ≥ 60% licences actives | 40 |
| **E** | Critique | Coût/employé > 100€, CO₂/employé > 500g, < 60% licences actives | 20 |

---

## 💰 Modèle Économique

| Offre | Cible | Prix | Fonctionnalités |
|-------|-------|------|-----------------|
| **Freemium** | PME avec < 5 abonnements | Gratuit | Tracker Shadow AI, calculs de base |
| **Pro** | PME avec ≥ 5 abonnements | 20€/mois | Accès illimité, rapports détaillés |
| **CSRD** | Rapports de conformité | 100€/rapport | Rapport CSRD complet (PDF) |

---

## 🤝 Contribution

Les contributions sont **les bienvenues** ! Voici comment contribuer :

1. **Forker le dépôt**.
2. **Créer une branche** (`git checkout -b feature/ma-fonctionnalité`).
3. **Commiter vos changements** (`git commit -m "Ajout de ma fonctionnalité"`).
4. **Pousser vers la branche** (`git push origin feature/ma-fonctionnalité`).
5. **Ouvrir une Pull Request**.

### **Idées de Contributions**
- [ ] Ajouter plus de **modèles API** (Claude, Gemini, etc.)
- [ ] Ajouter plus de **SaaS** (Jasper, WriteSonic, Grammarly AI, etc.)
- [ ] **Intégration avec QuickBooks/Pennylane** (API officielle)
- [ ] **Import de PDF** (avec pdfplumber)
- [ ] **Tableau de bord avancé** (suivi mensuel, historique)
- [ ] **Alertes automatiques** (ex: "Votre coût a augmenté de 20%")
- [ ] **Intégration Slack/Teams** pour les notifications
- [ ] **API REST** pour une intégration facile

---

## 📜 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **Streamlit** pour son framework incroyable.
- **OpenAI**, **Mistral AI**, **Meta** pour leurs modèles.
- **La communauté open-source** pour ses contributions.
- **Pépite Clermont-Auvergne** pour son soutien aux étudiants entrepreneurs.

---

## 📞 Contact

- **Auteur** : [Aziz](https://github.com/sobre-aziz)
- **Email** : [aziz@example.com](mailto:aziz@example.com) *(à remplacer)*
- **LinkedIn** : [LinkedIn](https://linkedin.com/in/aziz) *(à remplacer)*
- **Projet** : [GitHub](https://github.com/sobre-aziz/sobre)

---

**✨ Sobre - Parce que les PME aussi méritent une IA responsable et économique.**

[![Star on GitHub](https://img.shields.io/github/stars/sobre-aziz/sobre.svg?style=social)](https://github.com/sobre-aziz/sobre/stargazers)
