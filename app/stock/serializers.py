from rest_framework import serializers

from .models import Lote, Consumo, Stock, Movimiento


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ["id", "codigo", "medicamento", "cantidad", "fecha_vencimiento"]


class ConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = ["id", "institucion", "medicamento", "cantidad", "fecha"]


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "institucion", "medicamento", "cantidad", "has_quiebre", "fecha_actualizacion"]


class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = ["id", "institucion", "lote", "fecha"]
        error_messages = {
            "lote": {
                "unique_together": "Ya existe movimiento con este lote.",
            }
        }

    def validate_lote(self, value):
        if Movimiento.objects.filter(lote=value).exists():
            raise serializers.ValidationError("Ya existe movimiento con este lote.", code="unique")
        return value
