from django.shortcuts import render
from .models import RegenMeting
from .models import SensorData
from .serializers import SensorDataSerializer
from django.http import JsonResponse
from weerstation.tasks import running, stop_loop
from rest_framework import viewsets


from .models import RegenMeting
from .serializers import RegenMetingSerializer


def regen_data_view(request):
   
    data_per_dag = {}
    regenmetingen = RegenMeting.objects.all()

    for meting in regenmetingen:
        dag = meting.tijdstip.date().isoformat()  # Groepeer per dag
        uur = meting.tijdstip.hour  # Groepeer per uur
        if dag not in data_per_dag:
            data_per_dag[dag] = [0] * 24  # Voor elk uur van de dag
        data_per_dag[dag][uur] += meting.regenval  # Regenval optellen voor het uur

    return render(request, 'regendata.html', {'data_per_dag': data_per_dag})

def check_status(request):
    return JsonResponse({"running": running})

def stop_task(request):
    stop_loop()
    return JsonResponse({"message": "De lus is gestopt."})

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

class RegenMetingViewSet(viewsets.ModelViewSet):
    queryset = RegenMeting.objects.all()
    serializer_class = RegenMetingSerializer