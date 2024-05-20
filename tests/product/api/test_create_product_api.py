import pytest
from unittest.mock import patch
from system.application.dto.responses.product_response import CreateProductResponse
from system.application.exceptions.default_exceptions import InfrastructureError

from system.application.exceptions.product_exceptions import ProductAlreadyExistsError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


@pytest.fixture
def create_product_data():
    return {
        "product_id": 1,
        "type": "SIDE",
        "name": "Batata Frita Grande",
        "price": 20.0,
        "prep_time": 6,
        "description": "batatinha crocante tamanho grande",
        "image": "url_imagem2",
        "is_active": True,
    }


def test_create_product_success(client, create_product_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.CreateProductUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = CreateProductResponse(create_product_data)
        response = client.post(
            "/create_product",
            json=create_product_data,
            headers={"Authorization": "Bearer VALID_TOKEN"},
        )
        assert response.status_code == 200
        assert response.json == create_product_data


def test_create_product_already_exists(client, create_product_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.CreateProductUseCase.execute",
        side_effect=ProductAlreadyExistsError,
    ):
        response = client.post("/create_product", json=create_product_data)
        assert response.status_code == 400
        assert response.json == {"error": "This product already exists"}


def test_create_product_infrastructure_error(client, create_product_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.CreateProductUseCase.execute",
        side_effect=InfrastructureError,
    ):
        response = client.post("/create_product", json=create_product_data)
        assert response.status_code == 500
        assert response.json == {"error": "Internal Error"}
