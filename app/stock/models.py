"""Module que modela los objetos de negocio del sistema de stock"""
from typing import Iterable, Optional
from django.db import models 
from django.db import IntegrityError
from maestro.models import Medicamento, Institucion
from django.db.models.signals import post_save
from django.dispatch import receiver
from maestro.models import Quiebre
from datetime import date


class Lote(models.Model):
    """Clase representa un Lote"""
    codigo = models.CharField(max_length=255)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(max_length=255)
    fecha_vencimiento = models.DateField()

    def __str__(self) -> str:
        """Function imprime el objeto"""
        return self.codigo


class Consumo(models.Model):
    """Clase representa un consumo de stock"""
    institucion= models.ForeignKey(Institucion, on_delete=models.CASCADE)
    medicamento= models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(max_length=255)
    fecha = models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.cantidad >= 0:
            super(Consumo, self).save(*args, **kwargs)
        else:
            raise IntegrityError("consumo debe ser mayor o igual que cero")
        

class Stock(models.Model):
    """Clase representa el stock de un item/articulo"""
    institucion =  models.ForeignKey(Institucion, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    has_quiebre = models.BooleanField(default=False)
    fecha_actualizacion = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        print(f"{self.id} - institucion: {self.institucion.id} - medicamento: {self.medicamento.id} - cantidad: {self.cantidad} - has_quiebre:{self.has_quiebre} - fecha_actualizacion {self.fecha_actualizacion}")

   
    def upd_cantidad(self, cantidad):
      
        #print(f"pase por aqui:: upd_cantidad {cantidad}")
        self.cantidad = cantidad
        self.save(update_fields=["cantidad"]) 
        self.upd_has_quiebre()


    def upd_has_quiebre(self):
       
        #print(f"pase por aqui:: stock institucion {self.institucion_id} medicamento {self.medicamento_id}")
        
        quiebre = Quiebre.objects.filter(institucion_id = self.institucion_id).filter(medicamento_id = self.medicamento.id).first()
        print(type(quiebre))
        if quiebre is None:
            print("No hay quiebre para esta institución y medicamento.")
            quiebre = Quiebre.objects.create(
                institucion = Institucion.objects.filter(id=self.institucion.id).first(),
                medicamento = Medicamento.objects.filter(id=self.medicamento.id).first()
            )
        
        if(self.cantidad <= quiebre.cantidad):
            self.has_quiebre=True
        else:
            self.has_quiebre=False
        
        self.save(update_fields=["has_quiebre"])    
        



class Movimiento(models.Model):
    """Clase representa el registro de un movimiento de stock"""
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    
    def save(self, *args, **kwargs):
        """Funcion sobre-escribe save del modelo ORM Python"""
        mov = Movimiento.objects.filter(institucion_id=self.institucion.pk).filter(lote_id=self.lote.pk)

        if mov.count()==0:
            super(Movimiento, self).save(*args, **kwargs)
        else:
            raise IntegrityError(
                "UNIQUE constraint failed: stock_movimiento.lote_id"
                )

# method for updating
@receiver(post_save, sender=Movimiento, dispatch_uid="update_stock_count")
def update_stock(sender, instance, **kwargs):
    mov = instance
    stock_cant=0
    movimientos = Movimiento.objects.filter(institucion_id=mov.institucion.id).filter(lote__medicamento_id = mov.lote.medicamento.id)
    stock = Stock.objects.filter(institucion_id = mov.institucion_id).filter(medicamento_id = mov.lote.medicamento.id).first()

    if stock is not None:
        for m in movimientos:
            print(f"signals-test: id medicamento: {m.lote} - institucion {m.institucion.id}  fecha {m.lote.fecha_vencimiento} hoy:{date.today()}")
            if m.lote.fecha_vencimiento > date.today():
                stock_cant += m.lote.cantidad
        
        #print(f"signals-test: id mov: {mov.lote.medicamento.id} - institucion {mov.institucion.id} cant_stock: {stock_cant}")
        stock.upd_cantidad(stock_cant)

@receiver(post_save, sender=Consumo, dispatch_uid="update_stock_count_consumo")
def update_stock_consumo(sender, instance, **kwargs):
    consumo = instance
    stock_cant=0
    consumos = Consumo.objects.filter(institucion_id=consumo.institucion.id).filter(medicamento_id = consumo.medicamento.id)
    stock = Stock.objects.filter(institucion_id = consumo.institucion_id).filter(medicamento_id = consumo.medicamento.id).first()
    
    if stock is not None:
        for m in consumos:
            stock_cant += m.cantidad
        

        #print(f"signals-test: id medicamento: {consumo.medicamento.id} - institucion {consumo.institucion.id} consumo: {stock_cant}")

        stock.upd_cantidad(stock.cantidad - stock_cant)
        stock.upd_has_quiebre()



    