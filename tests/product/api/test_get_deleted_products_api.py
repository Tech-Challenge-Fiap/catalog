import pytest
from unittest.mock import patch
from system.application.dto.responses.product_response import (
    GetAllProductsResponse,
)
from system.application.exceptions.default_exceptions import InfrastructureError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


@pytest.fixture
def deleted_products_data():
    return {
        "product_id": 1,
        "type": "SIDE",
        "name": "Batata Frita Grande",
        "price": 20.0,
        "prep_time": 6,
        "description": "batatinha crocante tamanho grande",
        "image": "url_imagem2",
        "is_active": False,
    }


product_id = 1


def test_get_deleted_products_success(client, deleted_products_data):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.GetDeletedProductsUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = GetAllProductsResponse(deleted_products_data)
        response = client.get("/get_deleted_products/")
        assert response.status_code == 200
        assert response.json == deleted_products_data


def test_get_deleted_products_infrastructure_error(client):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.GetDeletedProductsUseCase.execute",
        side_effect=InfrastructureError,
    ):
        response = client.get("/get_deleted_products/")
        assert response.status_code == 500
        assert response.json == {"error": "Internal Error"}
