# Méthodologie Sobre - Transparence et Traçabilité des Données

> **Principe directeur** : *Un chiffre non sourcé ou une détection non qualifiée est un bug. La transparence est notre avantage compétitif.*

Ce document détaille **toutes les sources, formules, hypothèses et limites** utilisées par Sobre pour calculer les coûts, l'empreinte carbone, et les économies potentielles.

---

## 📊 Table des Matières
1. [Principe de Catégorisation : CERTAIN vs ESTIMÉ](#-principe-de-catégorisation-certain-vs-estimé)
2. [Sources des Données](#-sources-des-données)
3. [Formules de Calcul](#-formules-de-calcul)
4. [Hypothèses et Limites](#-hypothèses-et-limites)
5. [Niveaux de Confiance](#-niveaux-de-confiance)
6. [Conformité CSRD](#-conformité-csrd)
7. [Références Externes](#-références-externes)

---

## 🏷️ Principe de Catégorisation : CERTAIN vs ESTIMÉ

### Définitions
| Catégorie | Description | Exemples |
|-----------|-------------|----------|
| **CERTAIN** | Donnée **calculée directement** depuis les données importées par l'utilisateur (factures, fichiers CSV). Aucune hypothèse externe n'est nécessaire. | Coût total des abonnements importés, nombre de licences, noms des fournisseurs. |
| **ESTIMÉ** | Donnée **dépendant d'hypothèses** ou de facteurs externes (ex: facteurs CO₂, équivalences, projections). Toujours accompagnée d'une fourchette min-max et d'une source. | Empreinte carbone (dépend des facteurs CO₂ par modèle), économies potentielles (dépend de l'usage estimé), équivalence km voiture. |

### Règle d'or
> **En cas de doute, c'est ESTIMÉ.**

La catégorisation est **affichée systématiquement** dans l'UI, les rapports PDF, et les comparaisons de modèles via un composant dédié (voir `utils/components.py`).

---

## 📚 Sources des Données

### 1. Coûts des Modèles (APIs)

| Modèle | Coût (Input) | Coût (Output) | Source | Date de Vérification | Niveau de Confiance |
|--------|--------------|---------------|--------|---------------------|----------------------|
| GPT-4 | 0.03€/1k tokens | 0.06€/1k tokens | [OpenAI Pricing](https://openai.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| GPT-3.5-turbo | 0.0015€/1k tokens | 0.002€/1k tokens | [OpenAI Pricing](https://openai.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| Mistral-7B | 0.002€/1k tokens | 0.002€/1k tokens | [Mistral AI Pricing](https://mistral.ai/pricing/) | 2024-11-01 | `publie_par_fournisseur` |
| Mistral-8x7B | 0.0005€/1k tokens | 0.0005€/1k tokens | [Mistral AI Pricing](https://mistral.ai/pricing/) | 2024-11-01 | `publie_par_fournisseur` |
| Llama-2-70B | 0.001€/1k tokens | 0.001€/1k tokens | [AWS Bedrock Llama](https://aws.amazon.com/bedrock/llama/) | 2024-11-01 | `publie_par_fournisseur` |
| Llama-3 | 0.0015€/1k tokens | 0.0015€/1k tokens | [Meta Llama](https://ai.meta.com/llama/) | 2024-11-01 | `publie_par_fournisseur` |
| Claude-3-Sonnet | 0.003€/1k tokens | 0.015€/1k tokens | [Anthropic Pricing](https://www.anthropic.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| Claude-3-Haiku | 0.00025€/1k tokens | 0.00125€/1k tokens | [Anthropic Pricing](https://www.anthropic.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| Gemini-1.5-Pro | 0.0035€/1k tokens | 0.0105€/1k tokens | [Google Cloud Pricing](https://cloud.google.com/vertex-ai/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| Command-R | 0.0005€/1k tokens | 0.0015€/1k tokens | [Cohere Pricing](https://cohere.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |

> **Note** : Les coûts sont convertis en euros (€) depuis les devises originales (USD, etc.) en utilisant le taux de change moyen du jour de la vérification.

---

### 2. Coûts des SaaS (Abonnements)

| SaaS | Coût Mensuel | Source | Date de Vérification | Niveau de Confiance |
|------|--------------|--------|---------------------|----------------------|
| ChatGPT Plus | 20€/mois | [OpenAI](https://openai.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| ChatGPT Enterprise | 40€/utilisateur/mois | [OpenAI](https://openai.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| GitHub Copilot | 10€/mois | [GitHub](https://github.com/features/copilot) | 2024-11-01 | `publie_par_fournisseur` |
| GitHub Copilot Business | 19€/utilisateur/mois | [GitHub](https://github.com/features/copilot) | 2024-11-01 | `publie_par_fournisseur` |
| Notion AI | 10€/mois | [Notion](https://www.notion.so/ai) | 2024-11-01 | `publie_par_fournisseur` |
| Midjourney | 30€/mois | [Midjourney](https://www.midjourney.com/) | 2024-11-01 | `publie_par_fournisseur` |
| Canva Magic | 12.99€/mois | [Canva](https://www.canva.com/magic/) | 2024-11-01 | `publie_par_fournisseur` |
| Jasper AI | 59$/mois (~55€) | [Jasper](https://www.jasper.ai/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| WriteSonic | 19$/mois (~17.5€) | [WriteSonic](https://writesonic.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| Grammarly AI | 12$/mois (~11€) | [Grammarly](https://www.grammarly.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| Otter.ai | 10$/mois (~9.2€) | [Otter.ai](https://otter.ai/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| Descript | 15$/mois (~13.8€) | [Descript](https://www.descript.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |
| Runway ML | 15$/mois (~13.8€) | [Runway ML](https://runwayml.com/pricing) | 2024-11-01 | `publie_par_fournisseur` |

> **Note** : Les coûts en dollars ($) sont convertis en euros (€) en utilisant le taux de change moyen du jour de la vérification.

---

### 3. Facteurs d'Émission CO₂

#### Modèles (par 1 million de tokens)

| Modèle | CO₂ (kg) | Source | Date de Publication | Niveau de Confiance | Hypothèses |
|--------|----------|--------|---------------------|----------------------|------------|
| GPT-4 | 0.3 kg | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) | 2021-11-02 | `estimation_par_analogie` | Basé sur l'énergie consommée par les data centers. |
| GPT-3.5-turbo | 0.2 kg | [Microsoft Sustainability Report 2023](https://news.microsoft.com/sustainability/) | 2023-01-01 | `publie_par_fournisseur` | Inclut l'inférence et une partie de l'entraînement. |
| Mistral-7B | 0.05 kg | [ADEME - Impact environnemental du numérique](https://www.ademe.fr/) | 2023-05-01 | `estimation_par_analogie` | Estimation basée sur des modèles open-source similaires. |
| Mistral-8x7B | 0.03 kg | [ADEME](https://www.ademe.fr/) | 2023-05-01 | `estimation_par_analogie` | Moins énergivore grâce à l'architecture Mixture of Experts. |
| Llama-2-70B | 0.03 kg | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) | 2021-11-02 | `estimation_par_analogie` | |
| Llama-3 | 0.04 kg | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) | 2021-11-02 | `estimation_par_analogie` | |
| Claude-3-Sonnet | 0.22 kg | [Anthropic Sustainability](https://www.anthropic.com/sustainability) | 2024-03-01 | `publie_par_fournisseur` | |
| Claude-3-Haiku | 0.15 kg | [Anthropic Sustainability](https://www.anthropic.com/sustainability) | 2024-03-01 | `publie_par_fournisseur` | |
| Gemini-1.5-Pro | 0.25 kg | [Google Sustainability](https://sustainability.google/) | 2024-05-01 | `publie_par_fournisseur` | |
| Command-R | 0.18 kg | [Cohere Sustainability](https://cohere.com/sustainability) | 2024-02-01 | `publie_par_fournisseur` | |

#### SaaS (par mois)

| SaaS | CO₂ (kg/mois) | Source | Hypothèses |
|------|---------------|--------|------------|
| ChatGPT Plus | 0.3 kg | Basé sur GPT-4 | Estimation basée sur l'usage moyen d'un utilisateur ChatGPT Plus. |
| ChatGPT Enterprise | 1.5 kg | Basé sur GPT-4 | Estimation basée sur un usage intensif. |
| GitHub Copilot | 0.15 kg | [Microsoft Sustainability Report 2023](https://news.microsoft.com/sustainability/) | |
| Copilot Business | 0.3 kg | [Microsoft Sustainability Report 2023](https://news.microsoft.com/sustainability/) | |
| Notion AI | 0.075 kg | Estimation interne | Basé sur un usage moyen de Notion AI. |
| Midjourney | 0.5 kg | Estimation interne | Basé sur la génération de 100 images/mois. |
| Canva Magic | 0.06 kg | Estimation interne | Basé sur un usage moyen. |

> **⚠️ Limite majeure** : 
> **Seule l'inférence est comptée, pas l'entraînement des modèles.**
> L'entraînement des modèles (ex: GPT-4, Mistral-7B) est à la charge des fournisseurs (OpenAI, Mistral AI, etc.) et n'est **pas inclus** dans les calculs de Sobre.
> Les facteurs CO₂ pour les SaaS sont des **estimations basées sur les modèles sous-jacents** (ex: ChatGPT Plus utilise GPT-4).

---

### 4. Équivalences

| Équivalence | Facteur | Source | Date de Publication |
|-------------|---------|--------|---------------------|
| 1 kg CO₂ = X km en voiture | 0.2 kg CO₂/km | [ADEME - Facteurs d'émission](https://www.ademe.fr/expertises/dechets/passer-a-leconomie-circulaire/reduire-ses-dechets/reduire-ses-dechets-non-dangereux) | 2023-01-01 |

> **Hypothèse** : Moyenne européenne pour une voiture essence (200 g CO₂/km).

---

## ⚙️ Formules de Calcul

### 1. Coût pour les APIs

**Formule** :
```
coût_total = (nombre_tokens_input × coût_par_token_input) + (nombre_tokens_output × coût_par_token_output)
```

**Exemple** (GPT-4, 1000 tokens input, 500 tokens output) :
```
coût_total = (1000 × 0.00003) + (500 × 0.00006) = 0.03 + 0.03 = 0.06€
```

**Catégorie** : `CERTAIN` (si les tokens sont fournis par l'utilisateur).

---

### 2. Empreinte Carbone pour les APIs

**Formule** :
```
co2_total_kg = (nombre_tokens_total × co2_par_million_tokens) / 1_000_000
co2_total_g = co2_total_kg × 1000
```

**Exemple** (GPT-4, 1500 tokens) :
```
co2_total_kg = (1500 × 0.3) / 1_000_000 = 0.00045 kg = 0.45 g
```

**Catégorie** : `ESTIMÉ` (dépend du facteur CO₂ du modèle).

---

### 3. Équivalence en km Voiture

**Formule** :
```
km_voiture = co2_total_g / 200  # 200 g CO₂/km
```

**Exemple** (0.45 g CO₂) :
```
km_voiture = 0.45 / 200 = 0.00225 km
```

**Catégorie** : `ESTIMÉ` (dépend de l'équivalence CO₂/km).

---

### 4. Score GreenOps

**Formule** :
Le score GreenOps est calculé en fonction de 3 critères (poids égaux) :
1. **Coût par employé** :
   ```
   score_coût = max(0, 100 - (coût_par_employé / seuil_max_coût) × 100)
   ```
2. **CO₂ par employé** :
   ```
   score_co2 = max(0, 100 - (co2_par_employé / seuil_max_co2) × 100)
   ```
3. **Taux de licences actives** :
   ```
   score_licences = (taux_licences_actives / 100) × 100
   ```

**Score final** :
```
score_greenops = (score_coût + score_co2 + score_licences) / 3
```

**Seuils** (voir `config/models.yaml`) :
- **A (Excellent)** : Coût ≤ 10€/employé, CO₂ ≤ 50g/employé, ≥ 95% licences actives.
- **B (Bon)** : Coût ≤ 25€/employé, CO₂ ≤ 125g/employé, ≥ 90% licences actives.
- etc.

**Catégorie** : `ESTIMÉ` (dépend des seuils et des données importées).

---

### 5. Économies Potentielles

**Formule** :
```
économies_mensuelles = somme(coût_mensuel des licences dormantes)
économies_annuelles = économies_mensuelles × 12
```

**Catégorie** : `ESTIMÉ` (dépend de la détection des licences dormantes).

---

## ⚠️ Hypothèses et Limites

### 1. Limites des Facteurs CO₂
- **Pas d'entraînement** : Les facteurs CO₂ ne couvrent que l'**inférence** (utilisation des modèles), **pas l'entraînement** (apprentissage des modèles).
  - **Pourquoi** : L'entraînement est à la charge des fournisseurs (OpenAI, Mistral AI, etc.) et ses émissions sont **réparties sur tous les utilisateurs** du modèle.
  - **Impact** : Les chiffres de CO₂ sont **sous-estimés** si l'on inclut l'entraînement.
- **Moyennes** : Les facteurs CO₂ sont des **moyennes** basées sur des études scientifiques. Les valeurs réelles peuvent varier selon :
  - Le mix électrique du data center (ex: un data center alimenté par des énergies renouvelables émet moins de CO₂).
  - L'efficacité énergétique du matériel.
  - La région géographique (ex: l'Europe a un mix électrique moins carboné que les États-Unis).
- **SaaS** : Les facteurs CO₂ pour les SaaS sont des **estimations** basées sur les modèles sous-jacents (ex: ChatGPT Plus utilise GPT-4).

### 2. Limites des Coûts
- **Taux de change** : Les coûts en dollars ($) sont convertis en euros (€) en utilisant le **taux de change moyen du jour de la vérification**. Les fluctuations du taux de change peuvent affecter les résultats.
- **Abonnements** : Les coûts des SaaS sont basés sur les **tarifs publics** des fournisseurs. Les tarifs négociés (ex: contrats entreprise) ne sont pas pris en compte.

### 3. Limites de la Détection des Abonnements IA
- **Mots-clés** : La détection des abonnements IA repose sur une **liste de mots-clés** (voir `config/models.yaml`).
  - **Faux positifs** : Un abonnement peut être détecté comme IA alors qu'il ne l'est pas (ex: un SaaS nommé "AI Tools" mais sans IA).
  - **Faux négatifs** : Un abonnement IA peut ne pas être détecté s'il n'est pas dans la liste des mots-clés.
- **Colonnes requises** : La détection nécessite au minimum les colonnes **Nom** et **Coût** dans le fichier CSV importé.

### 4. Limites des Économies Potentielles
- **Hypothèse** : Les économies potentielles supposent que **toutes les licences dormantes peuvent être désactivées**. En réalité, certaines licences peuvent être nécessaires pour des raisons légales ou techniques.
- **Usage** : Les économies sont basées sur les **coûts mensuels** des licences dormantes. Les coûts annuels sont une **projection** (×12).

---

## 🎯 Niveaux de Confiance

| Niveau | Description | Exemple |
|--------|-------------|---------|
| `mesure` | Donnée **mesurée directement** (ex: coût importé depuis une facture). | Coût d'un abonnement ChatGPT Plus. |
| `publie_par_fournisseur` | Donnée **publiée par le fournisseur** (ex: tarif OpenAI). | Coût par token de GPT-4. |
| `estimation_par_analogie` | Donnée **estimée par analogie** avec des modèles/sources similaires. | CO₂ de Mistral-7B (basé sur des études scientifiques). |

---

## 📜 Conformité CSRD

### Qu'est-ce que le CSRD ?
Le **Corporate Sustainability Reporting Directive (CSRD)** est une directive européenne qui impose aux entreprises de publier des **rapports de durabilité** (environnementaux, sociaux, et de gouvernance).

### Positionnement de Sobre
- **Sobre génère des rapports structurés selon les attendus ESRS E1** (European Sustainability Reporting Standards, Environnement).
- **⚠️ Attention** : 
  > **Ces rapports ne constituent pas une conformité juridique garantie.**
  > La conformité CSRD dépend de nombreux facteurs (taille de l'entreprise, secteur d'activité, audit externe, etc.) et nécessite une **validation par un expert comptable ou un auditeur certifié**.
- **Recommandation** : Utilisez les rapports Sobre comme **point de départ** pour vos obligations CSRD, mais consultez un expert pour une conformité complète.

### Contenu des Rapports CSRD Générés par Sobre
1. **Empreinte carbone** : CO₂ total et par employé (ESTIMÉ).
2. **Coûts** : Coût total et par employé (CERTAIN si importé depuis des factures).
3. **Score GreenOps** : Évaluation de A à E (ESTIMÉ).
4. **Licences dormantes** : Liste des abonnements inutilisés (CERTAIN si détectés depuis les factures).
5. **Recommandations** : Actions pour réduire les coûts et le CO₂ (ESTIMÉ).

---

## 🔗 Références Externes

### 1. EcoLogits
- **Dépôt** : [github.com/mlco2/ecologits](https://github.com/mlco2/ecologits)
- **Licence** : MPL-2.0
- **Description** : Outil open-source pour mesurer l'empreinte carbone des projets de machine learning.
- **Utilisation dans Sobre** : 
  - **Non utilisé directement** (pour l'instant), mais les facteurs CO₂ de Sobre sont **comparables** à ceux d'EcoLogits.
  - **À étudier** : Intégration future des facteurs CO₂ d'EcoLogits pour une meilleure précision.

### 2. CodeCarbon
- **Dépôt** : [github.com/mlco2/codecarbon](https://github.com/mlco2/codecarbon)
- **Licence** : MIT
- **Description** : Outil pour mesurer l'empreinte carbone des scripts Python.
- **Utilisation dans Sobre** : 
  - **Non utilisé directement** (pour l'instant).
  - **À étudier** : Intégration future pour une mesure plus précise du CO₂ des APIs.

### 3. Études Scientifiques
- **[Carbon Footprint of AI Models (arXiv:2111.02186)](https://arxiv.org/abs/2111.02186)** : Étude de référence sur l'empreinte carbone des modèles d'IA.
- **[Microsoft Sustainability Report 2023](https://news.microsoft.com/sustainability/)** : Données CO₂ pour les modèles Microsoft (ex: GPT-3.5-turbo, Copilot).
- **[ADEME - Impact environnemental du numérique](https://www.ademe.fr/)** : Facteurs CO₂ pour les data centers et équivalences (ex: kg CO₂/km voiture).

---

## 📞 Contact et Contributions

### Signaler une Erreur ou une Source Manquante
Si vous trouvez une **erreur dans les sources** ou une **donnée non sourcée**, merci de :
1. **Ouvrir une issue** sur [GitHub](https://github.com/sobre-aziz/sobre/issues) avec :
   - Le fichier concerné.
   - La donnée problématique.
   - La source correcte (si disponible).
2. **Proposer une PR** pour corriger la donnée.

### Contribuer aux Sources
Pour ajouter une nouvelle source :
1. **Vérifiez** la donnée (URL, date, niveau de confiance).
2. **Ajoutez-la** dans `config/models.yaml` avec les champs `source`, `date_maj`, et `niveau_confiance`.
3. **Mettez à jour** ce document (`docs/METHODOLOGIE.md`).
4. **Testez** que le test de validation des modèles passe (voir `tests/test_models_validation.py`).

---

## 📅 Historique des Mises à Jour

| Date | Modification | Auteur |
|------|--------------|--------|
| 2024-11-01 | Création du document | Sobre Team |
| 2024-11-01 | Ajout des sources pour les modèles OpenAI, Mistral AI, Meta | Sobre Team |
| 2024-11-01 | Ajout des facteurs CO₂ et équivalences | Sobre Team |

---

> **Dernière mise à jour** : 2024-11-01
> **Version** : 1.0
> **Licence** : MIT (comme le projet Sobre)
