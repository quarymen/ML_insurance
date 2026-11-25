from django.http import JsonResponse
from django.shortcuts import render
from .forms import InsuranceForm
from .services import get_service


def predict_view(request):
    form = InsuranceForm(request.POST or None)
    result = None

    if request.method == 'POST' and form.is_valid():
        payload = form.cleaned_data
        service = get_service()
        result = service.predict(payload)

        # Добавляем удобный процент для вывода в HTML (0.5 -> 50.0)
        result['probability_percent'] = round(result['probability'] * 100, 1)

    return render(request, 'predictor/predict.html', {
        'form': form,
        'result': result
    })

def health_check(request):
    return JsonResponse({"status": "ok", "model_version": "mock-0.0.1"})