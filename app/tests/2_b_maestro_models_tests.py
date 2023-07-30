import pytest
from django.db.utils import IntegrityError

@pytest.mark.django_db
def test_institucion_model():
    from maestro.models import Institucion
    institucion = Institucion.objects.create(
        nombre="BLA BLA 1",
        tipo = Institucion.Tipo.CENTRO_MEDICO,
        titularidad = Institucion.Titularidad.PUBLICO,
        num_camas_uti = 10,
        num_camas_uci = 10,
        factor = 1.3,
    )

    assert institucion.nombre == "BLA BLA 1"
    assert institucion.tipo == Institucion.Tipo.CENTRO_MEDICO
    assert institucion.titularidad == Institucion.Titularidad.PUBLICO
    assert institucion.num_camas_uci == 10
    assert institucion.num_camas_uti == 10
    assert str(institucion) == institucion.nombre, "se debe usar el nombre como representación str del objeto"
    institucion.delete()
    assert Institucion.objects.filter(id=institucion.id).first() is None, "elimina institucion"


@pytest.mark.django_db
def test_medicamento_model():
    from maestro.models import Medicamento
    medicamento = Medicamento.objects.create(
        nombre_comercial = "ASPIRINA",
        nombre_generico = "Ácido acetilsalicílico",
        ingredientes = "ácido acetilsalicílico, 500 mg. celulosa en polvo y almidón de maíz.",
        concentracion = "500 miligramos",
        forma_presentacion = Medicamento.FormaPresentacion.BLISTER,
        forma_farmaceutica = Medicamento.FormaFarmaceutica.TABLETAS,
        via_administracion = Medicamento.Via.ORAL,
        indicaciones_terapeuticas = "Indicaciones del Medicamento"
    )

    assert medicamento.nombre_comercial == "ASPIRINA"
    assert medicamento.forma_presentacion == Medicamento.FormaPresentacion.BLISTER
    assert medicamento.forma_farmaceutica == Medicamento.FormaFarmaceutica.TABLETAS
    assert medicamento.via_administracion == Medicamento.Via.ORAL
    



@pytest.mark.django_db
def test_item_model():
    from maestro.models import Item
    item = Item.objects.create(
        nombre = "Test Item",
        tipo = Item.Tipo.APOYO_MONITORIZACION,
    )

    assert item.nombre == "Test Item"
    assert item.tipo == Item.Tipo.APOYO_MONITORIZACION
    assert str(item) == f"{item.nombre} ({item.tipo})", "se debe usar el nombre y tipo del item como representacion del objecto"


@pytest.mark.django_db
def test_equipamiento_model():
    from maestro.models import Equipamiento, Item
    equipamiento = Equipamiento.objects.create(
        item = Item.objects.create(
            nombre = "Test Item",
            tipo = Item.Tipo.APOYO_MONITORIZACION
        ),
        marca = "Test Marca",
        modelo = "Test Modelo",
    )

    assert equipamiento.item.nombre == "Test Item"
    assert equipamiento.marca == "Test Marca"
    assert equipamiento.modelo == "Test Modelo"
    equipamiento.item.delete()
    assert Equipamiento.objects.filter(id=equipamiento.id).first() is None, "Eliminar equipamiento debe eliminar Item ne cascada"


@pytest.mark.django_db
def test_quiebre_model():
    from maestro.models import Quiebre,Medicamento,Institucion
    
    institucion = Institucion.objects.create(
            nombre="BLA BLA 1",
            tipo = Institucion.Tipo.CENTRO_MEDICO,
            titularidad = Institucion.Titularidad.PUBLICO,
            num_camas_uti = 10,
            num_camas_uci = 10,
            factor = 1.3,
        )
    medicamento = Medicamento.objects.create(
            nombre_comercial = "ASPIRINA",
            nombre_generico = "Ácido acetilsalicílico",
            ingredientes = "ácido acetilsalicílico, 500 mg. celulosa en polvo y almidón de maíz.",
            concentracion = "500 miligramos",
            forma_presentacion = Medicamento.FormaPresentacion.BLISTER,
            forma_farmaceutica = Medicamento.FormaFarmaceutica.TABLETAS,
            via_administracion = Medicamento.Via.ORAL,
            indicaciones_terapeuticas = "Indicaciones del Medicamento",
        )


    quiebre = Quiebre.objects.create(
        institucion = institucion,
        medicamento = medicamento,
        cantidad = 10,
    )

    
    assert quiebre.cantidad == 10
    assert quiebre.institucion.tipo == Institucion.Tipo.CENTRO_MEDICO

    
    with pytest.raises(IntegrityError) as exc_info:
        Quiebre.objects.create(
            institucion = institucion,
            medicamento = medicamento,
        )
    assert str(exc_info.value) == "UNIQUE constraint failed: maestro_quiebre.institucion_id, maestro_quiebre.medicamento_id", "error"
    
