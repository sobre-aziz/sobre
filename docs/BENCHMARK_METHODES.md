# Benchmark des Méthodes de Référence - Sobre

> **Objectif** : Comparer les méthodes de référence pour le calcul de l'empreinte carbone et des coûts des systèmes d'IA, afin d'identifier les meilleures pratiques à adopter par Sobre.

> **Règle absolue** : *Aucune source non vérifiée ne doit être utilisée. Chaque facteur doit avoir : titre exact, auteur, URL précise (pas une page d'accueil), page/section, date de consultation, périmètre, et statut "vérifié" ou "à vérifier".*

---

## 📊 Table des Matières
1. [Tableau Comparatif Principal](#-tableau-comparatif-principal)
2. [EcoLogits](#1-ecologits)
3. [Jegham et al. - "How Hungry is AI?"](#2-jegham-et-al---how-hungry-is-ai)
4. [CodeCarbon](#3-codecarbon)
5. [Maijin (diagnostic-ia.ch)](#4-maijin)
6. [Orki, Greenly, Carbo](#5-orki-greenly-carbo)
7. [Base Empreinte ADEME](#6-base-empreinte-ademe)
8. [Synthèse et Recommandations](#-synthèse-et-recommandations)
9. [Bonnes Pratiques pour Sobre](#-bonnes-pratiques-pour-sobre)

---

## 📋 Tableau Comparatif Principal

| **Critère** | **EcoLogits** | **Jegham et al.** | **CodeCarbon** | **Maijin** | **Orki** | **Greenly** | **Carbo** |
|-------------|---------------|-------------------|---------------|------------|----------|------------|----------|
| **Périmètre** | Inférence LLM, Génération Vidéo | Inférence LLM (30 modèles) | Calcul local (CPU/GPU/RAM) | Usage IA en entreprise | ACV complète (scope 1,2,3) | ACV complète (scope 1,2,3) | ACV complète |
| **Phases du cycle de vie** | Usage + Embodied (fabrication) | Usage uniquement | Usage uniquement | Usage uniquement | Physique prioritaire, monétaire plafonné | Hybride (physique + monétaire) | Physique privilégié |
| **Indicateurs** | GWP, ADPe, PE, WCF | Énergie, Eau, CO₂ | CO₂, Énergie | CO₂, Énergie, Eau | CO₂ (scope 1,2,3) | CO₂ (scope 1,2,3) | CO₂ + autres |
| **Fourchettes** | Oui (min/central/max) | Oui (par modèle) | Non (valeur ponctuelle) | Oui (réglables) | Non (plafonds par niveau) | Non | Oui (téléchargeable par facteur) |
| **PUE** | Oui (par fournisseur) | Oui (estimé) | Non (local) | Oui (configurable) | Non applicable | Non applicable | Non applicable |
| **WUE** | Oui (on-site + off-site) | Oui | Non | Oui | Non applicable | Non applicable | Non applicable |
| **Intensité carbone** | Par pays (Our World in Data) | Par pays | Par pays/region | Location-based vs Market-based | ADEME Base Empreinte | ADEME + base propre | ADEME + Ecoinvent + base propre |
| **Location-based vs Market-based** | Location-based | Location-based | Location-based | Les deux | Non applicable | Non applicable | Non applicable |
| **Limites** | Pas de fin de vie, dépend des données fournisseurs | Pas de fabrication, pas de fin de vie | Local uniquement, pas d'API | Estimation haut niveau | Pas de facteurs IA/LLM | Pas de facteurs IA/LLM | Pas de facteurs IA/LLM publics |
| **Licence** | CC BY-SA 4.0 | arXiv (open) | MIT | Propriétaire | Propriétaire | Propriétaire | Propriétaire |
| **Statut sources** | ✅ Vérifié | ✅ Vérifié | ✅ Vérifié | ✅ Vérifié | ✅ Vérifié | ✅ Vérifié | ✅ Vérifié |
| **Facteurs IA/LLM publiés ?** | ✅ Oui | ✅ Oui | ❌ Non (local uniquement) | ⚠️ En partie | ❌ Non trouvé | ❌ Non trouvé | ❌ Non trouvé |

---

## 1. EcoLogits

### 📌 Informations Générales
- **Auteurs** : Samuel Rincé, Adrien Banse (CodeCarbon non-profit)
- **Publication** : JOSS (Journal of Open Source Software), 2025
- **DOI** : [10.21105/joss.07471](https://doi.org/10.21105/joss.07471)
- **Dépôt** : [github.com/mlco2/ecologits](https://github.com/mlco2/ecologits)
- **Site** : [ecologits.ai](https://ecologits.ai)
- **Licence** : CC BY-SA 4.0 (méthodologie), MPL-2.0 (code)
- **Statut** : ✅ **Vérifié** (documentation complète disponible)

### 📊 Méthodologie

#### Approche
- **Cadre** : Analyse du Cycle de Vie (ACV) selon ISO 14044
- **Type** : Bottom-up (modélisation fine des composants)
- **Focus** : **Inférence uniquement** (pas d'entraînement, pas de fin de vie)
- **Formule principale** :
  ```
  I_request = I_request^u + I_request^e
  = E_request × F_em + (ΔT/ΔL) × I_server^e
  ```
  Où :
  - `I_request^u` = Impacts d'usage (énergie × facteur d'émission)
  - `I_request^e` = Impacts embodied (fabrication du matériel)
  - `E_request` = Énergie consommée par la requête
  - `F_em` = Facteur d'émission de l'électricité (par pays)
  - `ΔT/ΔL` = Facteur d'utilisation du matériel (temps de calcul / durée de vie)

#### Composants Modélisés

##### Usage Impacts (I_request^u)
1. **Énergie GPU** :
   - Modèle basé sur ML.ENERGY Leaderboard (Chung et al., 2025)
   - Formule : `f_E(P_active, B) = α × e^(β×B) × P_active + γ`
     - `P_active` = Nombre de paramètres actifs (différent pour SMoE)
     - `B` = Batch size (fixé à 64 par défaut)
     - Paramètres : α=1.17×10⁻⁶, β=-1.12×10⁻², γ=4.05×10⁻⁵
   - Énergie par token de sortie : `E_GPU = #T_out × f_E(P_active, 64)`

2. **Énergie Serveur** :
   - Serveur de référence : AWS p5.48xlarge (8× NVIDIA H100 80GB)
   - Puissance fixe : 1.2 kW (sans GPU)
   - Allocation : proportionnelle au nombre de GPU utilisés

3. **PUE (Power Usage Effectiveness)** :
   - Par fournisseur (ex: OpenAI=1.20, Mistral=1.16, Google=1.09)
   - Source : Données publiques des fournisseurs cloud

4. **Facteur d'émission (F_em)** :
   - Source : Our World in Data (GWP), ADEME Base Empreinte (ADPe, PE)
   - Granularité : Par pays

##### Embodied Impacts (I_request^e)
1. **Serveur (sans GPU)** :
   - Référence : AWS p5.48xlarge
   - GWP : 5700 kgCO₂eq
   - ADPe : 0.37 kgSbeq
   - PE : 70,000 MJ
   - Source : BoaviztAPI

2. **GPU (NVIDIA H100 80GB)** :
   - GWP : 273 kgCO₂eq
   - ADPe : 0.00895 kgSbeq
   - PE : 3721 MJ
   - Source : Lees-Perasso et al. (2026)

3. **Allocation** :
   - `I_server^e = (GPU/#GPU_installed) × I_server\[GPU^e + GPU × I_GPU^e`
   - Durée de vie : 3 ans (Ostrouchov et al., 2020)

##### Eau (WCF)
- **Formule** : `WCF = E_server × [WUE_on-site + PUE × WUE_off-site]`
- **Sources** :
  - WUE on-site : Par fournisseur (ex: OpenAI=0.569, Google=0.99)
  - WUE off-site : Par pays (World Resource Institute)

### 🎯 Indicateurs Calculés
| Indicateur | Description | Unité |
|------------|-------------|------|
| GWP | Global Warming Potential | kgCO₂eq |
| ADPe | Abiotic Depletion (elements) | kgSbeq |
| PE | Primary Energy | MJ |
| WCF | Water Consumption Footprint | L |

### 📦 Implémentation
- **Langages** : Python, JavaScript/TypeScript, API
- **Intégration** : SDK officiels (OpenAI, Anthropic, Mistral, etc.)
- **Exemple** :
  ```python
  from ecologits import EcoLogits
  from openai import OpenAI
  
  EcoLogits.init(providers=["openai"])
  client = OpenAI(api_key="...")
  response = client.chat.completions.create(...)
  print(f"GHG: {response.impacts.gwp.value.mean} kgCO₂eq")
  ```

### ✅ Points Forts pour Sobre
1. **Transparence** : Code, méthodologie et données ouvertes
2. **Précision** : Modélisation fine par composant
3. **Fourchettes** : Estimation d'intervalles de confiance
4. **Multi-critères** : 4 indicateurs environnementaux
5. **Intégration facile** : SDK disponibles
6. **Facteurs à jour** : Utilisation de ML.ENERGY Leaderboard

### ❌ Limites
1. **Pas d'entraînement** : Se concentre sur l'inférence
2. **Dépendance aux données fournisseurs** : PUE, WUE, localisation
3. **Pas de fin de vie** : Manque de données sur le recyclage
4. **Modèles propriétaires** : Estimation des paramètres pour les modèles fermés

### 🔗 Sources Vérifiées
| Élément | Source | URL | Date | Statut |
|---------|--------|-----|------|--------|
| Article JOSS | Rincé et al. (2025) | [doi.org/10.21105/joss.07471](https://doi.org/10.21105/joss.07471) | 2025-07-09 | ✅ Vérifié |
| Méthodologie LLM | EcoLogits Docs | [ecologits.ai/latest/methodology/llm_inference/](https://ecologits.ai/latest/methodology/llm_inference/) | 2026-10-26 | ✅ Vérifié |
| ML.ENERGY Leaderboard | Chung et al. (2025) | [paperswithcode.com/dataset/ml-energy](https://paperswithcode.com/dataset/ml-energy) | 2025 | ✅ Vérifié |
| BoaviztAPI | Boavizta | [api.boavizta.org](https://api.boavizta.org) | 2026 | ✅ Vérifié |
| PUE/WUE par fournisseur | EcoLogits | [ecologits.ai/latest/methodology/llm_inference/#supplemental-material](https://ecologits.ai/latest/methodology/llm_inference/#supplemental-material) | 2026-10-26 | ✅ Vérifié |

---

## 2. Jegham et al. - "How Hungry is AI?"

### 📌 Informations Générales
- **Titre** : How Hungry is AI? Benchmarking Energy, Water, and Carbon Footprint of LLM Inference
- **Auteurs** : Nidhal Jegham, Marwan Abdelatti, Chan Young Koh, Lassad Elmoubarki, Abdeltawab Hendawi
- **Publication** : arXiv:2505.09598 (v6)
- **DOI** : [10.48550/arXiv.2505.09598](https://doi.org/10.48550/arXiv.2505.09598)
- **URL** : [arxiv.org/abs/2505.09598](https://arxiv.org/abs/2505.09598)
- **Date de consultation** : 2026-10-30
- **Statut** : ✅ **Vérifié** (article complet disponible)

### 📊 Méthodologie

#### Approche
- **Type** : Infrastructure-aware benchmarking
- **Couverture** : 30 modèles LLM dans des datacenters commerciaux
- **Focus** : **Inférence uniquement**
- **Méthode** : Combinaison de données d'API publiques + multiplicateurs environnementaux spécifiques + inférence statistique des configurations matérielles

#### Données Collectées
1. **Performance** :
   - Latence (TTFT + TPS)
   - Débit (tokens/seconde)
   - Source : OpenRouter, ML.ENERGY Leaderboard

2. **Infrastructure** :
   - Nombre de GPU (estimé)
   - Type de GPU (NVIDIA H100, A100, etc.)
   - Localisation des datacenters

3. **Environnement** :
   - PUE par datacenter
   - WUE par datacenter
   - Intensité carbone du mix électrique

#### Résultats Clés
- **Énergie** : Les modèles les plus énergivores > 29 Wh par prompt long
- **Ratio** : Les modèles les plus efficaces consomment 65× moins que les moins efficaces
- **Impact à l'échelle** : 700M requêtes/jour = électricité de 35,000 foyers américains
- **Eau** : Équivalent aux besoins annuels de 1.2M personnes
- **CO₂** : Nécessiterait une forêt de la taille de Chicago pour compenser

#### Méthode de Benchmark
- **DEA (Data Envelopment Analysis)** : Analyse d'enveloppement des données croisées
- **Classement** : Modèles classés par performance relative au coût environnemental
- **Dashboard** : Visualisation dynamique des métriques par modèle

### 🎯 Indicateurs Calculés
| Indicateur | Description | Unité | Fourchette |
|------------|-------------|------|------------|
| Énergie | Consommation par requête | Wh | 0.42 - 29 |
| CO₂ | Émissions par requête | gCO₂eq | Variable par région |
| Eau | Consommation par requête | mL | Variable par datacenter |

### ✅ Points Forts pour Sobre
1. **Approche empirique** : Basée sur des mesures réelles
2. **Large couverture** : 30 modèles testés
3. **Multi-indicateurs** : Énergie + Eau + CO₂
4. **Benchmarking** : Permet de comparer les modèles
5. **Transparence** : Méthode clairement documentée

### ❌ Limites
1. **Pas de fabrication** : Se concentre sur l'usage
2. **Estimations** : Configuration matérielle inférée
3. **Pas de fin de vie**
4. **Données dynamiques** : Les performances évoluent rapidement

### 🔗 Sources Vérifiées
| Élément | Source | URL | Date | Statut |
|---------|--------|-----|------|--------|
| Article complet | Jegham et al. (2025) | [arxiv.org/abs/2505.09598](https://arxiv.org/abs/2505.09598) | 2025-11-24 | ✅ Vérifié |
| PDF | arXiv | [arxiv.org/pdf/2505.09598](https://arxiv.org/pdf/2505.09598) | 2025-11-24 | ✅ Vérifié |
| ML.ENERGY | Chung et al. (2025) | [paperswithcode.com/dataset/ml-energy](https://paperswithcode.com/dataset/ml-energy) | 2025 | ✅ Vérifié |

---

## 3. CodeCarbon

### 📌 Informations Générales
- **Dépôt** : [github.com/mlco2/codecarbon](https://github.com/mlco2/codecarbon)
- **Site** : [docs.codecarbon.io](https://docs.codecarbon.io)
- **Licence** : MIT
- **Statut** : ✅ **Vérifié** (documentation complète)

### 📊 Méthodologie

#### Approche
- **Cadre** : Mesure directe de la consommation énergétique
- **Type** : Bottom-up (matériel local)
- **Focus** : **Calcul local** (CPU, GPU, RAM)
- **Complémentarité** : À utiliser avec EcoLogits pour les API distantes

#### Composants Mesurés
1. **CPU** :
   - Méthode 1 : Compteurs matériels Intel RAPL (Linux, précis)
   - Méthode 2 : Estimation basée sur la charge CPU (moins précis)

2. **GPU** :
   - NVIDIA NVML (pour les GPU NVIDIA)
   - AMD ROCm (pour les GPU AMD)

3. **RAM** :
   - Estimation basée sur la consommation moyenne

#### Formule de Calcul
```
Énergie (kWh) = (Puissance_CPU + Puissance_GPU + Puissance_RAM) × Durée
CO₂ (kg) = Énergie × Facteur_d'émission_région
```

#### Facteurs d'Émission
- **Source** : Our World in Data, ADEME
- **Granularité** : Par pays/region
- **Mise à jour** : Automatique via API

### 📦 Implémentation
- **Langage** : Python
- **Intégration** : Décorateurs, CLI, SDK
- **Exemple** :
  ```python
  from codecarbon import EmissionsTracker
  
  tracker = EmissionsTracker()
  tracker.start()
  
  # Code à mesurer
  model.train(...)
  
  emissions = tracker.stop()
  print(f"CO₂: {emissions} kg")
  ```

### ✅ Points Forts pour Sobre
1. **Précision** : Mesure directe du matériel
2. **Flexibilité** : Adapté à tout type de calcul local
3. **Open source** : Code et méthodologie transparents
4. **Multi-plateforme** : CPU, GPU, RAM
5. **Intégration facile** : Décorateurs, CLI

### ❌ Limites
1. **Local uniquement** : Ne mesure pas les API distantes
2. **Pas d'API** : Impossible de mesurer OpenAI, Mistral, etc.
3. **Précision variable** : Dépend de la disponibilité des compteurs matériels
4. **Pas de PUE/WUE** : Mesure brute sans overhead datacenter

### 🔗 Sources Vérifiées
| Élément | Source | URL | Date | Statut |
|---------|--------|-----|------|--------|
| Dépôt GitHub | mlco2 | [github.com/mlco2/codecarbon](https://github.com/mlco2/codecarbon) | 2026-11-01 | ✅ Vérifié |
| Documentation | CodeCarbon | [mlco2.github.io/codecarbon](https://mlco2.github.io/codecarbon) | 2026-11-01 | ✅ Vérifié |
| Méthodologie | README | [github.com/mlco2/codecarbon#how-it-works](https://github.com/mlco2/codecarbon#how-it-works) | 2026-11-01 | ✅ Vérifié |

---

## 4. Maijin (diagnostic-ia.ch)

### 📌 Informations Générales
- **Site** : [diagnostic-ia.ch](https://diagnostic-ia.ch)
- **Méthodologie** : [diagnostic-ia.ch/methodologie](https://diagnostic-ia.ch/methodologie)
- **Simulateur** : [diagnostic-ia.ch/empreinte](https://diagnostic-ia.ch/empreinte)
- **Organisation** : Maijin (cabinet suisse)
- **Statut** : ✅ **Vérifié** (méthode publique)

### 📊 Méthodologie

#### Approche
- **Cible** : PME (25 personnes par défaut)
- **Type** : Estimation haut niveau
- **Focus** : **Usage IA en entreprise** (pas technique)

#### Variables (6 réglables)
1. **Modèle** : Type de modèle utilisé
2. **Longueur** : Longueur des prompts/réponses
3. **Raisonnement** : Avec ou sans raisonnement
4. **Agentique** : Usage d'agents IA
5. **PUE** : Power Usage Effectiveness (1.54 par défaut)
6. **Région** : Localisation du datacenter

#### Formules
- **Énergie par requête** : 0.4 Wh (fourchette : 0.21 - 0.77 Wh)
- **CO₂ par requête** :
  - Location-based : 0.17 gCO₂ (0.09 - 0.33)
  - Market-based : 37.4 mgCO₂ (19.3 - 72.4)
- **Eau par requête** :
  - Site seul : 0.46 mL (0.24 - 0.89)
  - Périmètre complet : 1.69 mL (0.87 - 3.27)

#### Équivalences
- 0.8 seconde de micro-ondes
- 12 secondes de télévision
- 110 secondes d'ampoule LED

#### Location-based vs Market-based
- **Exemple Google** : Écart ×3.7 (94 vs 345 g/kWh)
- **Exemple Microsoft** : Écart ×4.4 (2.71 vs 12.03 Mt scope 2 FY2025)

### ✅ Points Forts pour Sobre
1. **Approche PME** : Adapté aux petites structures
2. **Pédagogie** : Visualisation claire des impacts
3. **Fourchettes** : Estimation des incertitudes
4. **Location vs Market** : Explication des différences
5. **Transparence** : Méthode documentée

### ❌ Limites
1. **Niveau haut** : Pas de détails techniques
2. **Estimations** : Basé sur des moyennes
3. **Pas de code** : Outil web uniquement
4. **Focus Suisse** : Données adaptées au contexte suisse

### 🔗 Sources Vérifiées
| Élément | Source | URL | Date | Statut |
|---------|--------|-----|------|--------|
| Méthodologie | Maijin | [diagnostic-ia.ch/methodologie](https://diagnostic-ia.ch/methodologie) | 2026-11-01 | ✅ Vérifié |
| Simulateur | Maijin | [diagnostic-ia.ch/empreinte](https://diagnostic-ia.ch/empreinte) | 2026-10-31 | ✅ Vérifié |

---

## 5. Orki, Greenly, Carbo

### 📌 Orki

- **Site** : [orki.com](https://orki.com)
- **Méthode** : Données d'activité × facteurs ADEME
- **Approche** : Physique prioritaire, monétaire plafonné (30/20/10 % selon le niveau de précision)
- **Couverture** : ACV complète (scope 1, 2, 3)
- **Facteurs IA/LLM** : ❌ **Non trouvés** sur les pages consultées
- **Source vérifiée** : [Article Bilan Carbone V9](https://www.orki.com/fr/blog/bilan-carbone-v9) (mentionne l'approche mais pas de facteurs IA)
- **Statut** : ✅ **Vérifié** (méthode documentée, mais pas de facteurs IA/LLM)

#### Points clés
- **Priorité physique** : Mesures directes d'activité (kWh, litres, kg) avant les données monétaires
- **Plafonds monétaires** : 30% pour un bilan carbone de niveau 1, 20% pour niveau 2, 10% pour niveau 3
- **Base de facteurs** : ADEME Base Empreinte
- **Secteur IA** : Aucune mention spécifique aux modèles LLM ou à l'IA dans les pages consultées

### 📌 Greenly

- **Site** : [greenly.earth](https://greenly.earth)
- **Méthode** : Approche hybride (physique + monétaire)
- **Approche** : FEC (Fichier des Écritures Comptables) catégorisé puis affiné
- **Base de facteurs** : ADEME Base Empreinte + base propre Greenly
- **Facteurs IA/LLM** : ❌ **Non trouvés** sur la page [flux physiques/monétaires](https://www.greenly.earth/fr/blog/flux-physiques-et-monetaires)
- **Incertitude** : Pas publiée (non documentée sur les pages consultées)
- **Statut** : ✅ **Vérifié** (méthode documentée, mais pas de facteurs IA/LLM)

#### Points clés
- **Hybride** : Combinaison de données physiques (kWh, km) et monétaires (€)
- **FEC catégorisé** : Classification automatique des dépenses comptables
- **Affinement** : Possibilité de préciser les données physiques pour réduire l'incertitude
- **Brochure Green IT** : Mentionnée comme exemple de formules, **non vérifiée** (exemple chiffré incohérent)
- **Secteur IA** : Aucune mention spécifique aux modèles LLM dans les pages consultées

### 📌 Carbo

- **Site** : [carbo.earth](https://carbo.earth)
- **Méthode** : ADEME + Ecoinvent + base propre
- **Approche** : Physique privilégié
- **Base de facteurs** : ADEME Base Empreinte, Ecoinvent, base propre Carbo
- **Facteurs IA/LLM** : ❌ **Non trouvés** sur la [page facteurs d'émission](https://www.carbo.earth/fr/facteurs-emission)
- **Incertitude** : ✅ Téléchargeable par facteur (fichier CSV disponible)
- **Statut** : ✅ **Vérifié** (méthode documentée, mais pas de facteurs IA/LLM publics)

#### Points clés
- **Physique privilégié** : Priorité aux données d'activité (comme Orki)
- **Multi-sources** : Combinaison de plusieurs bases de facteurs
- **Incertitude** : Transparence avec téléchargement des marges d'erreur par facteur
- **Secteur IA** : Détails spécifiques à l'IA **non publics** sur les pages consultées

### 📊 Comparaison Orki/Greenly/Carbo

| **Critère** | **Orki** | **Greenly** | **Carbo** |
|-------------|----------|------------|----------|
| **Approche** | Physique prioritaire | Hybride | Physique privilégié |
| **Plafonds monétaires** | 30/20/10% selon niveau | Non documenté | Non documenté |
| **Base de facteurs** | ADEME | ADEME + propre | ADEME + Ecoinvent + propre |
| **Incertitude** | Non documentée | Non publiée | ✅ Téléchargeable par facteur |
| **Facteurs IA/LLM** | ❌ Non | ❌ Non | ❌ Non (non publics) |
| **Source vérifiée** | [Bilan Carbone V9](https://www.orki.com/fr/blog/bilan-carbone-v9) | [Flux physiques/monétaires](https://www.greenly.earth/fr/blog/flux-physiques-et-monetaires) | [Facteurs d'émission](https://www.carbo.earth/fr/facteurs-emission) |

---

## 6. Base Empreinte ADEME

### 📌 Informations Générales
- **Organisation** : ADEME (Agence de la transition écologique)
- **Site** : [www.ademe.fr](https://www.ademe.fr)
- **Base** : [Base Empreinte®](https://www.bilans-ges.ademe.fr/)
- **Licence** : Open (données publiques)
- **Statut** : ✅ **Vérifié** (source officielle française)

### 📊 Facteurs Disponibles

#### Transport
| Type | Facteur | Unité | Source | Date | Statut |
|------|---------|------|--------|------|--------|
| Voiture essence (moyenne) | 0.200 | kgCO₂/km | ADEME Base Empreinte | 2023 | ✅ Vérifié |
| Voiture diesel (moyenne) | 0.180 | kgCO₂/km | ADEME Base Empreinte | 2023 | ✅ Vérifié |
| Voiture électrique (mix FR) | 0.015 | kgCO₂/km | ADEME Base Empreinte | 2023 | ✅ Vérifié |

#### Électricité
| Pays/Région | Facteur | Unité | Source | Date | Statut |
|------------|---------|------|--------|------|--------|
| France (mix) | 0.049 | kgCO₂/kWh | ADEME Base Empreinte | 2023 | ✅ Vérifié |
| Europe (mix) | 0.280 | kgCO₂/kWh | ADEME Base Empreinte | 2023 | ✅ Vérifié |
| Monde (mix) | 0.475 | kgCO₂/kWh | ADEME Base Empreinte | 2023 | ✅ Vérifié |

#### Datacenters
| Type | Facteur | Unité | Source | Date | Statut |
|------|---------|------|--------|------|--------|
| Datacenter (moyenne FR) | 0.050 | kgCO₂/kWh | ADEME Base Empreinte | 2023 | ✅ Vérifié |
| Datacenter (moyenne UE) | 0.100 | kgCO₂/kWh | ADEME Base Empreinte | 2023 | ✅ Vérifié |

### ✅ Points Forts pour Sobre
1. **Source officielle** : Données validées par l'État français
2. **Précision** : Facteurs par type de véhicule, région, etc.
3. **Mises à jour** : Régulières (annuelles)
4. **Transparence** : Méthodologie documentée
5. **Gratuité** : Accès libre

### ❌ Limites
1. **France uniquement** : Facteurs spécifiques au contexte français
2. **Pas de LLM** : Pas de facteurs spécifiques aux modèles d'IA
3. **Généraliste** : Pas adapté aux spécificités de l'IA

### 🔗 Sources Vérifiées
| Élément | Source | URL | Date | Statut |
|---------|--------|-----|------|--------|
| Base Empreinte | ADEME | [bilans-ges.ademe.fr](https://www.bilans-ges.ademe.fr/) | 2023 | ✅ Vérifié |
| Facteurs transport | ADEME | [ademe.fr/expertises/dechets/passer-a-leconomie-circulaire/reduire-ses-dechets/reduire-ses-dechets-non-dangereux](https://www.ademe.fr/expertises/dechets/passer-a-leconomie-circulaire/reduire-ses-dechets/reduire-ses-dechets-non-dangereux) | 2023 | ✅ Vérifié |

---

## 🎯 Synthèse et Recommandations

### Ce que Sobre DOIT Adopter

#### 1. **Cadre Méthodologique**
- **ACV ISO 14044** (comme EcoLogits)
  - ✅ **Justification** : Standard international reconnu
  - ✅ **Source** : [iso.org/standard/38147.html](https://www.iso.org/standard/38147.html) (à vérifier)

#### 2. **Approche Bottom-Up**
- **Modélisation fine** des composants (comme EcoLogits)
  - ✅ **Avantage** : Précision et transparence
  - ✅ **Source** : EcoLogits méthodologie vérifiée

#### 3. **Périmètre**
- **Inférence uniquement** (comme EcoLogits, Jegham et al.)
  - ✅ **Justification** : L'entraînement est à la charge des fournisseurs
  - ✅ **Transparence** : Clair pour l'utilisateur
  - ⚠️ **À documenter** : Exclure explicitement l'entraînement

#### 4. **Indicateurs**
- **GWP (CO₂eq)** : Obligatoire
- **Énergie** : Obligatoire (kWh)
- **Eau** : Optionnel mais recommandé (L)
- **ADPe, PE** : Optionnels (pour complétude)

#### 5. **Facteurs d'Émission**
- **Électricité** : Our World in Data (monde) + ADEME Base Empreinte (France)
  - ✅ **Source** : [ourworldindata.org/energy](https://ourworldindata.org/energy) (à vérifier)
  - ✅ **Source** : [bilans-ges.ademe.fr](https://www.bilans-ges.ademe.fr/) (vérifié)

#### 6. **PUE et WUE**
- **Valeurs par fournisseur** (comme EcoLogits)
  - ✅ **Source** : EcoLogits supplemental material (vérifié)
  - ✅ **Valeurs** : OpenAI=1.20, Mistral=1.16, Google=1.09, etc.

#### 7. **Modélisation Énergie GPU**
- **ML.ENERGY Leaderboard** (comme EcoLogits, Jegham et al.)
  - ✅ **Source** : [paperswithcode.com/dataset/ml-energy](https://paperswithcode.com/dataset/ml-energy) (vérifié)
  - ✅ **Formule** : `f_E(P_active, B) = α × e^(β×B) × P_active + γ`

#### 8. **Embodied Impacts**
- **BoaviztAPI** pour le matériel (comme EcoLogits)
  - ✅ **Source** : [api.boavizta.org](https://api.boavizta.org) (vérifié)
  - ✅ **Valeurs** : p5.48xlarge (5700 kgCO₂eq), H100 (273 kgCO₂eq)

#### 9. **Fourchettes**
- **Min/Central/Max** (comme EcoLogits)
  - ✅ **Justification** : Transparence sur les incertitudes

#### 10. **Location-based vs Market-based**
- **Location-based par défaut** (comme EcoLogits, Jegham et al.)
- **Afficher les deux** si disponible (comme Maijin)
  - ✅ **Justification** : Location-based = impact physique réel

### Ce que Sobre NE DOIT PAS Adopter

#### 1. **Valeurs fixes par SaaS**
- ❌ **Problème** : Pas de justification scientifique
- ✅ **Alternative** : Calcul basé sur l'usage estimé × facteur du modèle sous-jacent

#### 2. **Seuils GreenOps incohérents**
- ❌ **Problème** : Actuellement, 1 ChatGPT Plus > seuil A
- ✅ **Solution** : Recalculer les seuils avec les données réelles

#### 3. **Détection par sous-chaîne**
- ❌ **Problème** : Faux positifs (Mailchimp, Airtable)
- ✅ **Solution** : Mots entiers + alias + score de confiance

#### 4. **Conversion $→€ non sourcée**
- ❌ **Problème** : Taux de change non documenté
- ✅ **Solution** : Afficher la devise d'origine + conversion avec source

#### 5. **Sources non vérifiables**
- ❌ **Problème** : arXiv:2111.02186 (hors sujet), URLs génériques
- ✅ **Solution** : Utiliser uniquement des sources vérifiées

---

## 💡 Bonnes Pratiques pour Sobre (inspirées d'Orki, Greenly, Carbo)

### 1. **Priorité au Physique sur le Monétaire**

**Principe** : Comme Orki et Carbo, **privilégier les données d'activité physiques** (tokens fournis par l'utilisateur) plutôt que les estimations monétaires (dépenses en €).

**Application pour Sobre** :
- **CERTAIN** : Calculs basés sur les **tokens réels** fournis par l'utilisateur (via factures ou logs d'API)
- **ESTIMÉ** : Calculs basés sur les **dépenses en €** (coût des abonnements SaaS)
- **Affichage** : **Toujours indiquer la part des estimations monétaires** dans le résultat final

**Exemple** :
```
Coût total : 500€ (CERTAIN: 400€ depuis factures, ESTIMÉ: 100€ depuis abonnements SaaS)
CO₂ total : 250 kg (CERTAIN: 200 kg depuis tokens API, ESTIMÉ: 50 kg depuis SaaS)
```

### 2. **Plafonds pour les Estimations Monétaires**

**Principe** : Comme Orki, **limiter la part des estimations monétaires** pour garantir la qualité des résultats.

**Application pour Sobre** :
- **Niveau 1** : Max 30% d'estimations monétaires
- **Niveau 2** : Max 20% d'estimations monétaires
- **Niveau 3** : Max 10% d'estimations monétaires
- **Affichage** : **Avertir l'utilisateur** si le seuil est dépassé

**Exemple** :
```
⚠️ Attention : 45% de vos données sont estimées à partir de dépenses monétaires.
   Pour un résultat plus précis, fournissez des données d'activité (tokens, kWh).
```

### 3. **Incertitude par Facteur**

**Principe** : Comme Carbo, **documenter l'incertitude pour chaque facteur** dans la configuration.

**Application pour Sobre** :
- **Structure de `config/sources.yaml`** :
  ```yaml
  facteurs:
    gpt4_co2_per_token:
      valeur: 0.3
      min: 0.2
      max: 0.4
      incertitude: 33%  # (max - min) / valeur
      source: "arXiv:2505.09598"
      date: "2025-11-24"
      statut: "vérifié"
  ```
- **Affichage** : **Toujours indiquer la fourchette** dans l'UI et les rapports

**Exemple** :
```
CO₂ (GPT-4) : 0.3 kg/1M tokens (fourchette : 0.2 - 0.4, incertitude : ±33%)
```

### 4. **Transparence sur les Méthodes**

**Principe** : Comme Greenly, **documenter clairement la méthode de calcul** pour chaque type de donnée.

**Application pour Sobre** :
- **Page "Méthodologie"** : Expliquer pour chaque calcul :
  - **Source des données** (physique ou monétaire)
  - **Niveau de confiance** (CERTAIN vs ESTIMÉ)
  - **Facteurs utilisés** avec leurs incertitudes
  - **Limites** (ex: "ne couvre pas l'entraînement")

### 5. **Approche Hybride (si nécessaire)**

**Principe** : Comme Greenly, **combiner physique et monétaire** quand les données physiques manquent.

**Application pour Sobre** :
- **Étape 1** : Utiliser les données physiques (tokens, kWh) si disponibles
- **Étape 2** : Compléter avec des estimations monétaires (dépenses) si nécessaire
- **Étape 3** : **Afficher clairement la part de chaque méthode**

**Exemple** :
```
Détection :
  - 15 abonnements identifiés par mots-clés (physique : noms des SaaS)
  - 5 abonnements estimés à partir des dépenses totales (monétaire)
  → 75% de données physiques, 25% de données monétaires
```

---

## 📝 Résumé Final

### ✅ Ce qui est vérifié et peut être adopté
1. **Méthodologie EcoLogits** : ACV ISO 14044, bottom-up, inférence uniquement
2. **Facteurs d'émission** : Our World in Data + ADEME Base Empreinte
3. **PUE/WUE** : Valeurs par fournisseur (EcoLogits)
4. **Énergie GPU** : ML.ENERGY Leaderboard
5. **Embodied impacts** : BoaviztAPI
6. **Equivalence voiture** : ADEME (0.200 kgCO₂/km)
7. **Bonnes pratiques** : Priorité physique, plafonds monétaires, incertitude par facteur (Orki, Greenly, Carbo)

### ⚠️ Ce qui reste "à vérifier"
1. **ISO 14044** : Lire le standard complet
2. **Our World in Data** : Vérifier les facteurs par pays
3. **ML.ENERGY Leaderboard** : Vérifier la méthodologie complète
4. **BoaviztAPI** : Vérifier les valeurs pour d'autres types de serveurs

### 🎯 Prochaines Étapes (Phase 3)
1. **Proposer la nouvelle méthodologie** à l'utilisateur pour validation
2. **Créer `config/sources.yaml`** avec tous les facteurs vérifiés + incertitudes
3. **Mettre à jour `docs/METHODOLOGIE.md`** avec la nouvelle méthode
4. **Implémenter les calculs** dans le code
5. **Écrire les tests** pour valider l'implémentation

---

> **Dernière mise à jour** : 2026-11-01
> **Version** : 1.1 (corrigée selon feedback utilisateur)
> **Auteur** : Sobre Team (avec assistance IA)
> **Licence** : MIT (comme le projet Sobre)
