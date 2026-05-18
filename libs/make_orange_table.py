import logging
from Orange.data import Domain, DiscreteVariable, Table
from models.workoutInputModel import WorkoutInput

logger = logging.getLogger(__name__)


def make_orange_table(original_domain: Domain, data: WorkoutInput) -> Table:
    raw_values = {
        "age":                        data.age,
        "height_cm":                  data.height_cm,
        "weight_kg":                  data.weight_kg,
        "bmi":                        data.bmi,
        "body_fat_percentage":        data.body_fat_percentage,
        "resting_bpm":                data.resting_bpm,
        "target_timeline_weeks":      data.target_timeline_weeks,
        "fatigue_score":              data.fatigue_score,
        "workout_variety_preference": data.workout_variety_preference,
        "gender":                     data.gender,
        "health_goal":                data.health_goal,
        "fitness_level":              data.fitness_level,
        "has_gym_access":             str(data.has_gym_access),  # "True" / "False"
        "injury_type":                data.injury_type,
        "injury_severity":            data.injury_severity,
        "medical_condition":          data.medical_condition,
    }

    row = []
    for attr in original_domain.attributes:
        val = raw_values.get(attr.name)
        if val is None:
            logger.error(f"Feature manquante dans raw_values : '{attr.name}'")

        if isinstance(attr, DiscreteVariable):
            row.append(str(val) if val is not None else attr.values[0])
        else:
            row.append(float(val) if val is not None else 0.0)

    row.append(original_domain.class_var.values[0])  # classe factice
    return Table.from_list(original_domain, [row])
