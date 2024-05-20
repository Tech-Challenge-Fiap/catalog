import pytest
from unittest.mock import patch
from system.application.dto.responses.product_response import (
    UpdateProductResponse,
)
from system.application.exceptions.product_exceptions import ProductDoesNotExistError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


@pytest.fixture
def product_data():
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


product_id = 1


def test_enable_product_success(client, product_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.EnableProductUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = UpdateProductResponse(product_data)
        response = client.patch(f"/enable_product/{product_id}")
        assert response.status_code == 200
        assert response.json == product_data


def test_enable_product_not_found(client):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.EnableProductUseCase.execute",
        side_effect=ProductDoesNotExistError,
    ):
        response = client.patch(f"/enable_product/{product_id}")
        assert response.status_code == 404
        assert response.json == {"error": "This Product does not exist"}
