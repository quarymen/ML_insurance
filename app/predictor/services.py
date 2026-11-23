class MockBundle:
    """Заглушка, которая всегда выдает вероятность 0.5 (по ТЗ)"""
    version = "mock-0.0.1"
    threshold = 0.5

    def predict(self, payload: dict) -> dict:
        prob = 0.5  # Пока модель не готова, отдаем 50%
        return {
            "probability": prob,
            "prediction": int(prob >= self.threshold),
            "model_version": self.version
        }


class PredictionService:
    def __init__(self, bundle):
        self.bundle = bundle

    @classmethod
    def load(cls, path=None):
        # TODO: когда появится model_bundle.joblib, здесь будет joblib.load(path)
        return cls(MockBundle())

    def predict(self, payload: dict) -> dict:
        return self.bundle.predict(payload)


# Создаем единственный экземпляр сервиса при старте
_service_instance = None


def get_service():
    global _service_instance
    if _service_instance is None:
        _service_instance = PredictionService.load()
    return _service_instance