import pytest
from Orange.data import Domain, DiscreteVariable, ContinuousVariable

from services.model_service import ModelService


@pytest.fixture(autouse=True)
def reset_model_service_singleton():
    ModelService._instance = None
    yield
    ModelService._instance = None


def test_reconstruct_original_domain_builds_discrete_grouping():
    model_service = ModelService()

    attrs = [
        ContinuousVariable("age"),
        ContinuousVariable("gender=Male"),
        ContinuousVariable("gender=Female"),
        ContinuousVariable("height_cm"),
    ]
    class_var = DiscreteVariable("program", values=["a", "b"])
    onehot_domain = Domain(attrs, class_var)

    DummyModel = type("DummyModel", (), {"domain": onehot_domain})

    reconstructed = model_service._reconstruct_original_domain(DummyModel())

    assert [attr.name for attr in reconstructed.attributes] == [
        "age",
        "height_cm",
        "gender",
    ]
    gender_attr = reconstructed.attributes[-1]
    assert isinstance(gender_attr, DiscreteVariable)
    assert gender_attr.values == ("Male", "Female")


def test_get_working_domain_returns_original_when_discrete_present():
    model_service = ModelService()

    attrs = [
        ContinuousVariable("age"),
        DiscreteVariable("gender", values=["Male", "Female"]),
    ]
    class_var = DiscreteVariable("program", values=["a", "b"])
    domain = Domain(attrs, class_var)

    DummyModel = type("DummyModel", (), {"domain": domain})

    working = model_service._get_working_domain(DummyModel())
    assert working is domain


def test_get_working_domain_reconstructs_onehot_domain():
    model_service = ModelService()

    attrs = [
        ContinuousVariable("age"),
        ContinuousVariable("gender=Male"),
        ContinuousVariable("gender=Female"),
    ]
    class_var = DiscreteVariable("program", values=["a", "b"])
    onehot_domain = Domain(attrs, class_var)
    DummyModel = type("DummyModel", (), {"domain": onehot_domain})

    working = model_service._get_working_domain(DummyModel())

    assert [attr.name for attr in working.attributes] == ["age", "gender"]
    assert isinstance(working.attributes[1], DiscreteVariable)
    assert working.attributes[1].values == ("Male", "Female")


def test_getters_trigger_load_models_once(monkeypatch):
    model_service = ModelService()
    calls = {"count": 0}

    def fake_load_models():
        calls["count"] += 1
        model_service.program_model = object()
        model_service.intensity_model = object()
        model_service.program_classes = ["a", "b"]
        model_service.intensity_classes = ["low", "high"]
        model_service.program_original_domain = "program-domain"
        model_service.intensity_original_domain = "intensity-domain"

    monkeypatch.setattr(model_service, "load_models", fake_load_models)

    assert model_service.get_program_model() is model_service.program_model
    assert model_service.get_intensity_model() is model_service.intensity_model
    assert model_service.get_program_classes() == ["a", "b"]
    assert model_service.get_intensity_classes() == ["low", "high"]
    assert model_service.get_program_domain() == "program-domain"
    assert model_service.get_intensity_domain() == "intensity-domain"
    assert calls["count"] == 1


def test_load_models_populates_models(monkeypatch):
    import io
    from contextlib import contextmanager

    model_service = ModelService()

    program_domain = Domain(
        [ContinuousVariable("age")],
        DiscreteVariable("program", values=["a", "b"]),
    )
    intensity_domain = Domain(
        [ContinuousVariable("age")],
        DiscreteVariable("intensity", values=["low", "high"]),
    )

    class DummyModel:
        def __init__(self, domain):
            self.domain = domain

    models = [DummyModel(program_domain), DummyModel(intensity_domain)]

    def fake_pickle_load(_):
        return models.pop(0)

    @contextmanager
    def fake_open(*_args, **_kwargs):
        yield io.BytesIO(b"dummy")

    monkeypatch.setattr("services.model_service.pickle.load", fake_pickle_load)
    monkeypatch.setattr("builtins.open", fake_open)

    model_service.load_models()

    assert model_service.program_model is not None
    assert model_service.intensity_model is not None
    assert model_service.program_classes == ["a", "b"]
    assert model_service.intensity_classes == ["low", "high"]
    assert model_service.program_original_domain is program_domain
    assert model_service.intensity_original_domain is intensity_domain
