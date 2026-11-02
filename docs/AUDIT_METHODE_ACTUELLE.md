# Audit de la Méthode Actuelle de Sobre

> **Objectif** : Identifier toutes les **incohérences, sources invérifiables, et limites** de la méthode actuelle pour préparer une refonte défendable devant un jury, un client ou un expert.

> **Règle absolue** : *Un chiffre non sourcé ou une détection non qualifiée est un bug. Si une source ne peut pas être vérifiée, elle doit être marquée comme "à vérifier" et ne jamais s'afficher comme un fait dans l'interface.*

---

## 📋 Table des Matières
1. [Inventaire des Formules, Facteurs et Sources](#1-inventaire-des-formules-facteurs-et-sources)
2. [Incohérences Identifiées](#2-incohérences-identifiées)
3. [Problèmes par Catégorie](#3-problèmes-par-catégorie)
4. [Recommandations pour la Refonte](#4-recommandations-pour-la-refonte)

---

## 1. Inventaire des Formules, Facteurs et Sources

### 1.1 Coûts

#### APIs (Modèles IA)
| **Modèle**         | **Formule** | **Coût (Input)** | **Coût (Output)** | **Source** | **Statut** | **Problèmes** |
|--------------------|-------------|------------------|-------------------|------------|------------|---------------|
| GPT-4              | `coût_total = (tokens_input × coût_input) + (tokens_output × coût_output)` | 0.03€/1k tokens | 0.06€/1k tokens | [OpenAI Pricing](https://openai.com/pricing) | ❌ À vérifier | URL générique (page d'accueil) |
| GPT-3.5-turbo      | Idem | 0.0015€/1k tokens | 0.002€/1k tokens | [OpenAI Pricing](https://openai.com/pricing) | ❌ À vérifier | URL générique |
| Mistral-7B         | Idem | 0.002€/1k tokens | 0.002€/1k tokens | [Mistral AI Pricing](https://mistral.ai/pricing/) | ❌ À vérifier | URL générique |
| Llama-2-70B        | Idem | 0.001€/1k tokens | 0.001€/1k tokens | [AWS Bedrock Llama](https://aws.amazon.com/bedrock/llama/) | ❌ À vérifier | URL générique |
| Llama-3            | Idem | 0.0015€/1k tokens | 0.0015€/1k tokens | [Meta Llama](https://ai.meta.com/llama/) | ❌ À vérifier | URL générique |
| Claude-3-Sonnet    | Idem | 0.003€/1k tokens | 0.015€/1k tokens | [Anthropic Pricing](https://www.anthropic.com/pricing) | ❌ À vérifier | URL générique |
| Claude-3-Haiku     | Idem | 0.00025€/1k tokens | 0.00125€/1k tokens | [Anthropic Pricing](https://www.anthropic.com/pricing) | ❌ À vérifier | URL générique |
| Gemini-1.5-Pro     | Idem | 0.0035€/1k tokens | 0.0105€/1k tokens | [Google Cloud Pricing](https://cloud.google.com/vertex-ai/pricing) | ❌ À vérifier | URL générique |
| Command-R          | Idem | 0.0005€/1k tokens | 0.0015€/1k tokens | [Cohere Pricing](https://cohere.com/pricing) | ❌ À vérifier | URL générique |

**Problèmes communs** :
- Toutes les URLs pointent vers des **pages d'accueil** (pas de page spécifique avec les tarifs).
- Les coûts sont **affichés en €** mais les sources sont en **$** (ex: Llama-3 = 0.0015$/1k tokens).
- **Aucune source pour le taux de change** ($ → €).

---

#### SaaS (Abonnements)
| **SaaS** | **Coût Mensuel** | **Source** | **Statut** | **Problèmes** |
|----------|------------------|------------|------------|---------------|
| ChatGPT Plus | 20€/mois | [OpenAI](https://openai.com/pricing) | ❌ À vérifier | URL générique |
| ChatGPT Enterprise | 40€/utilisateur/mois | [OpenAI](https://openai.com/pricing) | ❌ À vérifier | URL générique |
| GitHub Copilot | 10€/mois | [GitHub](https://github.com/features/copilot) | ❌ À vérifier | URL générique |
| GitHub Copilot Business | 19€/utilisateur/mois | [GitHub](https://github.com/features/copilot) | ❌ À vérifier | URL générique |
| Notion AI | 10€/mois | [Notion](https://www.notion.so/ai) | ❌ À vérifier | URL générique |
| Midjourney | 30€/mois | [Midjourney](https://www.midjourney.com/) | ❌ À vérifier | URL générique |
| Canva Magic | 12.99€/mois | [Canva](https://www.canva.com/magic/) | ❌ À vérifier | URL générique |
| Jasper AI | 59$/mois (~55€) | [Jasper](https://www.jasper.ai/pricing) | ❌ À vérifier | URL générique + conversion $ → € non sourcée |
| WriteSonic | 19$/mois (~17.5€) | [WriteSonic](https://writesonic.com/pricing) | ❌ À vérifier | URL générique + conversion $ → € non sourcée |
| Grammarly AI | 12$/mois (~11€) | [Grammarly](https://www.grammarly.com/pricing) | ❌ À vérifier | URL générique + conversion $ → € non sourcée |
| Otter.ai | 10$/mois (~9.2€) | [Otter.ai](https://otter.ai/pricing) | ❌ À vérifier | URL générique + conversion $ → € non sourcée |
| Descript | 15$/mois (~13.8€) | [Descript](https://www.descript.com/pricing) | ❌ À vérifier | URL générique + conversion $ → € non sourcée |
| Runway ML | 15$/mois (~13.8€) | [Runway ML](https://runwayml.com/pricing) | ❌ À vérifier | URL générique + conversion $ → € non sourcée |

**Problèmes communs** :
- Toutes les URLs pointent vers des **pages d'accueil** (pas de page spécifique avec les tarifs).
- Les coûts en **$** sont convertis en **€** sans **source pour le taux de change**.

---

### 1.2 Facteurs d'Émission CO₂

#### Modèles (par 1 million de tokens)
| **Modèle** | **CO₂ (kg/1M tokens)** | **Source** | **Date de Publication** | **Statut** | **Problèmes** |
|------------|------------------------|------------|-------------------------|------------|---------------|
| GPT-4 | 0.3 | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) | 2021-11-02 | ❌ À vérifier | **Hors sujet** : L'article traite de l'edge computing pour véhicules, pas des LLM. |
| GPT-3.5-turbo | 0.2 | [Microsoft Sustainability Report 2023](https://news.microsoft.com/sustainability/) | 2023-01-01 | ❌ À vérifier | URL générique (page d'accueil) |
| Mistral-7B | 0.05 | [ADEME - Impact environnemental du numérique](https://www.ademe.fr/) | 2023-05-01 | ❌ À vérifier | URL générique (page d'accueil) |
| Mistral-8x7B | 0.03 | [ADEME](https://www.ademe.fr/) | 2023-05-01 | ❌ À vérifier | URL générique |
| Llama-2-70B | 0.03 | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) | 2021-11-02 | ❌ À vérifier | **Hors sujet** |
| Llama-3 | 0.04 | [arXiv:2111.02186](https://arxiv.org/abs/2111.02186) | 2021-11-02 | ❌ À vérifier | **Hors sujet** |
| Claude-3-Sonnet | 0.22 | [Anthropic Sustainability](https://www.anthropic.com/sustainability) | 2024-03-01 | ❌ À vérifier | URL générique |
| Claude-3-Haiku | 0.15 | [Anthropic Sustainability](https://www.anthropic.com/sustainability) | 2024-03-01 | ❌ À vérifier | URL générique |
| Gemini-1.5-Pro | 0.25 | [Google Sustainability](https://sustainability.google/) | 2024-05-01 | ❌ À vérifier | URL générique |
| Command-R | 0.18 | [Cohere Sustainability](https://cohere.com/sustainability) | 2024-02-01 | ❌ À vérifier | URL générique |

**Problèmes communs** :
- **Toutes les URLs pointent vers des pages d'accueil** (pas de document spécifique).
- **arXiv:2111.02186 est hors sujet** (edge computing pour véhicules, pas LLM).
- **Aucune justification** pour les valeurs choisies (ex: pourquoi Mistral-7B = 0.05 kg et pas 0.1 kg ?).

---

#### SaaS (par mois)
| **SaaS** | **CO₂ (kg/mois)** | **Source** | **Statut** | **Problèmes** |
|----------|-------------------|------------|------------|---------------|
| ChatGPT Plus | 0.3 | Basé sur GPT-4 (non sourcé) | ❌ À vérifier | **Aucune source directe**. Hypothèse non justifiée. |
| ChatGPT Enterprise | 1.5 | Basé sur GPT-4 (non sourcé) | ❌ À vérifier | **Aucune source directe**. Hypothèse non justifiée. |
| GitHub Copilot | 0.15 | [Microsoft Sustainability Report 2023](https://news.microsoft.com/sustainability/) | ❌ À vérifier | URL générique. **Aucune justification** de la valeur. |
| Copilot Business | 0.3 | [Microsoft Sustainability Report 2023](https://news.microsoft.com/sustainability/) | ❌ À vérifier | URL générique |
| Notion AI | 0.075 | Estimation interne (non sourcée) | ❌ À vérifier | **Aucune source**. |
| Midjourney | 0.5 | Estimation interne (non sourcée) | ❌ À vérifier | **Aucune source**. |
| Canva Magic | 0.06 | Estimation interne (non sourcée) | ❌ À vérifier | **Aucune source**. |

**Problèmes communs** :
- **Aucune source directe** pour les valeurs CO₂ des SaaS.
- Les valeurs sont **basées sur des hypothèses non documentées** (ex: "basé sur GPT-4").
- **Aucune hypothèse d'usage** (nombre de tokens/mois, temps d'utilisation).

---

### 1.3 Équivalences

| **Équivalence** | **Valeur** | **Source** | **Statut** | **Problèmes** |
|----------------|------------|------------|------------|---------------|
| 1 kg CO₂ = X km voiture | 0.2 kg CO₂/km | [ADEME - Facteurs d'émission](https://www.ademe.fr/) | ❌ À vérifier | URL générique. **Aucune précision** sur le type de voiture (essence/diesel) ou le périmètre (fabrication + usage). |

**Problèmes** :
- **Aucune source précise** (page d'accueil ADEME).
- **Aucune justification** pour la valeur 0.2 kg CO₂/km.

---

### 1.4 Score GreenOps

#### Formules
| **Critère** | **Formule** | **Source** | **Statut** | **Problèmes** |
|-------------|-------------|------------|------------|---------------|
| Score Coût | `score_coût = max(0, 100 - (coût_par_employé / seuil_max_coût) × 100)` | Interne | ❌ À vérifier | **`seuil_max_coût` non défini** dans le code ou la documentation. |
| Score CO₂ | `score_co2 = max(0, 100 - (co2_par_employé / seuil_max_co2) × 100)` | Interne | ❌ À vérifier | **`seuil_max_co2` non défini**. |
| Score Licences Actives | `score_licences = (taux_licences_actives / 100) × 100` | Interne | ❌ À vérifier | **Aucune méthode de détection** des licences actives. |
| Score Final | `score_greenops = (score_coût + score_co2 + score_licences) / 3` | Interne | ❌ À vérifier | **Règle de passage de la moyenne à la lettre (A-E) non définie**. |

#### Seuils (A-E)
| **Grade** | **Coût/employé** | **CO₂/employé** | **Licences actives** | **Statut** | **Problèmes** |
|-----------|------------------|------------------|-----------------------|------------|---------------|
| A (Excellent) | ≤ 10€ | ≤ 50 g | ≥ 95% | ❌ À vérifier | **Incohérent** : 1 abonnement ChatGPT Plus (20€) dépasse déjà le seuil A pour 1 employé. |
| B (Bon) | ≤ 25€ | ≤ 125 g | ≥ 90% | ❌ À vérifier | **Incohérent** : 1 ChatGPT Plus (20€) + 1 Copilot (10€) = 30€ > 25€ pour 1 employé. |
| C (Moyen) | ≤ 50€ | ≤ 250 g | ≥ 80% | ❌ À vérifier | **Incohérent** : 1 Midjourney (30€) + 1 ChatGPT Plus (20€) = 50€ = seuil C pour 1 employé. |
| D (À améliorer) | ≤ 100€ | ≤ 500 g | ≥ 60% | ❌ À vérifier | |
| E (Critique) | > 100€ | > 500 g | < 60% | ❌ À vérifier | |

**Problèmes** :
- **`seuil_max_coût` et `seuil_max_co2` ne sont pas définis** dans le code ou la documentation.
- **Règle de passage de la moyenne à la lettre (A-E) non définie**.
- **Seuils incohérents** avec les valeurs réelles (ex: 1 ChatGPT Plus = 20€ > seuil A = 10€ pour 1 employé).

---

### 1.5 Économies Potentielles

| **Donnée** | **Formule** | **Source** | **Statut** | **Problèmes** |
|------------|-------------|------------|------------|---------------|
| Économies mensuelles | `somme(coût_mensuel des licences dormantes)` | Interne | ❌ À vérifier | **Aucune méthode de détection** des licences dormantes. |
| Économies annuelles | `économies_mensuelles × 12` | Interne | ❌ À vérifier | **Hypothèse de ×12 aveugle** (ne tient pas compte des abonnements annuels ou des chevauchements). |

**Problèmes** :
- **Aucune méthode de détection** des licences dormantes (pas de colonne "dernière utilisation").
- **×12 aveugle** pour les économies annuelles (ne tient pas compte des abonnements annuels).

---

### 1.6 Détection des Abonnements IA

| **Donnée** | **Méthode** | **Source** | **Statut** | **Problèmes** |
|------------|-------------|------------|------------|---------------|
| Détection par mots-clés | Recherche de sous-chaînes (ex: "IA", "AI", "GPT", "Copilot") | Interne | ❌ À vérifier | **Faux positifs** : "Mailchimp", "Airtable", "Gmail" contiennent "AI" ou "mail". |
| Mots-clés | Liste dans `config/models.yaml` (`ai_keywords`) | Interne | ❌ À vérifier | **Pas de score de confiance** pour chaque détection. |
| Correction manuelle | Non implémentée | - | ❌ À vérifier | **Aucune possibilité de correction** des faux positifs/négatifs. |

**Problèmes** :
- **Faux positifs** : La détection utilise `if keyword in name` (recherche de sous-chaîne), ce qui génère des erreurs.
- **Aucun score de confiance** pour chaque détection.
- **Aucune correction manuelle** possible.

---

## 2. Incohérences Identifiées

### 2.1 Incohérences dans les Seuils du Score GreenOps
- **Problème** : Les seuils du score GreenOps sont **incompatibles avec les valeurs réelles**.
  - **Exemple 1** : Un seul abonnement **ChatGPT Plus (20€/mois)** dépasse déjà le seuil **A (≤ 10€/employé)** pour une PME de 1 employé.
  - **Exemple 2** : **1 ChatGPT Plus (20€) + 1 Copilot (10€) = 30€** > seuil **B (≤ 25€/employé)** pour 1 employé.
  - **Exemple 3** : **1 ChatGPT Plus (0.3 kg CO₂/mois = 300 g)** dépasse déjà le seuil **A (≤ 50 g/employé)** pour 1 employé.
- **Impact** : **Aucune PME avec ≥1 abonnement IA ne peut obtenir un score A ou B** avec les seuils actuels.

---

### 2.2 CO₂ Fixe par SaaS sans Hypothèse d'Usage
- **Problème** : Les valeurs CO₂ pour les SaaS (ex: ChatGPT Plus = 0.3 kg/mois) sont **fixes et non justifiées**.
  - **Aucune hypothèse** sur :
    - Le nombre de tokens/mois.
    - Le temps d'utilisation.
    - Le modèle sous-jacent (ex: ChatGPT Plus utilise GPT-4, mais combien de tokens par mois ?).
  - **Exemple** : Pourquoi ChatGPT Plus = 0.3 kg/mois et pas 0.1 kg ou 1 kg ?

---

### 2.3 `seuil_max` Non Définis
- **Problème** : Les formules du score GreenOps utilisent `seuil_max_coût` et `seuil_max_co2`, mais ces variables **ne sont pas définies** dans le code ou la documentation.
  - **Où sont-elles stockées ?** → **Nulle part**.
  - **Comment sont-elles calculées ?** → **Non documenté**.

---

### 2.4 Pas de Règle pour Passer de la Moyenne à la Lettre (A-E)
- **Problème** : La formule `score_greenops = (score_coût + score_co2 + score_licences) / 3` donne une **moyenne entre 0 et 100**, mais **aucune règle** n'explique comment cette moyenne est convertie en lettre (A-E).
  - **Exemple** : Une moyenne de 80 → **B** ? **A** ? **Non défini**.

---

### 2.5 Critère "Licences Actives" sans Méthode de Détection
- **Problème** : Le score GreenOps utilise un critère **"taux de licences actives"**, mais **aucune méthode** n'existe pour détecter si une licence est active ou non.
  - **Aucune colonne** "dernière utilisation" dans les données importées.
  - **Aucune intégration** avec des outils de monitoring (ex: API des fournisseurs).

---

### 2.6 Unité de Temps Non Précisée
- **Problème** : Les calculs mélangent des **unités de temps différentes** sans précision :
  - Coûts : **mensuels** (ex: 20€/mois pour ChatGPT Plus).
  - CO₂ : **par million de tokens** (ex: 0.3 kg/1M tokens) **ou par mois** (ex: 0.3 kg/mois pour ChatGPT Plus).
  - Économies : **mensuelles** ou **annuelles** (×12 aveugle).

---

### 2.7 Devise Non Cohérente
- **Problème** : Les coûts des modèles sont **publiés en $** (ex: Llama-3 = 0.0015$/1k tokens), mais **affichés en €** dans Sobre.
  - **Aucune source** pour le taux de change utilisé.
  - **Aucune date** pour le taux de change.
  - **Exemple** : Llama-3 = 0.0015$/1k tokens → **0.0015€/1k tokens** (taux 1:1 ?).

---

### 2.8 Détection par Mots-Clés en Sous-Chaîne
- **Problème** : La détection utilise `if keyword in name` (recherche de sous-chaîne), ce qui génère des **faux positifs** :
  - **"Mailchimp"** → détecté comme IA (contient "mail").
  - **"Airtable"** → détecté comme IA (contient "AI").
  - **"Gmail"** → détecté comme IA (contient "mail").
  - **"Adobe"** → détecté comme IA (si "AI" est dans la liste).

---

## 3. Problèmes par Catégorie

| **Catégorie** | **Nombre de Problèmes** | **Exemples** |
|---------------|-------------------------|--------------|
| **Sources invérifiables** | 20+ | arXiv:2111.02186 (hors sujet), URLs génériques (Microsoft, ADEME, Google, etc.). |
| **Incohérences** | 7 | Seuils GreenOps, CO₂ fixe par SaaS, `seuil_max` non défini, etc. |
| **Manque de transparence** | 5+ | Pas de méthode pour les licences actives, pas de règle A-E, unité de temps non précisée. |
| **Faux positifs** | 1 | Détection par sous-chaîne ("AI" dans "Airtable", "Gmail"). |
| **Devises** | 1 | Conversion $ → € sans source ou date. |

---

## 4. Recommandations pour la Refonte

### 4.1 Priorités
1. **Corriger les sources invérifiables** :
   - Remplacer les URLs génériques par des **liens directs** vers les documents sources.
   - Supprimer **arXiv:2111.02186** (hors sujet) et trouver des alternatives.
   - Ajouter des **champs de traçabilité** (titre du document, auteur, date de consultation, périmètre).

2. **Définir les seuils et règles du Score GreenOps** :
   - Définir **`seuil_max_coût` et `seuil_max_co2`** dans `config/models.yaml`.
   - Définir la **règle de passage de la moyenne à la lettre (A-E)**.
   - **Recalculer les seuils** pour qu'ils soient cohérents avec les valeurs réelles.

3. **Abandonner les valeurs CO₂ fixes pour les SaaS** :
   - Utiliser des **hypothèses d'usage** (faible/moyen/fort) × facteur CO₂ du modèle sous-jacent.
   - Si le modèle sous-jacent est inconnu, afficher **"non estimable"**.

4. **Améliorer la détection des abonnements IA** :
   - Utiliser des **mots entiers** (pas de sous-chaîne) avec des **frontières de mots**.
   - Ajouter un **score de confiance** pour chaque détection.
   - Permettre une **correction manuelle**.

5. **Gérer les devises et unités de temps** :
   - **Afficher la devise d'origine** (ex: 0.0015$/1k tokens) + conversion en € avec **source et date du taux de change**.
   - **Préciser l'unité de temps** pour chaque calcul (mensuel, annuel, par token).

6. **Documenter les hypothèses** :
   - **Périmètre** : Inclure ou exclure l'entraînement, la fabrication, etc.
   - **Location-based vs Market-based** : Choisir une approche par défaut et l'expliquer.
   - **Limites** : Lister toutes les limites (ex: "seule l'inférence est comptée").

---

### 4.2 Prochaines Étapes
1. **Valider les sources actuelles** :
   - Vérifier si les URLs génériques (Microsoft, ADEME, etc.) pointent vers des documents spécifiques.
   - Trouver des **alternatives** pour les sources hors sujet (ex: arXiv:2111.02186).

2. **Créer `docs/BENCHMARK_METHODES.md`** :
   - Lire les documents originaux (EcoLogits, Jegham et al., CodeCarbon, Maijin).
   - Créer un **tableau comparatif** des méthodes de référence.
   - Identifier **ce que Sobre doit adopter** (et pourquoi).

3. **Refondre `config/models.yaml`** :
   - Ajouter des **champs de traçabilité** pour chaque facteur (source, date, périmètre, statut).
   - Séparer les **coûts** (en $ et €) et les **facteurs CO₂** (avec fourchettes min/central/max).

4. **Créer `config/sources.yaml`** :
   - Un enregistrement par facteur avec :
     - **Titre exact du document**.
     - **Auteur/organisme**.
     - **URL précise** (pas une page d'accueil).
     - **Page ou section**.
     - **Date de consultation**.
     - **Périmètre** (ex: "inférence seulement").
     - **Statut** : "vérifié" ou "à vérifier".

5. **Mettre à jour le code** :
   - Implémenter les **nouveaux calculs** (coûts, CO₂, score, économies, détection).
   - Ajouter des **tests** pour valider les calculs.

---

## 5. Résumé des Actions à Valider

| **Action** | **Statut** | **Décision Requise** |
|------------|------------|-----------------------|
| Corriger les sources invérifiables | ⏳ En attente | Dois-je chercher les pages exactes ou marquer tout comme "à vérifier" ? |
| Supprimer arXiv:2111.02186 | ⏳ En attente | Confirmez-vous que ce papier est hors sujet ? |
| Trouver des alternatives pour ADEME | ⏳ En attente | Dois-je trouver le rapport spécifique ou utiliser la Base Empreinte ? |
| Lire les documents originaux (EcoLogits, etc.) | ⏳ En attente | Dois-je lire les documents originaux ou me baser sur les résumés ? |
| Créer `docs/BENCHMARK_METHODES.md` | ⏳ En attente | Attendez ma validation. |
| Refondre `config/models.yaml` | ⏳ En attente | Attendez ma validation. |
| Mettre à jour le code | ⏳ En attente | Attendez ma validation. |

---

> **Règle absolue** : *Aucune source non vérifiée ne doit s'afficher dans l'interface comme un fait. Si une source ne peut pas être vérifiée, elle doit être marquée comme "à vérifier" et ne jamais être utilisée pour des calculs affichés comme certains.*
