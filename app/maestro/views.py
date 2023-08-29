from maestro.models import Equipamiento, Institucion, Item, Medicamento, Quiebre
from maestro.serializers import EquipamientoSerializer, InstitucionSerializer, ItemSerializer, MedicamentoSerializer, QuiebreSerializer
from rest_framework import generics


class EquipamientoListCreateView(generics.ListCreateAPIView):
    queryset = Equipamiento.objects.all()
    serializer_class = EquipamientoSerializer

class EquipamientoRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipamiento.objects.all()
    serializer_class = EquipamientoSerializer

class InstitucionListCreateView(generics.ListCreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class InstitucionRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class MedicamentoListCreateView(generics.ListCreateAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class MedicamentoRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


class QuiebreListCreateView(generics.ListCreateAPIView):
    queryset = Quiebre.objects.all()
    serializer_class = QuiebreSerializer

class QuiebreRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiebre.objects.all()
    serializer_class = QuiebreSerializer