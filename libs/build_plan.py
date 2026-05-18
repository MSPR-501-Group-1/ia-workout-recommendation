import random

def build_plan(exercises, fitness_level, intensity):
            plan = []
            for ex in exercises:
                rep_mult = ex["intensity_modifier"][intensity]["rep_mult"]
                serie_mult = ex["intensity_modifier"][intensity]["serie_mult"]

                rep_count = ex["levels"][fitness_level]["rep"] * rep_mult
                serie_count = ex["levels"][fitness_level]["serie"] * serie_mult
                repos_count = ex["levels"][fitness_level]["repos"]

                plan.append({
                    "exercise": ex["name"],
                    "muscle_group": ex["muscle_group"],
                    "equipment": ex["equipment"],
                    "reps": round(rep_count),
                    "series": round(serie_count),
                    "repos": round(repos_count)
                })

            random.shuffle(plan)
            if intensity == "low":
                plan = plan[:3]
            elif intensity == "moderate":
                plan = plan[:5]
            else:
                plan = plan[:7]
            return plan