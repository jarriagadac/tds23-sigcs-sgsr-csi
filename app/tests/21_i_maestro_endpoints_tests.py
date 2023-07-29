import pytest


@pytest.mark.django_db
def test_add_medicamentos(client):
    response = client.post(
        "/maestro/medicamentos",
        {
            "nombre_comercial": "nombre comercial prueba",
            "nombre_generico": "nombre generico prueba",
            "ingredientes": "ingredientes prueba",
            "concentracion": "concentracion prueba",
            "forma_presentacion": "frasco",
            "forma_farmaceutica": "tabletas",
            "via_administracion": "oral",
            "indicaciones_terapeuticas": "i.t. prueba",
            "contraindicaciones": "contraindicaciones prueba",
            "efectos_secundarios": "e.s. prueba",
            "instrucciones_dosificacion": "i.d. prueba",
            "fabricante": "fabricante prueba",
            "informacion_almacenamiento": "i.a. prueba",
            "interacciones_medicamentosas": "i.m. prueba",
        },
        content_type="application/json",
    )
    assert response.status_code == 201, "endpoint no encontrado"
    assert response.data["nombre_comercial"] == "nombre comercial prueba"
    assert response.data["nombre_generico"] == "nombre generico prueba"
    assert response.data["ingredientes"] == "ingredientes prueba"
    assert response.data["concentracion"] == "concentracion prueba"
    assert response.data["forma_presentacion"] == "frasco"
    assert response.data["forma_farmaceutica"] == "tabletas"
    assert response.data["via_administracion"] == "oral"
    assert response.data["indicaciones_terapeuticas"] == "i.t. prueba"
    assert response.data["contraindicaciones"] == "contraindicaciones prueba"
    assert response.data["efectos_secundarios"] == "e.s. prueba"
    assert response.data["instrucciones_dosificacion"] == "i.d. prueba"
    assert response.data["fabricante"] == "fabricante prueba"
    assert response.data["informacion_almacenamiento"] == "i.a. prueba"
    assert response.data["interacciones_medicamentosas"] == "i.m. prueba"


@pytest.mark.django_db
def test_list_medicamentos(client):
    client.post(
        "/maestro/medicamentos",
        {
            "nombre_comercial": "nombre comercial prueba",
            "nombre_generico": "nombre generico prueba",
            "ingredientes": "ingredientes prueba",
            "concentracion": "concentracion prueba",
            "forma_presentacion": "frasco",
            "forma_farmaceutica": "tabletas",
            "via_administracion": "oral",
            "indicaciones_terapeuticas": "i.t. prueba",
            "contraindicaciones": "contraindicaciones prueba",
            "efectos_secundarios": "e.s. prueba",
            "instrucciones_dosificacion": "i.d. prueba",
            "fabricante": "fabricante prueba",
            "informacion_almacenamiento": "i.a. prueba",
            "interacciones_medicamentosas": "i.m. prueba",
        },
        content_type="application/json",
    )
    response = client.get("/maestro/medicamentos", content_type="application/json")
    assert response.status_code == 200, "endpoint no encontrado"
    assert len(response.data) == 36, "se agregó más de un medicamento en la base de datos"


@pytest.mark.django_db
def test_get_medicamentos(client):
    client.post(
        "/maestro/medicamentos",
        {
            "nombre_comercial": "nombre comercial prueba",
            "nombre_generico": "nombre generico prueba",
            "ingredientes": "ingredientes prueba",
            "concentracion": "concentracion prueba",
            "forma_presentacion": "frasco",
            "forma_farmaceutica": "tabletas",
            "via_administracion": "oral",
            "indicaciones_terapeuticas": "i.t. prueba",
            "contraindicaciones": "contraindicaciones prueba",
            "efectos_secundarios": "e.s. prueba",
            "instrucciones_dosificacion": "i.d. prueba",
            "fabricante": "fabricante prueba",
            "informacion_almacenamiento": "i.a. prueba",
            "interacciones_medicamentosas": "i.m. prueba",
        },
        content_type="application/json",
    )
    response = client.get("/maestro/medicamentos/36", content_type="application/json")
    assert response.status_code == 200, "endpoint no encontrado"
    assert response.data["id"] == 36, "no se obtuvieron medicamentos"


@pytest.mark.django_db
def test_delete_medicamentos(client):
    client.post(
        "/maestro/medicamentos",
        {
            "nombre_comercial": "nombre comercial prueba",
            "nombre_generico": "nombre generico prueba",
            "ingredientes": "ingredientes prueba",
            "concentracion": "concentracion prueba",
            "forma_presentacion": "frasco",
            "forma_farmaceutica": "tabletas",
            "via_administracion": "oral",
            "indicaciones_terapeuticas": "i.t. prueba",
            "contraindicaciones": "contraindicaciones prueba",
            "efectos_secundarios": "e.s. prueba",
            "instrucciones_dosificacion": "i.d. prueba",
            "fabricante": "fabricante prueba",
            "informacion_almacenamiento": "i.a. prueba",
            "interacciones_medicamentosas": "i.m. prueba",
        },
        content_type="application/json",
    )
    response = client.delete("/maestro/medicamentos/36", content_type="application/json")
    assert response.status_code == 204, "endpoint no encontrado"

    response = client.get("/maestro/medicamentos/36", content_type="application/json")
    assert response.status_code == 404, "el medicamento no fue eliminado"


@pytest.mark.django_db
def test_add_medicamento_invalid_json(client):
    response = client.post(
        "/maestro/medicamentos",
        {
            "nombre_comercial": "nombre comercial prueba",
            "nombre_generico": "nombre generico prueba",
            "ingredientes": "ingredientes prueba",
            "concentracion": "concentracion prueba",
            "forma_presentacion": "prueba",
            "forma_farmaceutica": "prueba",
            "via_administracion": "prueba",
            "indicaciones_terapeuticas": "i.t. prueba",
            "contraindicaciones": "contraindicaciones prueba",
            "efectos_secundarios": "e.s. prueba",
            "instrucciones_dosificacion": "i.d. prueba",
            "fabricante": "fabricante prueba",
            "informacion_almacenamiento": "i.a. prueba",
            "interacciones_medicamentosas": "i.m. prueba",
        },
        content_type="application/json",
    )
    assert response.status_code == 400, "endpoint no encontrado / no se debe permitir data mal formada"


@pytest.mark.django_db
def test_add_quiebres(client):
    response = client.post(
        "/maestro/quiebres",
        {
            "institucion": 1,
            "medicamento": 1,
            "cantidad": 500,
        },
        content_type="application/json",
    )
    assert response.status_code == 201, "endpoint no encontrado"
    assert response.data["institucion"] == 1
    assert response.data["medicamento"] == 1
    assert response.data["cantidad"] == 500


@pytest.mark.django_db
def test_list_quiebres(client):
    client.post(
        "/maestro/quiebres",
        {
            "institucion": 1,
            "medicamento": 1,
            "cantidad": 500,
        },
        content_type="application/json",
    )
    response = client.get("/maestro/quiebres", content_type="application/json")
    assert response.status_code == 200, "endpoint no encontrado"
    assert len(response.data) == 47, "se agregó más de un quiebre en la base de datos"


@pytest.mark.django_db
def test_get_quiebre(client):
    client.post(
        "/maestro/quiebres",
        {
            "institucion": 1,
            "medicamento": 1,
            "cantidad": 500,
        },
        content_type="application/json",
    )
    response = client.get("/maestro/quiebres/47", content_type="application/json")
    assert response.status_code == 200, "endpoint no encontrado"
    assert response.data["id"] == 47, "no se obtuvieron quiebres"


@pytest.mark.django_db
def test_delete_quiebres(client):
    client.post(
        "/maestro/quiebres",
        {
            "institucion": 1,
            "medicamento": 1,
            "cantidad": 500,
        },
        content_type="application/json",
    )
    response = client.delete("/maestro/quiebres/47", content_type="application/json")
    assert response.status_code == 204, "endpoint no encontrado"

    response = client.get("/maestro/quiebres/47", content_type="application/json")
    assert response.status_code == 404, "el quiebre no fue eliminado"


@pytest.mark.django_db
def test_add_quiebre_invalid_json(client):
    response = client.post(
        "/maestro/medicamentos",
        {
            "id_institucion": 1,
            "id_medicamento": 1,
            "cantidad": 500,
        },
        content_type="application/json",
    )
    assert response.status_code == 400, "endpoint no encontrado / no se debe permitir data mal formada"
