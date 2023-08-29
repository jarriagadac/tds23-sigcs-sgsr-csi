from rest_framework import generics
from .models import Medicamento, Quiebre
from .serializers import MedicamentoSerializer, QuiebreSerializer


class MedicamentoListCreateView(generics.ListCreateAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


class MedicamentoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


class QuiebreListCreateView(generics.ListCreateAPIView):
    queryset = Quiebre.objects.all()
    serializer_class = QuiebreSerializer


class QuiebreRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Quiebre.objects.all()
    serializer_class = QuiebreSerializer
