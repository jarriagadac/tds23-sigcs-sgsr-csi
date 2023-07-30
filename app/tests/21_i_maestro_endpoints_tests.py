import pytest

@pytest.mark.django_db
def test_add_institucion(client):
    from maestro.models import Institucion
    
    institucion = Institucion(
        nombre="BLA BLA 1",
        tipo = Institucion.Tipo.CENTRO_MEDICO,
        titularidad = Institucion.Titularidad.PUBLICO,
        num_camas_uti = 10,
        num_camas_uci = 10,
        factor = 1.3,
    )

    response = client.post(
        "/maestro/institucion",
        {
            "nombre" : institucion.nombre,
            "tipo": institucion.tipo,
            "titularidad": institucion.titularidad,
            "num_camas_uti": institucion.num_camas_uti,
            "num_camas_uci": institucion.num_camas_uci,
            "factor": institucion.factor,
        },
        content_type="application/json",
    )

    assert response.status_code == 201, "endpoint no encontrado"
    assert response.data["nombre"] == institucion.nombre
    assert response.data["tipo"] == institucion.tipo

    
@pytest.mark.django_db
def test_add_medicamento(client):
    from maestro.models import Medicamento
    medicamento = Medicamento(
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

    response = client.post(
        "/maestro/medicamento",
        {
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
        },
        content_type="application/json",
    )

    assert response.status_code == 201, "endpoint no encontrado"
    assert response.data["nombre_comercial"] == medicamento.nombre_comercial
    assert response.data["ingredientes"] == medicamento.ingredientes

@pytest.mark.django_db
def test_add_item(client):
    from maestro.serializers import ItemSerializer
    from maestro.models import Item

    item = Item(
        nombre = "Test Item",
        tipo = Item.Tipo.APOYO_MONITORIZACION,
    )

    response = client.post(
        "/maestro/item",
        {
            "nombre": item.nombre,
            "tipo": item.tipo,
        },
        content_type="application/json",
    )

    assert response.status_code == 201, "endpoint no encontrado"
    assert response.data["nombre"] == item.nombre


@pytest.mark.django_db
def test_add_quiebre(client):
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


    quiebre = Quiebre(
        institucion = institucion,
        medicamento = medicamento,
        cantidad = 10,
    )

    response = client.post(
        "/maestro/quiebre",
        {
            "institucion": quiebre.institucion.id,
            "medicamento": quiebre.medicamento.id,
            "cantidad": quiebre.cantidad,
        },
        content_type="application/json",
    )

    assert response.status_code == 201, "endpoint no encontrado"
