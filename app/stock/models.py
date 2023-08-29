from datetime import date

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import UniqueConstraint

from maestro.models import Quiebre


class Lote(models.Model):
    codigo = models.CharField(max_length=200, default="")
    medicamento = models.ForeignKey("maestro.Medicamento", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    fecha_vencimiento = models.DateField(null=True)

    def __str__(self):
        return self.codigo


class Consumo(models.Model):
    institucion = models.ForeignKey("maestro.Institucion", on_delete=models.CASCADE)
    medicamento = models.ForeignKey("maestro.Medicamento", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    fecha = models.DateField(default=date.today())


@receiver(post_save, sender=Consumo)
def callback_consumo(sender, instance, **kwargs):
    stock = Stock.objects.filter(institucion=instance.institucion, medicamento=instance.medicamento).first()
    quiebre = Quiebre.objects.filter(institucion=instance.institucion, medicamento=instance.medicamento).first()
    if stock is not None:
        cantidad = stock.cantidad - instance.cantidad
        stock.upd_cantidad(cantidad)
    if quiebre is not None:
        stock.upd_has_quiebre(quiebre.cantidad, cantidad)


class Movimiento(models.Model):
    institucion = models.ForeignKey("maestro.Institucion", on_delete=models.CASCADE)
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today())

    class Meta:
        unique_together = ["lote"]


@receiver(post_save, sender=Movimiento)
def callback_movimiento(sender, instance, **kwargs):
    today = date.today()
    stock = Stock.objects.filter(institucion=instance.institucion, medicamento=instance.lote.medicamento).first()
    quiebre = Quiebre.objects.filter(institucion=instance.institucion, medicamento=instance.lote.medicamento).first()
    if instance.lote.fecha_vencimiento > today and stock is not None:
        cantidad = instance.lote.cantidad + stock.cantidad
        stock.upd_cantidad(cantidad)
    if quiebre is not None:
        stock.upd_has_quiebre(quiebre.cantidad, cantidad)


class Stock(models.Model):
    institucion = models.ForeignKey("maestro.Institucion", on_delete=models.CASCADE)
    medicamento = models.ForeignKey("maestro.Medicamento", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    fecha_actualizacion = models.DateField(default=date.today())
    has_quiebre = models.BooleanField(default=False)

    class Meta:
        constraints = [UniqueConstraint(fields=["institucion", "medicamento"], name="unique_institucion_medicamento")]

    def upd_cantidad(self, cantidad):
        self.cantidad = cantidad
        self.save()

    def upd_has_quiebre(self, quiebre_value, cantidad):
        if cantidad <= quiebre_value:
            self.has_quiebre = True
        else:
            self.has_quiebre = False
        self.save()


@receiver(pre_save, sender=Stock)
def callback_quiebre(sender, instance, **kwargs):
    if instance._state.adding and not instance.has_quiebre:
        instance.has_quiebre = False


@receiver(pre_save, sender=Stock)
def callback_stock_cantidad(sender, instance, **kwargs):
    if instance._state.adding and not instance.cantidad:
        instance.cantidad = 0
