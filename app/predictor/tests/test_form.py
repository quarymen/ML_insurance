from django.test import TestCase
from predictor.forms import InsuranceForm

class InsuranceFormTests(TestCase):
    def test_valid_form(self):
        """Форма должна быть валидной с правильными данными."""
        valid_data = {
            'Gender': 'Male',
            'Age': 30,
            'Driving_License': 1,
            'Region_Code': 28.0,
            'Previously_Insured': 0,
            'Vehicle_Age': '1-2 Year',
            'Vehicle_Damage': 'Yes',
            'Annual_Premium': 30000.0,
            'Policy_Sales_Channel': 152.0,
            'Vintage': 150
        }
        form = InsuranceForm(data=valid_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_invalid_age(self):
        """Форма должна отклонять возраст меньше 18 лет."""
        invalid_data = {
            'Gender': 'Male',
            'Age': 10, # Невалидный возраст
            'Driving_License': 1,
            'Region_Code': 28.0,
            'Previously_Insured': 0,
            'Vehicle_Age': '1-2 Year',
            'Vehicle_Damage': 'Yes',
            'Annual_Premium': 30000.0,
            'Policy_Sales_Channel': 152.0,
            'Vintage': 150
        }
        form = InsuranceForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Age', form.errors) # Ошибка должна быть именно в поле Age

    def test_empty_form(self):
        """Пустая форма не должна проходить валидацию."""
        form = InsuranceForm(data={})
        self.assertFalse(form.is_valid())
        # У нас 10 обязательных полей, значит должно быть 10 ошибок
        self.assertEqual(len(form.errors), 10)