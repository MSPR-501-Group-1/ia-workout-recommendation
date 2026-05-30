from types import SimpleNamespace

from services.prediction_service import PredictionService
from models.workoutInputModel import WorkoutInput


def test_predict_returns_response_and_uses_dependencies(monkeypatch):
    input_data = WorkoutInput(
        age=30,
        gender="Male",
        height_cm=180.0,
        weight_kg=75.0,
        bmi=23.1,
        body_fat_percentage=15.0,
        resting_bpm=65,
        health_goal="muscle_gain",
        target_timeline_weeks=12,
        fitness_level="intermediate",
        fatigue_score=5.0,
        has_gym_access=True,
        workout_variety_preference=6.0,
        injury_type="knee",
        injury_severity="mild",
        medical_condition="none",
    )

    calls = {
        "program_table": None,
        "intensity_table": None,
        "filter_args": None,
        "build_plan_args": None,
    }

    def fake_make_orange_table(domain, data):
        if domain == "program-domain":
            calls["program_table"] = True
            return "program-table"
        calls["intensity_table"] = True
        return "intensity-table"

    def fake_program_model(table):
        assert table == "program-table"
        return [1]

    def fake_intensity_model(table):
        assert table == "intensity-table"
        return [0]

    fake_model_service = SimpleNamespace(
        get_program_domain=lambda: "program-domain",
        get_intensity_domain=lambda: "intensity-domain",
        get_program_model=lambda: fake_program_model,
        get_intensity_model=lambda: fake_intensity_model,
        get_program_classes=lambda: ["fat_loss", "muscle_gain"],
        get_intensity_classes=lambda: ["low", "high"],
    )

    class DummyDb:
        def filter(self, programs=None, forbidden_injuries=None):
            calls["filter_args"] = (programs, forbidden_injuries)
            return [
                {
                    "name": "Pushup",
                    "muscle_group": "chest",
                    "equipment": "bodyweight",
                    "levels": {"intermediate": {"rep": 10, "serie": 3, "repos": 60}},
                    "intensity_modifier": {
                        "low": {"rep_mult": 1, "serie_mult": 1},
                        "high": {"rep_mult": 1.5, "serie_mult": 1.5},
                    },
                }
            ]

    def fake_build_plan(exercises, fitness_level, intensity):
        calls["build_plan_args"] = (exercises, fitness_level, intensity)
        return [
            {
                "exercise": "Pushup",
                "muscle_group": "chest",
                "equipment": "bodyweight",
                "reps": 10,
                "series": 3,
                "repos": 60,
            }
        ]

    monkeypatch.setattr("services.prediction_service.make_orange_table", fake_make_orange_table)
    monkeypatch.setattr("services.prediction_service.model_service", fake_model_service)
    monkeypatch.setattr("services.prediction_service.db", DummyDb())
    monkeypatch.setattr("services.prediction_service.build_plan", fake_build_plan)

    response = PredictionService.predict(input_data)

    assert response.recommended_program == "muscle_gain"
    assert response.recommended_intensity == "low"
    assert len(response.recommended_plan) == 1
    assert calls["program_table"] is True
    assert calls["intensity_table"] is True
    assert calls["filter_args"] == ("muscle_gain", "knee_mild")
    assert calls["build_plan_args"][1:] == ("intermediate", "low")
