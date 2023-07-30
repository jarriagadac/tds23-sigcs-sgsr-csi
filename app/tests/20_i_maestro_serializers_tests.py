import pytest
import json

@pytest.mark.django_db
def test_institucion_serializer():
    from maestro.serializers import InstitucionSerializer
    from maestro.models import Institucion
    institucion = Institucion.objects.create(
        nombre="BLA BLA 1",
        tipo = Institucion.Tipo.CENTRO_MEDICO,
        titularidad = Institucion.Titularidad.PUBLICO,
        num_camas_uti = 10,
        num_camas_uci = 10,
        factor = 1.3,
    )

    data = {
        "id": institucion.id,
        "nombre" : institucion.nombre,
        "tipo": institucion.tipo,
        "titularidad": institucion.titularidad,
        "num_camas_uti": institucion.num_camas_uti,
        "num_camas_uci": institucion.num_camas_uci,
        "factor": institucion.factor,
    }

    serialized_data = InstitucionSerializer(data=data)
    serialized_object = InstitucionSerializer(institucion)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el mismo orden"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"


@pytest.mark.django_db
def test_medicamento_serializer():
    from maestro.serializers import MedicamentoSerializer
    from maestro.models import Medicamento
    medicamento = Medicamento.objects.create(
        nombre_comercial = "ASPIRINA",
        nombre_generico = "Ácido acetilsalicílico",
        ingredientes = "ácido acetilsalicílico, 500 mg. celulosa en polvo y almidón de maíz.",
        concentracion = "500 miligramos",
        forma_presentacion = Medicamento.FormaPresentacion.BLISTER,
        forma_farmaceutica = Medicamento.FormaFarmaceutica.TABLETAS,
        via_administracion = Medicamento.Via.ORAL,
        indicaciones_terapeuticas = "Indicaciones del Medicamento",
        fabricante = "Bayer",
        
    )

    data = {
        "id" : medicamento.id,
        "nombre_comercial": medicamento.nombre_comercial,
        "nombre_generico" : medicamento.nombre_generico,
        "ingredientes": medicamento.ingredientes,
        "concentracion": medicamento.concentracion,
        "forma_presentacion": medicamento.forma_presentacion,
        "forma_farmaceutica": medicamento.forma_farmaceutica,
        "via_administracion": medicamento.via_administracion,
        "indicaciones_terapeuticas": medicamento.indicaciones_terapeuticas,
        "contraindicaciones": medicamento.contraindicaciones,
        "efectos_secundarios": medicamento.efectos_secundarios,
        "instrucciones_dosificacion": medicamento.instrucciones_dosificacion,
        "fabricante": medicamento.fabricante,
        "informacion_almacenamiento": medicamento.informacion_almacenamiento,
        "interacciones_medicamentosas": medicamento.interacciones_medicamentosas,
    }

    serialized_data = MedicamentoSerializer(data=data)
    serialized_object = MedicamentoSerializer(medicamento)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el mismo orden"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"



@pytest.mark.django_db
def test_item_serializer():
    from maestro.serializers import ItemSerializer
    from maestro.models import Item

    item = Item.objects.create(
        nombre = "Test Item",
        tipo = Item.Tipo.APOYO_MONITORIZACION,
    )

    data = {
        "id": item.id,
        "nombre": item.nombre,
        "tipo": item.tipo,
    }

    serialized_data = ItemSerializer(data=data)
    serialized_object = ItemSerializer(item)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el mismo orden"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"



@pytest.mark.django_db
def test_equipamiento_serializer():
    from maestro.serializers import EquipamientoSerializer
    from maestro.models import Equipamiento, Item
    equipamiento = Equipamiento.objects.create(
        item = Item.objects.create(
            nombre = "Test Item",
            tipo = Item.Tipo.APOYO_MONITORIZACION
        ),
        marca = "Test Marca",
        modelo = "Test Modelo",
    )

    data = {
        "id": equipamiento.id,
        "item": equipamiento.item.id,
        "marca": equipamiento.marca,
        "modelo": equipamiento.modelo,
    }


    serialized_data = EquipamientoSerializer(data=data)
    serialized_object = EquipamientoSerializer(equipamiento)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el mismo orden"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"



@pytest.mark.django_db
def test_quiebre_serializer():
    from maestro.serializers import QuiebreSerializer
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

    data = {
        "institucion": quiebre.institucion.id,
        "medicamento": quiebre.medicamento.id,
        "cantidad": quiebre.cantidad,
    }

    serialized_data = QuiebreSerializer(data=data)
    serialized_object = QuiebreSerializer(quiebre)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el mismo orden"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"



