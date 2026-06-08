from types import SimpleNamespace
from unittest.mock import patch


def test_get_products(client, admin_headers):
    fake_products = [
        SimpleNamespace(
            product_id=1,
            product_name="Producto A",
            brand_id=1,
            category_id=1,
            model_year=2026,
            list_price=19.99,
        )
    ]

    with patch("blueprints.products.routes.get_all_products", return_value=fake_products):
        response = client.get("/api/products/", headers=admin_headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["product_name"] == "Producto A"
    assert float(data[0]["list_price"]) == 19.99


def test_get_brands(client, admin_headers):
    fake_brands = [SimpleNamespace(brand_id=1, brand_name="Marca A")]

    with patch("blueprints.products.routes.get_all_brands", return_value=fake_brands):
        response = client.get("/api/products/brands", headers=admin_headers)

    assert response.status_code == 200
    assert response.get_json()[0]["brand_name"] == "Marca A"
