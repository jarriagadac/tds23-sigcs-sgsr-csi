from django.urls import include, path
from rest_framework import routers


from .views import (
    EquipamientoListCreateView,
    EquipamientoRetrieveDestroyView,
    InstitucionListCreateView,
    InstitucionRetrieveDestroyView, 
    ItemListCreateView,
    ItemRetrieveDestroyView, 
    MedicamentoListCreateView,
    MedicamentoRetrieveDestroyView, 
    QuiebreListCreateView,
    QuiebreRetrieveDestroyView
)


app_name = "maestro"
urlpatterns = [
    path("equipamiento", EquipamientoListCreateView.as_view(), name="equipamiento-lc"),
    path("equipamiento/<int:pk>",EquipamientoRetrieveDestroyView.as_view(), name="equipamiento-rud"),
    path("institucion", InstitucionListCreateView.as_view(), name="institucion-lc"),
    path("institucion/<int:pk>", InstitucionRetrieveDestroyView.as_view(), name="institucion-rud"),
    path("item", ItemListCreateView.as_view(), name="item-lc"),
    path("item/<int:pk>", ItemRetrieveDestroyView.as_view(), name="item-rud"),
    path("medicamento", MedicamentoListCreateView.as_view(), name="medicamento-lc"),
    path("medicamento/<int:pk>", MedicamentoRetrieveDestroyView.as_view(), name="medicamento-rud"),
    path("quiebre", QuiebreListCreateView.as_view(),name="quiebre-lc"),
    path("quiebre/<int:pk>", QuiebreRetrieveDestroyView.as_view(),name="quiebre-rud"),
]

