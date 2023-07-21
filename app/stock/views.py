from .models import Movimiento, Consumo
from .serializers import MovimientoSerializer, ConsumoSerializer
from rest_framework import status, generics
from rest_framework.views import APIView


class MovimientoListCreateView(generics.ListCreateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

class MovimientoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer


class MovimientoLoteRetrieveView:
    pass


class MovimientoMedicamentoView:
    def get():
        pass


class ConsumoListCreateView(generics.ListCreateAPIView):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer


class ConsumoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer


class ConsumoMedicamentoView:
    def get():
        pass


# class DisponibilidadMedicamentoView(views.APIView):
#     pass
