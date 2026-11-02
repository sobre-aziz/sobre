# Proposition de Nouvelle Méthode - Sobre

> **Objectif** : Proposer une méthode de calcul **défendable devant un jury, un client ou un expert**, inspirée des meilleures pratiques (EcoLogits, Jegham et al., ADEME, Orki, Greenly, Carbo) et adaptée aux contraintes de Sobre.

> **Règle absolue** : *Un chiffre non sourcé ou une détection non qualifiée est un bug. Chaque facteur doit avoir : titre exact, auteur, URL précise, date de consultation, périmètre, et statut "vérifié" ou "à vérifier".*

---

## 📊 Table des Matières
1. [Principes Fondamentaux](#-principes-fondamentaux)
2. [Formules de Calcul](#-formules-de-calcul)
3. [Structure de `config/sources.yaml`](#-structure-de-configsourcesyaml)
4. [Catégorisation CERTAIN vs ESTIMÉ](#-catégorisation-certain-vs-estimé)
5. [Gestion des Incertitudes](#-gestion-des-incertitudes)
6. [Changements de Code Requis](#-changements-de-code-requis)
7. [Plan de Tests](#-plan-de-tests)
8. [Décisions à Valider](#-décisions-à-valider)
9. [Résumé des Livrables](#-résumé-des-livrables)

---

## 🎯 Principes Fondamentaux

### 1. Priorité au Physique sur le Monétaire
**Inspiration** : Orki (Bilan Carbone V9), Carbo

- **Physique (CERTAIN)** : Données d'activité mesurables directement
  - Tokens réels (input/output) fournis par l'utilisateur (via facture ou logs d'API)
  - kWh consommés (si disponibles)
  - Nombre de licences (depuis factures)
  
- **Monétaire (ESTIMÉ)** : Estimations basées sur les dépenses
  - Coût des abonnements SaaS → estimation des tokens via modèle sous-jacent
  - Dépenses API → estimation des tokens (si tarif connu)

- **Règle** : **Toujours afficher la part des estimations monétaires** dans les résultats

### 2. Plafonds pour les Estimations Monétaires
**Inspiration** : Orki (30/20/10% selon niveau)

| Niveau | Max % Monétaire | Couleur | Action |
|--------|------------------|---------|--------|
| 1 | 30% | ⚠️ Jaune | Avertissement : "Résultat acceptable mais à améliorer" |
| 2 | 20% | ✅ Vert | Résultat de qualité standard |
| 3 | 10% | ⭐ Or | Résultat haute précision |

### 3. Incertitude par Facteur
**Inspiration** : Carbo

Chaque facteur doit avoir `valeur`, `min`, `max`, `incertitude` dans `config/sources.yaml`

### 4. Transparence Totale
- **Sources** : Toujours citer URL précise (pas homepage)
- **Périmètre** : Toujours préciser inclusions/exclusions
- **Statut** : Toujours indiquer "vérifié" ou "à vérifier"

---

## 📐 Formules de Calcul

### 1. Coûts

#### 1.1 APIs (Modèles IA)
**Formule** : `coût_€ = (tokens_input × coût_input_€) + (tokens_output × coût_output_€)`
**Catégorie** : CERTAIN (si tokens fournis), ESTIMÉ (si tokens estimés)

#### 1.2 SaaS (Abonnements)
**Formule** : `coût_mensuel = valeur_abonnements`
**Règle** : NE JAMAIS ×12 pour les annuels. Préciser la période.

### 2. CO₂

#### 2.1 APIs
**Formule** : `CO2_kg = (tokens/1M) × co2_per_million × PUE × F_em_correction`
**Catégorie** : ESTIMÉ (toujours)

#### 2.2 SaaS
**Nouvelle approche** : `CO2 = (tokens_estimés/1M) × co2_per_million × PUE × F_em_correction`
**Si modèle inconnu** : "non estimable"

### 3. Équivalences
**Voiture** : `km = CO2_g / 0.2` (ADEME, 0.200 kgCO₂/km)
**Arrondi** : Toujours en mètres/kilomètres sensés

### 4. Score GreenOps
**Nouveaux seuils** (recalculés) :
- A: ≤50€, ≤250g CO₂/employé
- B: ≤100€, ≤500g
- C: ≤200€, ≤1000g
- D: ≤500€, ≤2500g
- E: >500€, >2500g

### 5. Économies
**Formule** : `économies_mensuelles = Σ(coût licences dormantes)`
**Annuelles** : UNIQUEMENT pour abonnements mensuels

### 6. Détection
**Nouvelle méthode** :
- Mots entiers (pas sous-chaîne)
- Liste blanche + alias
- Score de confiance (0-100)
- Correction manuelle

---

## 📁 Structure de `config/sources.yaml`

Voir le fichier complet dans la section [Structure Complète](#-structure-complète-de-configsourcesyaml) à la fin de ce document.

**Champs obligatoires pour chaque facteur** :
```yaml
valeur: 0.3
min: 0.2
max: 0.4
incertitude: "33%"  # Calculé : (max - min) / valeur
source: "Jegham et al. (2025)"
url: "https://arxiv.org/abs/2505.09598"
date_consultation: "2024-11-01"
périmètre: "inférence uniquement"
statut: "vérifié"  # ou "à vérifier"
```

---

## 🏷️ Catégorisation CERTAIN vs ESTIMÉ

### Règles

| Type de Donnée | Catégorie | Condition |
|----------------|-----------|-----------|
| Tokens (input/output) | CERTAIN | Fournis par l'utilisateur |
| Coût API | CERTAIN | Calculé depuis tokens × tarif |
| Coût SaaS | CERTAIN | Extrait directement d'une facture |
| Coût SaaS | ESTIMÉ | Converti depuis $ (taux non vérifié) |
| CO₂ API | ESTIMÉ | Toujours (dépend des facteurs) |
| CO₂ SaaS | ESTIMÉ | Toujours (hypothèse tokens) |
| Équivalence voiture | ESTIMÉ | Toujours (dépend du facteur) |
| Score GreenOps | ESTIMÉ | Toujours (dépend des seuils) |
| Économies | ESTIMÉ | Toujours (dépend détection dormantes) |
| Détection IA | CERTAIN | Score ≥ 90% + correction manuelle |
| Détection IA | ESTIMÉ | Score 50-89% |

### Affichage dans l'UI

**Format standard** :
```
[Valeur] [Unité] ([Catégorie])
  - Fourchette : [min] - [max] (±[incertitude])
  - Source : [source] ([date])
  - Périmètre : [périmètre]
```

**Exemple** :
```
Coût total : 500€ (CERTAIN)
  - Détail : 400€ (API, CERTAIN) + 100€ (SaaS, ESTIMÉ)
  - Part estimée : 20%

CO₂ total : 250 kg (ESTIMÉ)
  - Fourchette : 180 - 350 kg (±40%)
  - Source : Jegham et al. (2025) + ADEME (2023)
  - Périmètre : Inférence uniquement
```

---

## 📊 Gestion des Incertitudes

### 1. Calcul Automatique
```python
def calculer_incertitude(valeur: float, min_val: float, max_val: float) -> str:
    incertitude = ((max_val - min_val) / valeur) * 100
    return f"{incertitude:.0f}%"
```

### 2. Propagation des Incertitudes
Pour les calculs combinés (ex: CO₂ = tokens × co2_per_million × PUE × F_em) :
```
incertitude_totale = sqrt(
    incertitude_tokens² + 
    incertitude_co2_per_million² + 
    incertitude_PUE² + 
    incertitude_F_em²
)
```

**Simplification pour v1** : Utiliser les fourchettes min/max directement

### 3. Affichage
- **Toujours** : Valeur centrale + fourchette + incertitude
- **Optionnel** : Détail des incertitudes par composant (mode avancé)

---

## 🔧 Changements de Code Requis

### 1. Fichiers à Créer

| Fichier | Description | Priorité |
|---------|-------------|----------|
| `config/sources.yaml` | Tous les facteurs avec incertitudes | ⭐⭐⭐ |
| `config/corrections.yaml` | Corrections manuelles de détection | ⭐⭐ |
| `utils/uncertainty.py` | Calcul et gestion des incertitudes | ⭐⭐ |
| `utils/detection_ia.py` | Nouvelle détection avec score de confiance | ⭐⭐⭐ |

### 2. Fichiers à Modifier

#### `utils/carbon_calculator.py`
**Changements** :
- Intégrer PUE et F_em_correction dans les calculs
- Ajouter le calcul des fourchettes (min/max)
- Retourner la catégorie (CERTAIN/ESTIMÉ)
- Ajouter l'incertitude dans les résultats

**Exemple** :
```python
def calculate_api_carbon(
    model_name: str,
    total_tokens: int,
    region: str = "France"
) -> Dict:
    # Récupérer les facteurs
    co2_per_million = get_co2_factor(model_name)
    pue = get_pue(model_name)
    f_em_local = get_emission_factor(region)
    f_em_reference = get_emission_factor("Monde")
    f_em_correction = f_em_local / f_em_reference
    
    # Calcul central
    co2_kg = (total_tokens / 1_000_000) * co2_per_million * pue * f_em_correction
    
    # Calcul fourchettes
    co2_min = (total_tokens / 1_000_000) * co2_per_million['min'] * pue['min'] * (f_em_local['min'] / f_em_reference['max'])
    co2_max = (total_tokens / 1_000_000) * co2_per_million['max'] * pue['max'] * (f_em_local['max'] / f_em_reference['min'])
    
    return {
        "model": model_name,
        "total_tokens": total_tokens,
        "carbon_kg": co2_kg,
        "carbon_g": co2_kg * 1000,
        "carbon_min_kg": co2_min,
        "carbon_max_kg": co2_max,
        "incertitude": calculer_incertitude(co2_kg, co2_min, co2_max),
        "catégorie": "ESTIMÉ",
        "périmètre": "inférence uniquement"
    }
```

#### `utils/cost_calculator.py`
**Changements** :
- Gérer les devises (USD, EUR)
- Appliquer le taux de change si nécessaire
- Retourner la catégorie (CERTAIN/ESTIMÉ)
- Préciser la période (mensuel/annuel)

**Exemple** :
```python
def calculate_api_cost(
    model_name: str,
    input_tokens: int,
    output_tokens: int,
    currency: str = "EUR"
) -> Dict:
    # Récupérer les tarifs
    input_cost = get_model_cost(model_name, "input")
    output_cost = get_model_cost(model_name, "output")
    
    # Calcul
    total_cost_input = input_tokens * input_cost['valeur']
    total_cost_output = output_tokens * output_cost['valeur']
    total_cost = total_cost_input + total_cost_output
    
    # Conversion si nécessaire
    if input_cost['devise'] != currency:
        total_cost = convert_currency(total_cost, input_cost['devise'], currency)
    
    return {
        "model": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_cost": total_cost,
        "currency": currency,
        "catégorie": "CERTAIN",
        "source": f"{input_cost['source']}, {output_cost['source']}"
    }
```

#### `utils/greenops_scoring.py`
**Changements** :
- Utiliser les nouveaux seuils (50€, 100€, 200€, 500€)
- Exclure temporairement le critère "licences actives"
- Ajouter la règle de passage score → grade
- Retourner plus de détails

**Exemple** :
```python
def calculate_greenops_score(
    total_cost: float,
    total_carbon_g: float,
    number_of_employees: int,
    number_of_licenses: int,
    dormant_licenses_count: int = 0
) -> Dict:
    # Calculer les métriques par employé
    cost_per_employee = total_cost / number_of_employees
    carbon_per_employee = total_carbon_g / number_of_employees
    
    # Taux de licences actives (si données disponibles)
    if number_of_licenses > 0:
        active_licenses_percentage = ((number_of_licenses - dormant_licenses_count) / number_of_licenses) * 100
        licences_data_available = True
    else:
        active_licenses_percentage = 100  # Neutraliser
        licences_data_available = False
    
    # Calculer les scores
    score_coût = max(0, 100 - (cost_per_employee / 50) * 100)  # seuil A = 50
    score_co2 = max(0, 100 - (carbon_per_employee / 250) * 100)  # seuil A = 250
    score_licences = 100 if not licences_data_available else (active_licenses_percentage / 100) * 100
    
    # Score final
    score_greenops = (score_coût + score_co2 + score_licences) / 3
    
    # Déterminer le grade
    if score_greenops >= 90:
        grade, grade_name = "A", "Excellent"
    elif score_greenops >= 70:
        grade, grade_name = "B", "Bon"
    elif score_greenops >= 50:
        grade, grade_name = "C", "Moyen"
    elif score_greenops >= 30:
        grade, grade_name = "D", "À améliorer"
    else:
        grade, grade_name = "E", "Critique"
    
    return {
        "cost_per_employee": round(cost_per_employee, 2),
        "carbon_per_employee": round(carbon_per_employee, 2),
        "active_licenses_percentage": round(active_licenses_percentage, 1) if licences_data_available else None,
        "score_coût": round(score_coût, 1),
        "score_co2": round(score_co2, 1),
        "score_licences": round(score_licences, 1),
        "score_greenops": round(score_greenops, 1),
        "grade": grade,
        "grade_name": grade_name,
        "licences_data_available": licences_data_available,
        "catégorie": "ESTIMÉ"
    }
```

#### `utils/subscription_tracker.py`
**Changements** :
- Remplacer la détection par sous-chaîne par la nouvelle méthode
- Ajouter le score de confiance
- Intégrer les corrections manuelles
- Gérer les alias

**Exemple** :
```python
def detect_ai_subscriptions(
    data: Union[pd.DataFrame, List[Dict]],
    name_column: str = "Nom",
    description_column: Optional[str] = None,
    provider_column: Optional[str] = None
) -> List[Dict]:
    """
    Détecte les abonnements IA avec score de confiance.
    """
    # Charger les configurations
    config = load_config()
    liste_blanche = config['mots_cles_ia']['liste_blanche']
    alias = config['mots_cles_ia']['alias']
    corrections = load_corrections()
    
    detected = []
    
    for _, row in data.iterrows():
        nom = str(row[name_column]).strip()
        description = str(row[description_column]).strip() if description_column else ""
        fournisseur = str(row[provider_column]).strip() if provider_column else ""
        
        # Vérifier les corrections manuelles
        correction = next((c for c in corrections if c['nom'].lower() == nom.lower()), None)
        if correction:
            detected.append({
                **correction,
                "nom": nom,
                "est_ia": correction['type'] == "ia",
                "score_confiance": 100,
                "source": "correction manuelle"
            })
            continue
        
        # Détection automatique
        result = détecter_abonnements_ia(nom, description, fournisseur, liste_blanche, alias)
        detected.append(result)
    
    return detected

def détecter_abonnements_ia(nom: str, description: str, fournisseur: str, liste_blanche: List[str], alias: Dict) -> Dict:
    """
    Détection automatique avec score de confiance.
    """
    # Normalisation
    texte = f"{nom} {description} {fournisseur}".lower()
    mots = re.findall(r'\b\w+\b', texte)  # Mots entiers uniquement
    nom_normalisé = re.sub(r'[^\w\s-]', '', nom).lower()
    
    # Correspondances
    correspondances = []
    
    # Liste blanche
    for mot in mots:
        if mot in liste_blanche:
            correspondances.append(mot)
    
    # Alias
    for alias_key, saas_standard in alias.items():
        alias_normalisé = re.sub(r'[^\w\s-]', '', alias_key).lower()
        if alias_normalisé in nom_normalisé:
            correspondances.append(saas_standard)
    
    # Score de confiance
    score = calculer_score_confiance(correspondances, mots, nom_normalisé)
    
    return {
        "nom": nom,
        "est_ia": score >= 50,
        "correspondances": correspondances,
        "score_confiance": score,
        "type": "ia" if score >= 50 else "autre",
        "source": "détection automatique"
    }
```

#### `app.py`
**Changements** :
- Intégrer les nouvelles fonctions de calcul
- Afficher les catégories (CERTAIN/ESTIMÉ) partout
- Afficher les fourchettes et incertitudes
- Ajouter des avertissements pour les estimations monétaires
- Ajouter une page "Méthodologie" (déjà fait en Phase 1)

**Exemple d'affichage** :
```python
# Dans le dashboard
st.subheader("💰 Coûts")
col1, col2 = st.columns(2)
with col1:
    st.metric("Coût total", f"{total_cost:.2f}€", delta=f"{cost_variation:.2f}€")
    st.caption(f"Catégorie: {cost_category} | Source: {cost_source}")
    if cost_estimated_percentage > 0:
        st.warning(f"⚠️ {cost_estimated_percentage}% des données sont estimées")

with col2:
    st.metric("CO₂ total", f"{total_co2:.1f} kg", delta=f"{co2_variation:.1f} kg")
    st.caption(f"Catégorie: ESTIMÉ | Fourchette: {co2_min:.1f}-{co2_max:.1f} kg (±{co2_uncertainty})")

# Dans les détails
with st.expander("📊 Détails des calculs"):
    st.write("### Coûts")
    for cost_item in cost_details:
        st.write(f"- **{cost_item['name']}**: {cost_item['cost']:.2f}€ ({cost_item['category']})")
        if cost_item['category'] == "ESTIMÉ":
            st.caption(f"  Source: {cost_item['source']} | Incertitude: {cost_item['uncertainty']}")
    
    st.write("### CO₂")
    for co2_item in co2_details:
        st.write(f"- **{co2_item['name']}**: {co2_item['co2']:.3f} kg (ESTIMÉ)")
        st.caption(f"  Fourchette: {co2_item['min']:.3f}-{co2_item['max']:.3f} kg | Source: {co2_item['source']}")
```

#### `utils/report_generator.py`
**Changements** :
- Ajouter les catégories dans les rapports PDF
- Ajouter les fourchettes et incertitudes
- Clarifier le périmètre (inférence uniquement)
- Ajouter une section "Méthodologie" dans le PDF

**Exemple** :
```python
def generate_pdf_report(data: Dict) -> None:
    # ... code existant ...
    
    # Nouvelle section : Méthodologie
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Méthodologie", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, """
    Tous les calculs de ce rapport sont basés sur des sources vérifiées.
    
    • Coûts : Tarifs officiels des fournisseurs (OpenAI, Mistral, etc.)
    • CO₂ : Facteurs de Jegham et al. (2025) + ADEME Base Empreinte
    • PUE : Valeurs par fournisseur (EcoLogits)
    • Équivalence voiture : 0.200 kgCO₂/km (ADEME, 2023)
    
    Périmètre : Inférence uniquement (pas entraînement, pas fabrication).
    Catégories :
      - CERTAIN : Données mesurées directement
      - ESTIMÉ : Données calculées avec hypothèses
    """)
    
    # Dans les tableaux
    for item in data['costs']:
        pdf.cell(50, 10, item['name'])
        pdf.cell(30, 10, f"{item['cost']:.2f}€")
        pdf.cell(30, 10, item['category'])
        pdf.cell(0, 10, item['source'], ln=True)
```

### 3. Fichiers à Supprimer

| Fichier | Raison |
|---------|--------|
| Aucun | Tous les fichiers existants sont conservés et mis à jour |

---

## 🧪 Plan de Tests

### 1. Tests Unitaires

#### `tests/test_carbon_calculator.py`
**Nouveaux tests** :
```python
# Test des formules de base
class TestCarbonCalculator:
    def test_calculate_api_carbon_gpt4(self):
        result = calculate_api_carbon("GPT-4", 1000, region="France")
        assert result["carbon_kg"] == pytest.approx(0.000037, rel=0.01)
        assert result["catégorie"] == "ESTIMÉ"
        assert result["incertitude"] is not None
        
    def test_calculate_api_carbon_with_uncertainty(self):
        result = calculate_api_carbon("GPT-4", 1000, region="France")
        assert result["carbon_min_kg"] < result["carbon_kg"] < result["carbon_max_kg"]
        
    def test_calculate_saas_carbon_chatgpt_plus(self):
        result = calculate_saas_carbon("ChatGPT_Plus", usage_level="moyen", region="France")
        assert result["carbon_kg"] == pytest.approx(0.037, rel=0.01)
        assert result["catégorie"] == "ESTIMÉ"
        
    def test_calculate_saas_carbon_unknown_model(self):
        result = calculate_saas_carbon("Unknown_SaaS", usage_level="moyen", region="France")
        assert result["carbon_kg"] == "non estimable"

# Test des sources
class TestCarbonSources:
    def test_all_sources_have_required_fields(self):
        sources = load_sources()
        for source_type, items in sources.items():
            if source_type in ["facteurs_co2", "pue", "tarifs", "taux_de_change", "équivalences"]:
                for item in items.values():
                    if isinstance(item, dict):
                        assert "valeur" in item, f"Missing 'valeur' in {source_type}.{item}"
                        assert "source" in item, f"Missing 'source' in {source_type}.{item}"
                        assert "url" in item, f"Missing 'url' in {source_type}.{item}"
                        assert "date_consultation" in item, f"Missing 'date_consultation' in {source_type}.{item}"
                        assert "statut" in item, f"Missing 'statut' in {source_type}.{item}"
                        assert item["statut"] in ["vérifié", "à vérifier"]
```

#### `tests/test_cost_calculator.py`
**Nouveaux tests** :
```python
class TestCostCalculator:
    def test_calculate_api_cost_gpt4(self):
        result = calculate_api_cost("GPT-4", 1000, 500, currency="EUR")
        assert result["total_cost"] == pytest.approx(0.06, rel=0.01)
        assert result["currency"] == "EUR"
        assert result["catégorie"] == "CERTAIN"
        
    def test_calculate_api_cost_with_conversion(self):
        # Llama-3 tarif en USD, conversion en EUR
        result = calculate_api_cost("Llama-3", 1000, 500, currency="EUR")
        # 0.0015$ × 1500 = 0.00225$ → 0.00225 × 0.92 = 0.00207€
        assert result["total_cost"] == pytest.approx(0.00207, rel=0.01)
        assert result["currency"] == "EUR"
        assert result["catégorie"] == "ESTIMÉ"  # À cause de la conversion
        
    def test_calculate_saas_cost(self):
        result = calculate_saas_cost("ChatGPT_Plus", period="mensuel")
        assert result["cost"] == pytest.approx(20.0, rel=0.01)
        assert result["period"] == "mensuel"
        assert result["catégorie"] == "CERTAIN"

# Test des conversions
class TestCurrencyConversion:
    def test_convert_usd_to_eur(self):
        amount_eur = convert_currency(100, "USD", "EUR")
        assert amount_eur == pytest.approx(92.0, rel=0.01)  # 100 × 0.92
        
    def test_convert_eur_to_usd(self):
        amount_usd = convert_currency(100, "EUR", "USD")
        assert amount_usd == pytest.approx(108.7, rel=0.01)  # 100 / 0.92
```

#### `tests/test_greenops_scoring.py`
**Nouveaux tests** :
```python
class TestGreenOpsScoring:
    def test_score_a_with_one_subscription(self):
        # 1 employée, 1 ChatGPT Plus (20€), 1 Copilot (10€)
        result = calculate_greenops_score(
            total_cost=30.0,
            total_carbon_g=37.1,  # ChatGPT Plus + Copilot
            number_of_employees=1,
            number_of_licenses=2,
            dormant_licenses_count=0
        )
        assert result["grade"] == "A"
        assert result["grade_name"] == "Excellent"
        assert result["score_greenops"] >= 90
        
    def test_score_e_with_high_cost(self):
        # 1 employée, 1000€ de coûts
        result = calculate_greenops_score(
            total_cost=1000.0,
            total_carbon_g=5000.0,
            number_of_employees=1,
            number_of_licenses=5,
            dormant_licenses_count=0
        )
        assert result["grade"] == "E"
        assert result["grade_name"] == "Critique"
        
    def test_score_without_licenses_data(self):
        result = calculate_greenops_score(
            total_cost=30.0,
            total_carbon_g=37.1,
            number_of_employees=1,
            number_of_licenses=0,  # Pas de données
            dormant_licenses_count=0
        )
        assert result["licences_data_available"] == False
        assert result["score_licences"] == 100  # Neutralisé

# Test des seuils
class TestGreenOpsThresholds:
    def test_all_thresholds_are_coherent(self):
        """Vérifie que les seuils permettent à une PME avec 1 abonnement d'atteindre A"""
        # ChatGPT Plus = 20€, CO₂ = 37.1g
        for grade, config in load_config()["seuils_greenops"].items():
            if grade == "A":
                assert 20 <= config["max_coût_par_employé"], "Seuil A coût trop bas"
                assert 37.1 <= config["max_co2_par_employé_g"], "Seuil A CO₂ trop bas"
```

#### `tests/test_subscription_tracker.py`
**Nouveaux tests** :
```python
class TestSubscriptionDetection:
    def test_detect_chatgpt_plus(self):
        result = détecter_abonnements_ia("ChatGPT Plus", "", "")
        assert result["est_ia"] == True
        assert result["score_confiance"] >= 50
        
    def test_detect_github_copilot(self):
        result = détecter_abonnements_ia("GitHub Copilot", "", "")
        assert result["est_ia"] == True
        assert result["score_confiance"] >= 50
        
    def test_detect_midjourney(self):
        result = détecter_abonnements_ia("Midjourney", "", "")
        assert result["est_ia"] == True
        assert result["score_confiance"] >= 50
        
    def test_no_false_positive_mailchimp(self):
        result = détecter_abonnements_ia("Mailchimp", "", "")
        assert result["est_ia"] == False
        assert result["score_confiance"] < 50
        
    def test_no_false_positive_airtable(self):
        result = détecter_abonnements_ia("Airtable", "", "")
        assert result["est_ia"] == False
        assert result["score_confiance"] < 50
        
    def test_no_false_positive_gmail(self):
        result = détecter_abonnements_ia("Gmail", "", "")
        assert result["est_ia"] == False
        assert result["score_confiance"] < 50
        
    def test_alias_chatgptplus(self):
        result = détecter_abonnements_ia("ChatGPTPlus", "", "")
        assert result["est_ia"] == True
        assert "ChatGPT Plus" in result["correspondances"]
        
    def test_correction_manuelle(self):
        # Ajouter une correction pour Mailchimp
        add_correction("Mailchimp", "non_ia", "Test")
        result = detect_ai_subscriptions([{"Nom": "Mailchimp"}])
        assert result[0]["est_ia"] == False
        assert result[0]["source"] == "correction manuelle"
        # Nettoyer
        remove_correction("Mailchimp")

# Test du score de confiance
class TestConfidenceScore:
    def test_exact_match(self):
        score = calculer_score_confiance(["chatgpt"], ["chatgpt"], "chatgpt plus")
        assert score >= 50
        
    def test_partial_match(self):
        score = calculer_score_confiance(["gpt"], ["my", "gpt", "app"], "my gpt app")
        assert score >= 30
        
    def test_no_match(self):
        score = calculer_score_confiance([], ["mailchimp"], "mailchimp")
        assert score < 50
```

### 2. Tests d'Intégration

#### `tests/test_integration.py`
```python
class TestFullCalculation:
    def test_full_calculation_api(self):
        """Test un calcul complet pour une API"""
        # Données
        model = "GPT-4"
        input_tokens = 1000
        output_tokens = 500
        region = "France"
        
        # Calcul coût
        cost_result = calculate_api_cost(model, input_tokens, output_tokens, currency="EUR")
        
        # Calcul CO₂
        co2_result = calculate_api_carbon(model, input_tokens + output_tokens, region)
        
        # Vérifications
        assert cost_result["catégorie"] == "CERTAIN"
        assert co2_result["catégorie"] == "ESTIMÉ"
        assert cost_result["total_cost"] > 0
        assert co2_result["carbon_kg"] > 0
        
    def test_full_calculation_saas(self):
        """Test un calcul complet pour un SaaS"""
        # Données
        saas = "ChatGPT_Plus"
        usage_level = "moyen"
        region = "France"
        
        # Calcul coût
        cost_result = calculate_saas_cost(saas, period="mensuel")
        
        # Calcul CO₂
        co2_result = calculate_saas_carbon(saas, usage_level, region)
        
        # Vérifications
        assert cost_result["catégorie"] == "CERTAIN"
        assert co2_result["catégorie"] == "ESTIMÉ"
        
    def test_full_greenops_score(self):
        """Test un calcul complet de score GreenOps"""
        result = calculate_greenops_score(
            total_cost=100.0,
            total_carbon_g=500.0,
            number_of_employees=5,
            number_of_licenses=5,
            dormant_licenses_count=0
        )
        
        assert result["grade"] in ["A", "B", "C", "D", "E"]
        assert 0 <= result["score_greenops"] <= 100
        assert result["catégorie"] == "ESTIMÉ"

# Test des fourchettes
class TestUncertaintyPropagation:
    def test_co2_uncertainty(self):
        """Vérifie que l'incertitude CO₂ est correctement calculée"""
        result = calculate_api_carbon("GPT-4", 1000, region="France")
        
        # L'incertitude doit être > 0
        assert result["incertitude"] > "0%"
        
        # La fourchette doit être cohérente
        assert result["carbon_min_kg"] < result["carbon_kg"] < result["carbon_max_kg"]
        
    def test_cost_uncertainty_with_conversion(self):
        """Vérifie que la conversion de devise ajoute de l'incertitude"""
        result_usd = calculate_api_cost("Llama-3", 1000, 500, currency="USD")
        result_eur = calculate_api_cost("Llama-3", 1000, 500, currency="EUR")
        
        # Le coût en USD doit être CERTAIN
        assert result_usd["catégorie"] == "CERTAIN"
        
        # Le coût en EUR doit être ESTIMÉ (à cause de la conversion)
        assert result_eur["catégorie"] == "ESTIMÉ"
```

### 3. Tests de Validation

#### `tests/test_sources_validation.py`
```python
class TestSourcesValidation:
    def test_all_factors_have_uncertainty(self):
        """Vérifie que tous les facteurs ont min/max/incertitude"""
        sources = load_sources()
        
        for source_type, items in sources.items():
            if source_type in ["facteurs_co2", "pue", "taux_de_change", "équivalences"]:
                for item in items.values():
                    if isinstance(item, dict):
                        assert "valeur" in item
                        assert "min" in item
                        assert "max" in item
                        # L'incertitude peut être calculée ou stockée
                        assert "incertitude" in item or ("min" in item and "max" in item)
                        
    def test_no_homepage_urls(self):
        """Vérifie qu'aucune URL n'est une page d'accueil"""
        sources = load_sources()
        homepages = [
            "https://openai.com",
            "https://mistral.ai",
            "https://www.ademe.fr",
            "https://arxiv.org",
            "https://ecologits.ai",
            "https://github.com"
        ]
        
        for source_type, items in sources.items():
            for item in items.values():
                if isinstance(item, dict) and "url" in item:
                    url = item["url"]
                    for homepage in homepages:
                        assert not url.startswith(homepage), f"URL homepage détectée : {url}"
                        
    def test_all_sources_have_dates(self):
        """Vérifie que toutes les sources ont une date de consultation"""
        sources = load_sources()
        
        for source_type, items in sources.items():
            for item in items.values():
                if isinstance(item, dict):
                    assert "date_consultation" in item, f"Missing date in {source_type}"
                    # Format YYYY-MM-DD
                    assert re.match(r'\d{4}-\d{2}-\d{2}', item["date_consultation"])
                        
    def test_all_factors_have_status(self):
        """Vérifie que tous les facteurs ont un statut"""
        sources = load_sources()
        
        for source_type, items in sources.items():
            for item in items.values():
                if isinstance(item, dict):
                    assert "statut" in item, f"Missing statut in {source_type}"
                    assert item["statut"] in ["vérifié", "à vérifier"]
```

### 4. Tests de Non-Régression

**Exécuter tous les tests existants** pour s'assurer que les changements ne cassent rien :
```bash
pytest tests/ -v
```

---

## ❓ Décisions à Valider

### 1. Inclure les Embodied Impacts ?

| Option | Pour | Contre | Recommandation |
|--------|------|---------|----------------|
| **Oui** | Complétude de l'ACV, alignement avec EcoLogits | Complexité supplémentaire, impact marginal pour l'inférence | ❌ Non (par défaut) |
| **Non** | Simplicité, focus sur l'usage | Moins complet | ✅ **Oui (par défaut)** |

**Décision proposée** : **Exclure par défaut**, optionnel pour les utilisateurs avancés.

**Implémentation** :
- Ajouter un paramètre `include_embodied` (défaut: False) dans les fonctions de calcul
- Si `True`, ajouter le CO₂ embodied au CO₂ total
- **Affichage** : "CO₂ total : X kg (usage: Y kg, embodied: Z kg)"

---

### 2. Location-based vs Market-based

| Option | Description | Recommandation |
|--------|-------------|----------------|
| **Location-based** | Impact physique réel (ce que le réseau émet) | ✅ **Par défaut** |
| **Market-based** | Impact après achat de certificats verts | Optionnel |
| **Les deux** | Afficher les deux valeurs | ⭐ **Idéal** |

**Décision proposée** : **Location-based par défaut**, avec option pour Market-based.

**Implémentation** :
- Ajouter un paramètre `method` (défaut: "location-based") dans les fonctions de calcul
- Stocker les deux facteurs d'émission (location et market) pour chaque région
- **Affichage** : "CO₂ (location-based) : X kg | CO₂ (market-based) : Y kg"

---

### 3. Niveau de Détail par Défaut

| Niveau | Description | Public Cible | Recommandation |
|--------|-------------|--------------|----------------|
| **Simple** | Résultats finaux uniquement | Utilisateurs standards | ✅ **Par défaut** |
| **Avancé** | Détails des calculs, fourchettes, sources | Experts, auditeurs | Optionnel |

**Décision proposée** : **Simple par défaut**, avec option pour le mode avancé.

**Implémentation** :
- Ajouter un paramètre `detail_level` (défaut: "simple") dans l'UI
- **Simple** : Afficher uniquement les résultats finaux avec catégories
- **Avancé** : Afficher tous les détails (fourchettes, sources, formules)

---

### 4. Seuil de Confiance pour la Détection IA

| Seuil | Description | Recommandation |
|-------|-------------|----------------|
| 40 | Détection plus large (plus de vrais positifs, plus de faux positifs) | ❌ Trop bas |
| 50 | Équilibre | ✅ **Recommandé** |
| 60 | Détection plus stricte (moins de faux positifs, plus de faux négatifs) | ⚠️ À tester |

**Décision proposée** : **50** (comme dans la proposition actuelle).

**Test** : Vérifier les faux positifs/negatifs avec ce seuil avant validation.

---

### 5. Période d'Inactivité pour les Licences Dormantes

| Période | Description | Recommandation |
|---------|-------------|----------------|
| 15 jours | Court, détecte rapidement | ⚠️ Risque de faux positifs |
| 30 jours | Équilibre | ✅ **Recommandé** |
| 60 jours | Long, moins de faux positifs | ⚠️ Risque de faux négatifs |

**Décision proposée** : **30 jours** (standard dans l'industrie).

**Implémentation** :
- Paramètre configurable : `dormant_threshold_days` (défaut: 30)
- **Affichage** : "Licences dormantes : inactivité > 30 jours"

---

### 6. Gestion des Abonnements Annuels

| Option | Description | Recommandation |
|--------|-------------|----------------|
| **Ne jamais ×12** | Sécurité maximale | ✅ **Recommandé** |
| **×12 pour les mensuels** | Standard | ✅ **Recommandé** |
| **Estimer la période** | Basé sur le nom du SaaS | ⚠️ Risque d'erreur |

**Décision proposée** : **Ne jamais ×12 automatiquement**. La période doit être **explicitement spécifiée** dans les données.

**Implémentation** :
- Ajouter un champ `période` ("mensuel" ou "annuel") dans les données importées
- **Si période inconnue** : Afficher un avertissement et ne pas calculer les projections annuelles
- **Exemple** : "⚠️ Période inconnue pour cet abonnement. Impossible de calculer les économies annuelles."

---

## 📦 Résumé des Livrables

### Phase 3 (À valider)

| Livrable | Statut | Description |
|----------|--------|-------------|
| `docs/PROPOSITION_NOUVELLE_METHODE.md` | ✅ **Terminé** | Ce document |
| `config/sources.yaml` | ⏳ **À créer** | Tous les facteurs avec incertitudes |
| `config/corrections.yaml` | ⏳ **À créer** | Corrections manuelles (vide au départ) |

### Phase 4 (Après validation)

| Livrable | Priorité | Description |
|----------|----------|-------------|
| Mise à jour `utils/carbon_calculator.py` | ⭐⭐⭐ | Intégrer PUE, F_em, fourchettes |
| Mise à jour `utils/cost_calculator.py` | ⭐⭐⭐ | Gérer devises, périodes |
| Mise à jour `utils/greenops_scoring.py` | ⭐⭐⭐ | Nouveaux seuils, exclusion licences actives |
| Mise à jour `utils/subscription_tracker.py` | ⭐⭐⭐ | Nouvelle détection avec score de confiance |
| Création `utils/uncertainty.py` | ⭐⭐ | Calcul des incertitudes |
| Création `utils/detection_ia.py` | ⭐⭐ | Module de détection dédié |
| Mise à jour `app.py` | ⭐⭐⭐ | Intégrer nouvelles fonctions, afficher catégories |
| Mise à jour `utils/report_generator.py` | ⭐⭐ | Ajouter méthodologie dans PDF |
| Mise à jour `docs/METHODOLOGIE.md` | ⭐⭐⭐ | Documenter la nouvelle méthode |
| Mise à jour `tests/` | ⭐⭐⭐ | Ajouter tous les nouveaux tests |

### Validation

| Étape | Statut | Responsable |
|-------|--------|-------------|
| Valider cette proposition | ⏳ **En attente** | Utilisateur |
| Valider les décisions (1-6) | ⏳ **En attente** | Utilisateur |
| Créer `config/sources.yaml` | ⏳ **En attente** | Sobre Team |
| Implémenter les changements | ⏳ **En attente** | Sobre Team |
| Exécuter les tests | ⏳ **En attente** | Sobre Team |
| Valider les résultats | ⏳ **En attente** | Utilisateur |

---

## 🎯 Prochaines Étapes

1. **Valider cette proposition** (ce document)
2. **Valider les décisions** (1-6 ci-dessus)
3. **Créer `config/sources.yaml`** avec tous les facteurs vérifiés
4. **Implémenter les changements de code** (Phase 4)
5. **Exécuter les tests** et corriger les erreurs
6. **Valider les résultats** avec l'utilisateur

---

> **Dernière mise à jour** : 2024-11-01
> **Version** : 1.0
> **Auteur** : Sobre Team (avec assistance IA)
> **Licence** : MIT (comme le projet Sobre)

---

## 📄 Structure Complète de `config/sources.yaml`

Voir le fichier séparé `config/sources.yaml` (à créer) qui contient la structure complète avec tous les facteurs vérifiés.

**Résumé des sections** :
1. `facteurs_co2` - Facteurs CO₂ par million de tokens et par kWh
2. `pue` - Power Usage Effectiveness par fournisseur
3. `tarifs` - Tarifs des APIs et SaaS par token/mois
4. `taux_de_change` - Taux de change USD→EUR
5. `équivalences` - Équivalence voiture (kgCO₂/km)
6. `hypotheses_usage` - Niveaux d'usage pour les SaaS
7. `seuils_greenops` - Nouveaux seuils pour le score GreenOps
8. `mots_cles_ia` - Liste blanche et alias pour la détection
9. `plafonds_monetaires` - Plafonds pour les estimations monétaires
10. `metadata` - Métadonnées du fichier
