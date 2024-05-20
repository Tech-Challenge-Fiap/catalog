import pytest
from unittest.mock import patch
from system.application.dto.responses.product_response import (
    GetProductsByTypeResponse,
)
from system.application.exceptions.product_exceptions import ProductTypeError


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


product_type = "SIDE"


def test_get_products_by_type_success(
    client, mock_get_products_by_type_usecase_response
):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.GetProductsByTypeUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = GetProductsByTypeResponse(
            mock_get_products_by_type_usecase_response
        )
        response = client.get(f"/get_products/{product_type}")
        assert response.status_code == 200
        assert response.json == mock_get_products_by_type_usecase_response


def test_get_products_by_type_not_found(client):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.GetProductsByTypeUseCase.execute",
        side_effect=ProductTypeError,
    ):
        response = client.get(f"/get_products/{product_type}")
        assert response.status_code == 400
        assert response.json == {"error": "This Product Type does not exist"}
