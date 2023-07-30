from stock.models import Movimiento
from stock.models import Consumo
from stock.models import Stock
from stock.models import Quiebre
from stock.models import Lote
from stock.serializers import MovimientoSerializer
from stock.serializers import ConsumoSerializer
from rest_framework import generics
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date



class MovimientoListCreateView(generics.ListCreateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer


class MovimientoRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer


#class MovimientoLoteRetrieveView:
#    pass


#class MovimientoMedicamentoView:
#    def get():
#        pass


class ConsumoListCreateView(generics.ListCreateAPIView):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer


class ConsumoRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer

class MovimientoMedicamentoView(APIView):

    def get(self, request, medicamento=None, format=None):
        
        movs = Movimiento.objects.all()
        if medicamento is not None:
            movs = movs.filter(lote__medicamento_id = medicamento)
        
        datas = []
        for m in movs:
            data = {}
            if m.lote.medicamento.id is not data:
                data= {
                    "medicamento": m.lote.medicamento.id,
                    "movimientos": []
                }
            data["movimientos"].append({
                "lote": m.lote.id,
                "institucion": m.institucion.id,
                "fecha": m.fecha,
            })
            datas.append(data)

        print(f"data: {datas} list(data) : {list(datas)} len {len(datas)}")

        #{'medicamento': 5, 'movimientos': [{'fecha': datetime.date(2023, 7, 28), 'institucion': 1, 'lote': 20}]}


        return Response(datas)

class ConsumoMedicamentoAPIView(APIView):  

    def get(self, request, medicamento=None, format=None):
        consumos = Consumo.objects.all()
        if medicamento is not None:
            consumos = consumos.filter(medicamento__id = medicamento)
        data = {}
        for c in consumos:
            if c.medicamento.id not in data:
                data[c.medicamento.id]={
                    "medicamento": c.medicamento.id,
                    "cantidad": 0,
                    "consumos": [],
                }
            data[c.medicamento.id]["cantidad"] += c.cantidad
            data[c.medicamento.id]["consumos"].append({
                "institucion": c.institucion.id,
                "cantidad": c.cantidad,
                "fecha": c.fecha,
            })
        
        return Response(data)


class QuiebreStockAPIView(APIView):    
    def get(self, request, format=None):
        stocks = Stock.objects.all()
        print(f"cant: {stocks.count()}")

        datas = []
    
        for s in stocks:
            quiebre = Quiebre.objects.filter(medicamento_id=s.medicamento.id).filter(institucion_id=s.institucion.id).first()
            data={
                "institucion": s.institucion.id,
                "medicamento": s.medicamento.id,
                "stock": s.cantidad,
                "quiebre": quiebre.cantidad,
            }
            datas.append(data)
        
        print(f"data: {datas} list(data) : {list(datas)} len {len(datas)}")
        return Response(datas)

class AlertaCaducidadLoteAPIView(APIView):    
    def get(self, request, format=None):
        lotes = Lote.objects.all()
        datas=[]
        for m in lotes:
            if m.fecha_vencimiento < date.today():
                data = {
                    "id": m.id,
                    "codigo": m.codigo,
                    "medicamento": m.medicamento.id,
                    "cantidad": m.cantidad,
                    "fecha_vencimiento": m.fecha_vencimiento.strftime("%Y-%m-%d"),
                }
                datas.append(data)

        print(f"data: {datas}")
        return Response(datas)

class DisponibilidadMedicamentoAPIView(APIView):
    def get(self, request, medicamento=None, format=None):
        stock = Stock.objects.all()
        if medicamento is not None:
            stock = stock.filter(medicamento__id = medicamento)
        data = {}
        for c in stock:
             if c.medicamento.id not in data:
                 data[c.medicamento.id]={
                     "medicamento": c.medicamento.id,
                     "cantidad": 0,
                     "stocks":[],
                 }
             data[c.medicamento.id]["cantidad"] += c.cantidad
             data[c.medicamento.id]["stocks"].append({
                "institucion": c.institucion.id,
                "cantidad": c.cantidad,               
            })
        return Response(data)
      