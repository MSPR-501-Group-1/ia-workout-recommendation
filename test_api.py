#!/usr/bin/env python3
"""
Script de test pour l'API de recommandation d'entraînement.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test le health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    assert response.status_code == 200

def test_predict_valid():
    """Test une prédiction avec données valides."""
    print("Testing /predict endpoint with valid data...")
    
    payload = {
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
        "has_gym_access": True,
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
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    assert response.status_code == 200
    assert "recommended_program" in response.json()
    assert "recommended_intensity" in response.json()

def test_predict_invalid_null():
    """Test avec données null (doit échouer)."""
    print("Testing /predict endpoint with NULL data...")
    
    payload = {
        "age": None,  # Invalide
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
        "has_gym_access": True,
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
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    assert response.status_code == 422  # Validation error

def test_predict_invalid_enum():
    """Test avec valeur enum invalide (doit échouer)."""
    print("Testing /predict endpoint with invalid ENUM...")
    
    payload = {
        "age": 30,
        "gender": "Unknown",  # Invalide (doit être Male ou Female)
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
        "has_gym_access": True,
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
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    print("=" * 60)
    print("Fitness AI Coach API - Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_health()
        test_predict_valid()
        test_predict_invalid_null()
        test_predict_invalid_enum()
        
        print("✓ All tests passed!")
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API. Is it running on http://localhost:8000?")
