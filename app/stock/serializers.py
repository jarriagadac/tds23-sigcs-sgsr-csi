from rest_framework import serializers

from .models import Consumo, Stock, Lote, Movimiento

class ConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = [
            "id",
            "institucion",
            "medicamento",
            "cantidad",
            "fecha",
        ]

class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = [
            "id",
            "codigo",
            "medicamento",
            "cantidad",
            "fecha_vencimiento",
        ]

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "institucion",
            "medicamento",
            "cantidad",
            "has_quiebre",
            "fecha_actualizacion"
        ]

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        
        fields = [
            "id",
            "institucion",
            "lote",
            "fecha",
        ]

    def validate_lote(self, value):
        mov = Movimiento.objects.filter(lote_id=value)
        #breakpoint()
        if mov.count()>0:
            raise serializers.ValidationError('Ya existe movimiento con este lote.', 'unique')
        else:
            return value
         