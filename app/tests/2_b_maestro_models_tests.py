import pytest


@pytest.mark.django_db
def test_institucion_model():
    from maestro.models import Institucion

    institucion = Institucion.objects.create(
        nombre="Clínica RedSalud Elqui",
        tipo="clinica",
        titularidad="privado",
        num_camas_uti=12,
        num_camas_uci=6,
        factor=1.0,
    )

    assert institucion.nombre == "Clínica RedSalud Elqui"
    assert institucion.tipo == "clinica"
    assert institucion.titularidad == "privado"
    assert institucion.num_camas_uti == 12
    assert institucion.num_camas_uci == 6
    assert institucion.factor == 1.0

    assert str(institucion) == institucion.nombre, "Se debe usar el nombre como representacion str del objeto"


@pytest.mark.django_db
def test_medicamento_model():
    from maestro.models import Medicamento

    medicamento = Medicamento.objects.create(
        nombre_comercial="Ibupirac",
        nombre_generico="Ibuprofeno",
        ingredientes="Ibuprofeno",
        concentracion="400mg",
        forma_presentacion="blister",
        forma_farmaceutica="tabletas",
        via_administracion="oral",
        indicaciones_terapeuticas="Alivio temporal de dolores leves a moderados, como dolores de cabeza, dolores musculares, dolor de espalda, dolor de muelas, dolor menstrual y dolor de artritis.",
        contraindicaciones="No utilizar en caso de alergia al ibuprofeno, úlcera péptica activa o hemorragia gastrointestinal, insuficiencia cardíaca grave o enfermedad hepática grave.",
        efectos_secundarios="Algunos efectos secundarios pueden incluir malestar estomacal, náuseas, vómitos, diarrea, mareos, dolor de cabeza y erupciones en la piel. En casos raros, puede causar reacciones alérgicas graves.",
        instrucciones_dosificacion="La dosis recomendada para adultos es de 400mg cada 4 a 6 horas, no excediendo los 1,200mg en 24 horas. Consulte a su médico para obtener instrucciones específicas.",
        fabricante="Laboratorios Chile S.A.",
        informacion_almacenamiento="Almacenar en un lugar fresco y seco, protegido de la luz y fuera del alcance de los niños.",
        interacciones_medicamentosas="El ibuprofeno puede interactuar con otros medicamentos, como anticoagulantes, antihipertensivos, aspirina, corticosteroides y diuréticos. Consulte a su médico o farmacéutico para obtener información sobre posibles interacciones.",
    )

    assert medicamento.nombre_comercial == "Ibupirac"
    assert medicamento.nombre_generico == "Ibuprofeno"
    assert medicamento.ingredientes == "Ibuprofeno"
    assert medicamento.concentracion == "400mg"
    assert medicamento.forma_presentacion == "blister"
    assert medicamento.forma_farmaceutica == "tabletas"
    assert medicamento.via_administracion == "oral"
    assert medicamento.indicaciones_terapeuticas == (
        "Alivio temporal de dolores leves a moderados, como dolores de cabeza, "
        "dolores musculares, dolor de espalda, dolor de muelas, dolor menstrual y "
        "dolor de artritis."
    )
    assert medicamento.contraindicaciones == (
        "No utilizar en caso de alergia al ibuprofeno, úlcera péptica activa o "
        "hemorragia gastrointestinal, insuficiencia cardíaca grave o enfermedad "
        "hepática grave."
    )
    assert medicamento.efectos_secundarios == (
        "Algunos efectos secundarios pueden incluir malestar estomacal, náuseas, "
        "vómitos, diarrea, mareos, dolor de cabeza y erupciones en la piel. En "
        "casos raros, puede causar reacciones alérgicas graves."
    )
    assert medicamento.instrucciones_dosificacion == (
        "La dosis recomendada para adultos es de 400mg cada 4 a 6 horas, no "
        "excediendo los 1,200mg en 24 horas. Consulte a su médico para obtener "
        "instrucciones específicas."
    )
    assert medicamento.fabricante == "Laboratorios Chile S.A."
    assert medicamento.informacion_almacenamiento == (
        "Almacenar en un lugar fresco y seco, protegido de la luz y fuera del " "alcance de los niños."
    )
    assert medicamento.interacciones_medicamentosas == (
        "El ibuprofeno puede interactuar con otros medicamentos, como "
        "anticoagulantes, antihipertensivos, aspirina, corticosteroides y "
        "diuréticos. Consulte a su médico o farmacéutico para obtener información "
        "sobre posibles interacciones."
    )

    assert str(medicamento) == f"{medicamento.nombre_comercial} ({medicamento.nombre_generico}) | {medicamento.fabricante}"


@pytest.mark.django_db
def test_item_model():
    from maestro.models import Item

    item = Item.objects.create(nombre="Respirador Mecánico", tipo="soporte_vital")

    assert item.nombre == "Respirador Mecánico"
    assert item.tipo == "soporte_vital"

    assert str(item) == f"{item.nombre} ({item.tipo})"


@pytest.mark.django_db
def test_equipamiento_model():
    from maestro.models import Equipamiento
    from maestro.models import Item

    item = Item.objects.all().first()
    equipamiento = Equipamiento.objects.create(item=item, marca="Philips", modelo="Respironics V60")

    assert equipamiento.item == item
    assert equipamiento.marca == "Philips"
    assert equipamiento.modelo == "Respironics V60"

    assert str(equipamiento) == f"{equipamiento.marca} ({equipamiento.modelo}) | {equipamiento.item}"

    equipamiento.item.delete()
    assert Equipamiento.objects.filter(id=equipamiento.id).first() is None, "eliminar item debe eliminar equipamiento en cascada"


@pytest.mark.django_db
def test_quiebre_model():
    from maestro.models import Quiebre
    from maestro.models import Institucion
    from maestro.models import Medicamento

    medicamento = Medicamento.objects.all().first()
    institucion = Institucion.objects.all().first()

    quiebre = Quiebre.objects.create(institucion=institucion, medicamento=medicamento, cantidad=200)

    assert quiebre.institucion == institucion
    assert quiebre.medicamento == medicamento
    assert quiebre.cantidad == 200

    _, created = Quiebre.objects.get_or_create(
        institucion=quiebre.institucion,
        medicamento=quiebre.medicamento,
    )

    assert not created, "institucion y medicamento deben ser unique together"
