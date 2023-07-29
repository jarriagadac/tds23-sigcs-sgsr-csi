import pytest

from django.core.management import call_command

from django.db.models.signals import post_save
from stock.models import Movimiento, Consumo, Stock
from stock.models import callback_movimiento, callback_consumo, callback_quiebre, callback_stock_cantidad


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        post_save.disconnect(callback_movimiento, sender=Movimiento)
        post_save.disconnect(callback_consumo, sender=Consumo)
        post_save.disconnect(callback_quiebre, sender=Stock)
        post_save.disconnect(callback_stock_cantidad, sender=Stock)

        call_command("loaddata", "_fixtures/maestro_institucion.json")
        call_command("loaddata", "_fixtures/maestro_medicamento.json")
        call_command("loaddata", "_fixtures/maestro_item.json")
        call_command("loaddata", "_fixtures/maestro_equipamiento.json")
        call_command("loaddata", "_fixtures/maestro_quiebre.json")

        try:
            call_command("loaddata", "_fixtures/stock.json")
        except Exception:
            pass

        post_save.connect(callback_movimiento, sender=Movimiento)
        post_save.connect(callback_consumo, sender=Consumo)
        post_save.connect(callback_quiebre, sender=Stock)
        post_save.connect(callback_stock_cantidad, sender=Stock)
