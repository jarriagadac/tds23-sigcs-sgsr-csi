from datetime import date
from django.db import models
from django.db.models.signals import pre_save
from django.db import IntegrityError
from django.dispatch import receiver
from django.db.models import UniqueConstraint


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


@receiver(pre_save, sender=Consumo)
def callback_consumo_cantidad(sender, instance, **kwargs):
    if instance.cantidad < 0:
        raise IntegrityError("consumo debe ser mayor o igual que cero")


class Stock(models.Model):
    institucion = models.ForeignKey("maestro.Institucion", on_delete=models.CASCADE)
    medicamento = models.ForeignKey("maestro.Medicamento", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    quiebre = models.OneToOneField("maestro.Quiebre", on_delete=models.SET_NULL, null=True, blank=True)
    fecha_actualizacion = models.DateField(default=date.today())
    has_quiebre = models.BooleanField(default=False)

    class Meta:
        constraints = [UniqueConstraint(fields=['institucion', 'medicamento'], name='unique_institucion_medicamento')]


@receiver(pre_save, sender=Stock)
def callback_quiebre(sender, instance, **kwargs):
    if instance._state.adding:
        instance.quiebre = None
        instance.has_quiebre = False


@receiver(pre_save, sender=Stock)
def callback_stock_cantidad(sender, instance, **kwargs):
    if instance._state.adding:
        instance.cantidad = 0


class Movimiento(models.Model):
    institucion = models.ForeignKey("maestro.Institucion", on_delete=models.CASCADE)
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today())

    class Meta:
        unique_together = ["lote"]
