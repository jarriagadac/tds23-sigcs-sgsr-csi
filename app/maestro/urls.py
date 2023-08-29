from django.urls import path

from .views import (
    MedicamentoListCreateView,
    MedicamentoRetrieveDestroyView,
    QuiebreListCreateView,
    QuiebreRetrieveDestroyView,
)

app_name = "maestro"
urlpatterns = [
    path("medicamentos", MedicamentoListCreateView.as_view(), name="medicamentos-lc"),
    path("medicamentos/<int:pk>", MedicamentoRetrieveDestroyView.as_view(), name="medicamentos-rud"),
    path("quiebres", QuiebreListCreateView.as_view(), name="quiebres-lc"),
    path("quiebres/<int:pk>", QuiebreRetrieveDestroyView.as_view(), name="medicamentos-rud"),
]
