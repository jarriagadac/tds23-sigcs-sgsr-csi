import pytest
import json
from maestro.models import Institucion, Medicamento, Quiebre, Item, Equipamiento


@pytest.mark.django_db
def test_institucion_serializer():
    from maestro.serializers import InstitucionSerializer

    institucion = Institucion.objects.create(
        nombre="Clínica RedSalud Elqui", tipo="clinica", titularidad="privado", num_camas_uti=12, num_camas_uci=6, factor=1.0
    )

    data = {
        "id": institucion.id,
        "nombre": institucion.nombre,
        "tipo": institucion.tipo,
        "titularidad": institucion.titularidad,
        "num_camas_uti": institucion.num_camas_uti,
        "num_camas_uci": institucion.num_camas_uci,
        "factor": institucion.factor,
    }

    serialized_data = InstitucionSerializer(data=data)
    serialized_object = InstitucionSerializer(institucion)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el orden correcto"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"


@pytest.mark.django_db
def test_medicamento_serializer():
    from maestro.serializers import MedicamentoSerializer

    medicamento = Medicamento.objects.create(
        nombre_comercial="Naproxeno",
        nombre_generico="Naproxeno",
        ingredientes="Naproxeno",
        concentracion="250mg",
        forma_presentacion="blister",
        forma_farmaceutica="tabletas",
        via_administracion="oral",
        indicaciones_terapeuticas="Alivio temporal del dolor y la inflamación.",
        contraindicaciones="No utilizar en caso de alergia al naproxeno, úlcera péptica activa o enfermedad renal grave.",
        efectos_secundarios="Puede causar molestias estomacales, úlceras, sangrado gastrointestinal y daño renal si se excede la dosis recomendada.",
        instrucciones_dosificacion="Tomar 1 tableta cada 8-12 horas según sea necesario. No exceder 1,250mg en 24 horas.",
        fabricante="Bayer AG",
        informacion_almacenamiento="Almacenar a temperatura ambiente, protegido de la luz y la humedad.",
        interacciones_medicamentosas="El naproxeno puede interactuar con medicamentos antiinflamatorios y anticoagulantes. Consulte a su médico o farmacéutico para obtener información sobre posibles interacciones.",
    )

    data = {
        "id": medicamento.id,
        "nombre_comercial": medicamento.nombre_comercial,
        "nombre_generico": medicamento.nombre_generico,
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

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el orden correcto"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"


@pytest.mark.django_db
def test_item_serializer():
    from maestro.serializers import ItemSerializer

    item = Item.objects.create(nombre="Respirador Mecánico", tipo="soporte_vital")

    data = {"id": item.id, "nombre": item.nombre, "tipo": item.tipo}

    serialized_data = ItemSerializer(data=data)
    serialized_object = ItemSerializer(item)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el orden correcto"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"


@pytest.mark.django_db
def test_equipamiento_serializer():
    from maestro.serializers import EquipamientoSerializer

    item = Item.objects.all().first()

    equipamiento = Equipamiento.objects.create(item=item, marca="Philips", modelo="Respironics V60")

    data = {"id": equipamiento.id, "item": equipamiento.item.id, "marca": equipamiento.marca, "modelo": equipamiento.modelo}

    serialized_data = EquipamientoSerializer(data=data)
    serialized_object = EquipamientoSerializer(equipamiento)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el orden correcto"
    assert serialized_data.errors == {}, f"Errores: {serialized_data.errors}"


@pytest.mark.django_db
def test_quiebre_serializer():
    from maestro.serializers import QuiebreSerializer

    institucion = Institucion.objects.all().first()
    medicamento = Medicamento.objects.all().first()

    quiebre = Quiebre.objects.create(institucion=institucion, medicamento=medicamento, cantidad=500)

    data = {"id": quiebre.id, "institucion": quiebre.institucion.id, "medicamento": quiebre.medicamento.id, "cantidad": quiebre.cantidad}

    serialized_data = QuiebreSerializer(data=data)
    serialized_object = QuiebreSerializer(quiebre)
    serialized_data.is_valid()

    assert json.dumps(serialized_object.data) == json.dumps(data), "data serializada no tiene el orden correcto"
