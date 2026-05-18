# IA-training-recommendation-MSPR2

Microservice FastAPI pour recommandation d'entraînement basé sur deux modèles de réseaux de neurones.

## 🚀 Quick Start

### 1. Installation des dépendances

```bash
python3 -m pip install -r requirements.txt
```

### 2. Lancer l'API

```bash
python3 main.py
```

L'API sera accessible à `http://localhost:8000`

- **API Interactive**: http://localhost:8000/docs (Swagger UI)
- **Alternative**: http://localhost:8000/redoc (ReDoc)
- **Health Check**: http://localhost:8000/health

### 3. Effectuer une prédiction

**Endpoint**: `POST /predict`

#### Exemple de requête

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "gender": "Male",
    "height_cm": 180.0,
    "weight_kg": 75.0,
    "bmi": 23.1,
    "body_fat_percentage": 15.0,
    "resting_bpm": 65,
    "primary_goal": "muscle_gain",
    "target_timeline_weeks": 12,
    "fitness_level": "intermediate",
    "avg_session_duration_min": 60,
    "recent_fatigue_score": 5.0,
    "has_gym_access": true,
    "home_equipment": "none",
    "available_space_m2": 20.0,
    "available_days_per_week": 4,
    "preferred_session_duration_min": 60,
    "preferred_activities": "strength",
    "preferred_time_of_day": "morning",
    "workout_variety_preference": 6.0,
    "injury_type": "none",
    "injury_severity": "none",
    "medical_condition": "none",
    "fatigue_level": 4.0
  }'
```

#### Réponse

```json
{
  "recommended_program": "mixed_health_maintenance",
  "recommended_intensity": "moderate"
}
```

## 📋 Schéma des données

### Champs d'entrée

Tous les champs sont **obligatoires** et validés :

#### Numériques
- `age` (entier, > 0): Âge en années
- `height_cm` (float, > 0): Hauteur en centimètres
- `weight_kg` (float, > 0): Poids en kilogrammes
- `bmi` (float, > 0): Indice de masse corporelle
- `body_fat_percentage` (float, > 0): Pourcentage de masse grasse
- `resting_bpm` (entier, > 0): Fréquence cardiaque au repos (bpm)
- `target_timeline_weeks` (entier, > 0): Durée objectif en semaines
- `avg_session_duration_min` (entier, > 0): Durée moyenne de session (minutes)
- `recent_fatigue_score` (float, > 0): Score de fatigue récente
- `available_space_m2` (float, > 0): Espace disponible (m²)
- `available_days_per_week` (entier, > 0): Jours d'entraînement par semaine
- `preferred_session_duration_min` (entier, > 0): Durée préférée de session (minutes)
- `workout_variety_preference` (float, > 0): Préférence pour la variété (0-10)
- `fatigue_level` (float, > 0): Niveau de fatigue (0-10)

#### Catégorielles (énumérations strictes)
- `gender`: "Male" | "Female"
- `primary_goal`: "endurance" | "fat_loss" | "general_health" | "muscle_gain"
- `fitness_level`: "beginner" | "intermediate" | "advanced"
- `home_equipment`: "none" | "dumbbells" | "resistance_bands" | "barbell" | "full_home_gym"
- `preferred_time_of_day`: "morning" | "afternoon" | "evening"
- `injury_type`: "none" | "ankle" | "knee" | "back" | "shoulder" | "wrist"
- `injury_severity`: "none" | "mild" | "moderate" | "severe"
- `medical_condition`: "none" | "diabetes" | "hypertension" | "asthma" | "cardiac"

#### Booléenne
- `has_gym_access` (boolean): Accès à une salle de gym

#### Multi-valeur
- `preferred_activities` (string): Activités préférées séparées par virgule
  - Valeurs acceptées: "cardio", "hiit", "outdoor", "sport", "strength", "yoga"
  - Exemples: "strength", "strength,cardio", "yoga,outdoor"

### Sorties

- `recommended_program` (string): Programme d'entraînement recommandé
  - Valeurs possibles: 22 programmes différents
  - Exemples: "ppl_split_gym", "cardio_fat_burn", "yoga_mobility_balance", etc.

- `recommended_intensity` (string): Intensité recommandée
  - Valeurs possibles: "low", "moderate", "high"

## ✅ Validations

L'API effectue les validations suivantes sur chaque requête :

✓ **Aucun champ ne peut être NULL** - Erreur 422  
✓ **Aucun champ ne peut être NaN** - Erreur 422  
✓ **Les champs numériques doivent être > 0** - Erreur 422  
✓ **Les énumérations doivent correspondre exactement** - Erreur 422  
✓ **Les activités préférées doivent être valides** - Transformées automatiquement

## 🧪 Tests

Pour tester l'API :

```bash
python3 -m pip install requests
python3 test_api.py
```

## 🏗️ Architecture

```
.
├── main.py                                     # Microservice FastAPI
├── Neural_network_program_model_MSPR.pkcls    # Modèle programme (Orange ML)
├── Neural_network_intensity_model_MSPR.pkcls  # Modèle intensité (Orange ML)
├── healthai_coach_dataset.csv                 # Données d'entraînement
├── requirements.txt                           # Dépendances Python
├── test_api.py                               # Suite de tests
└── README.md                                  # Cette documentation
```

## 📦 Dépendances principales

- **FastAPI** 0.115+: Framework web asynchrone
- **Uvicorn** 0.27+: Serveur ASGI
- **Pydantic** 2.8+: Validation des schémas
- **Orange3** 3.39+: Modèles ML (Orange Canvas)
- **pandas** 2.2.2+: Manipulation des données
- **numpy** 1.26+: Calculs numériques
- **scikit-learn** 1.5+: Outils ML

## 🔄 Pipeline de traitement

1. **Réception** de la requête JSON
2. **Validation** Pydantic (type, énumération, plages de valeurs)
3. **Transformation** des 24 features brutes en 54 features one-hot encodées
4. **Prédiction** avec les deux modèles de réseaux de neurones
5. **Mapping** des indices de classe en noms lisibles
6. **Retour** des recommandations au format JSON

## ⚠️ Notes

- Les modèles Orange utilisent des indices de classe (0-21 pour programme, 0-2 pour intensité)
- Les données d'entrée sont transformées via one-hot encoding des variables catégorielles
- Les prédictions sont toujours déterministes pour les mêmes données d'entrée
- L'API est sans état - chaque requête est indépendante

## 📝 Exemple d'erreur de validation

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "age"],
      "msg": "Value error, Valeur ne peut pas être null",
      "input": null,
      "ctx": {"error": {}}
    }
  ]
}
```
