from django import forms
from .schema import INPUT_SCHEMA

class InsuranceForm(forms.Form):
    Gender = forms.ChoiceField(choices=INPUT_SCHEMA['Gender']['choices'], label=INPUT_SCHEMA['Gender']['label'])
    Age = forms.IntegerField(min_value=INPUT_SCHEMA['Age']['min'], max_value=INPUT_SCHEMA['Age']['max'], label=INPUT_SCHEMA['Age']['label'])
    Driving_License = forms.ChoiceField(choices=INPUT_SCHEMA['Driving_License']['choices'], label=INPUT_SCHEMA['Driving_License']['label'])
    Region_Code = forms.FloatField(label=INPUT_SCHEMA['Region_Code']['label'])
    Previously_Insured = forms.ChoiceField(choices=INPUT_SCHEMA['Previously_Insured']['choices'], label=INPUT_SCHEMA['Previously_Insured']['label'])
    Vehicle_Age = forms.ChoiceField(choices=INPUT_SCHEMA['Vehicle_Age']['choices'], label=INPUT_SCHEMA['Vehicle_Age']['label'])
    Vehicle_Damage = forms.ChoiceField(choices=INPUT_SCHEMA['Vehicle_Damage']['choices'], label=INPUT_SCHEMA['Vehicle_Damage']['label'])
    Annual_Premium = forms.FloatField(min_value=INPUT_SCHEMA['Annual_Premium']['min'], label=INPUT_SCHEMA['Annual_Premium']['label'])
    Policy_Sales_Channel = forms.FloatField(label=INPUT_SCHEMA['Policy_Sales_Channel']['label'])
    Vintage = forms.IntegerField(label=INPUT_SCHEMA['Vintage']['label'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})