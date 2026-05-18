import pickle
import logging
from pathlib import Path
from collections import OrderedDict
from Orange.data import Domain, DiscreteVariable, ContinuousVariable, Table

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent

class ModelService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.program_model = None
            self.intensity_model = None
            self.program_classes = None
            self.intensity_classes = None
            self.program_original_domain = None
            self.intensity_original_domain = None
            self._initialized = True

    def _reconstruct_original_domain(self, model) -> Domain:
        categorical_groups = OrderedDict()
        continuous_attrs = []

        for attr in model.domain.attributes:
            name = attr.name
            if "=" in name:
                base, value = name.split("=", 1)
                if base not in categorical_groups:
                    categorical_groups[base] = []
                categorical_groups[base].append(value)
            else:
                continuous_attrs.append(ContinuousVariable(name))

        attrs = continuous_attrs[:]
        for base_name, values in categorical_groups.items():
            attrs.append(DiscreteVariable(base_name, values=values))

        return Domain(attrs, model.domain.class_var)

    def _get_working_domain(self, model) -> Domain:
        has_onehot = any("=" in attr.name for attr in model.domain.attributes)
        has_discrete = any(isinstance(attr, DiscreteVariable) for attr in model.domain.attributes)

        if has_onehot and not has_discrete:
            logger.info("Domain prétraité détecté → reconstruction du domain original")
            return self._reconstruct_original_domain(model)
        else:
            logger.info("Domain original détecté → utilisation directe")
            return model.domain

    def load_models(self):
        try:
            # with open(BASE_DIR / "IA_models/Tree_program_model_MSPR.pkcls", "rb") as f:
            with open(BASE_DIR / "IA_models/NeuNet_program_model_2_MSPR.pkcls", "rb") as f:
                self.program_model = pickle.load(f)
            self.program_classes = list(self.program_model.domain.class_var.values)
            logger.info("✓ Program model loaded")
        except Exception as e:
            logger.error(f"✗ Failed to load program model: {e}")
            raise

        try:
            # with open(BASE_DIR / "IA_models/Tree_intensity_model_MSPR.pkcls", "rb") as f:
            with open(BASE_DIR / "IA_models/NeuNet_intensity_model_2_MSPR.pkcls", "rb") as f:
                self.intensity_model = pickle.load(f)
            self.intensity_classes = list(self.intensity_model.domain.class_var.values)
            logger.info("✓ Intensity model loaded")
        except Exception as e:
            logger.error(f"✗ Failed to load intensity model: {e}")
            raise

        self.program_original_domain = self._get_working_domain(self.program_model)
        self.intensity_original_domain = self._get_working_domain(self.intensity_model)

    # Les getters
    def get_program_model(self):
        if self.program_model is None:
            self.load_models()
        return self.program_model
    
    def get_intensity_model(self):
        if self.intensity_model is None:
            self.load_models()
        return self.intensity_model
    
    def get_program_classes(self):
        if self.program_classes is None:
            self.load_models()
        return self.program_classes
    
    def get_intensity_classes(self):
        if self.intensity_classes is None:
            self.load_models()
        return self.intensity_classes
    
    def get_program_domain(self):
        if self.program_original_domain is None:
            self.load_models()
        return self.program_original_domain
    
    def get_intensity_domain(self):
        if self.intensity_original_domain is None:
            self.load_models()
        return self.intensity_original_domain