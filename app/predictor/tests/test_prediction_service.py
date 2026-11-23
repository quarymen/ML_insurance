from django.test import SimpleTestCase
from predictor.services import PredictionService, MockBundle


class PredictionServiceTests(SimpleTestCase):
    def test_mock_bundle_returns_correct_probability(self):
        """Проверяем, что заглушка выдает 0.5 и правильную версию."""
        bundle = MockBundle()
        payload = {"Age": 30, "Gender": "Male"}  # Заглушке все равно, какие данные

        result = bundle.predict(payload)

        self.assertEqual(result['probability'], 0.5)
        self.assertEqual(result['prediction'], 1)  # 0.5 >= 0.5
        self.assertEqual(result['model_version'], 'mock-0.0.1')

    def test_prediction_service_singleton(self):
        """Проверяем, что сервис загружается правильно."""
        service = PredictionService.load()
        self.assertIsInstance(service.bundle, MockBundle)