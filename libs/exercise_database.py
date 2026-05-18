import json
import os
import logging

logger = logging.getLogger(__name__)


class ExerciseDatabase:
    _instance = None
    _exercises = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExerciseDatabase, cls).__new__(cls)
            cls._instance._load_exercises()
        return cls._instance
    
    def _load_exercises(self):
        """Charge les exercices depuis le fichier JSON"""
        try:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'exercise_db.json'
            )
            with open(db_path, 'r', encoding='utf-8') as f:
                self._exercises = json.load(f)
            logger.info(f"Base de données chargée: {len(self._exercises)} exercices")
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la base de données: {e}")
            self._exercises = []
    
    def filter(self, programs: str = None, forbidden_injuries: str = None) -> list:
        """
        Filtre les exercices selon:
        - programs: le programme recommandé (ex: "fat_loss", "muscle_gain")
        - forbidden_injuries: l'injury à éviter (ex: "shoulder_moderate")
        
        Returns:
            Liste des exercices filtrés
        """
        result = self._exercises.copy()
        
        # Filtre par programme
        if programs:
            result = [
                ex for ex in result 
                if programs in ex.get('programs', [])
            ]
        
        # Filtre par injuries interdites
        if forbidden_injuries:
            result = [
                ex for ex in result 
                if forbidden_injuries not in ex.get('forbidden_injuries', [])
            ]
        
        return result
    
    def get_all(self) -> list:
        """Retourne tous les exercices"""
        return self._exercises.copy()
    
    def get_by_id(self, exercise_id: str) -> dict:
        """Récupère un exercice par son ID"""
        for ex in self._exercises:
            if ex.get('id') == exercise_id:
                return ex
        return None


# Singleton instance
db = ExerciseDatabase()
