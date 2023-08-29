from datetime import date

from maestro.models import Quiebre
from rest_framework import generics, views, response

from .models import Movimiento, Consumo, Stock, Lote
from .serializers import MovimientoSerializer, ConsumoSerializer, LoteSerializer


class MovimientoListCreateView(generics.ListCreateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer


class MovimientoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer


class MovimientoLoteRetrieveView:
    pass


class MovimientoMedicamentoAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        medicamento_id = self.kwargs.get("medicamento")
        if medicamento_id is not None:
            movimientos = (
                Movimiento.objects.filter(lote__medicamento=medicamento_id)
                .values("lote__medicamento", "lote", "institucion", "fecha")
                .order_by("fecha")
            )
        else:
            movimientos = Movimiento.objects.all().values("lote__medicamento", "lote", "institucion", "fecha").order_by("fecha")
        data = {}

        for movimiento in movimientos:
            medicamento_id = movimiento["lote__medicamento"]
            if medicamento_id not in data:
                data[medicamento_id] = {"medicamento": medicamento_id, "movimientos": []}
            data[medicamento_id]["movimientos"].append(
                {"lote": movimiento["lote"], "institucion": movimiento["institucion"], "fecha": movimiento["fecha"]}
            )

        return response.Response(list(data.values()))


class ConsumoListCreateView(generics.ListCreateAPIView):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer


class ConsumoRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer


class ConsumoMedicamentoAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        medicamento_id = kwargs.get("medicamento")
        if medicamento_id is not None:
            consumos = (
                Consumo.objects.filter(medicamento_id=medicamento_id)
                .values("medicamento", "cantidad", "institucion", "fecha")
                .order_by("medicamento")
            )
        else:
            consumos = Consumo.objects.all().values("medicamento", "cantidad", "institucion", "fecha").order_by("medicamento")
        data = {}

        for consumo in consumos:
            medicamento_id = consumo["medicamento"]
            if medicamento_id not in data:
                data[medicamento_id] = {"medicamento": medicamento_id, "cantidad": 0, "consumos": []}
            data[medicamento_id]["cantidad"] += consumo["cantidad"]
            data[medicamento_id]["consumos"].append(
                {"institucion": consumo["institucion"], "cantidad": consumo["cantidad"], "fecha": consumo["fecha"]}
            )

        return response.Response(data)


class DisponibilidadMedicamentoAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        medicamento_id = self.kwargs.get("medicamento")
        if medicamento_id is not None:
            stocks = Stock.objects.filter(medicamento_id=medicamento_id).values("medicamento", "institucion", "cantidad")
        else:
            stocks = Stock.objects.all().values("medicamento", "institucion", "cantidad")
        data = {}

        for stock in stocks:
            medicamento_id = stock["medicamento"]
            if medicamento_id not in data:
                data[medicamento_id] = {"medicamento": medicamento_id, "cantidad": 0, "stocks": []}
            data[medicamento_id]["cantidad"] += stock["cantidad"]
            data[medicamento_id]["stocks"].append(
                {
                    "institucion": stock["institucion"],
                    "cantidad": stock["cantidad"],
                }
            )

        return response.Response(data)


class QuiebreStockAPIView(views.APIView):
    def get(self, request):
        stocks = Stock.objects.filter(has_quiebre=True)
        quiebres = Quiebre.objects.values("institucion_id", "medicamento_id", "cantidad")
        quiebre_dict = {(q["institucion_id"], q["medicamento_id"]): q["cantidad"] for q in quiebres}
        data = []

        for stock in stocks:
            key = (stock.institucion_id, stock.medicamento_id)
            data.append(
                {
                    "institucion": stock.institucion_id,
                    "medicamento": stock.medicamento_id,
                    "stock": stock.cantidad,
                    "quiebre": quiebre_dict.get(key, 0),
                }
            )

        return response.Response(data)


class AlertaCaducidadLoteAPIView(views.APIView):
    def get(self, request):
        today = date.today()
        lotes = Lote.objects.filter(fecha_vencimiento__lt=today)
        serializer = LoteSerializer(lotes, many=True)
        return response.Response(serializer.data)
