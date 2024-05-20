from unittest.mock import patch
from system.application.dto.responses.product_response import GetAllProductsResponse
from system.application.exceptions.default_exceptions import InfrastructureError


def mock_require_auth(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def mock_verify_token(token):
    return {"user_id": "12345"}


def test_get_all_products_success(client, mock_get_products_usecase_response):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.GetAllProductsUseCase.execute"
    ) as mock_use_case:
        mock_use_case.return_value = GetAllProductsResponse(
            mock_get_products_usecase_response
        )
        response = client.get("/get_products/")
        assert response.status_code == 200
        assert response.json == mock_get_products_usecase_response


def test_get_all_products_infrastructure_error(client):
    with patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.verify_token",
        new=mock_verify_token,
    ), patch(
        "system.infrastructure.adapters.decorators.jwt_decorator.require_auth",
        new=mock_require_auth,
    ), patch(
        "system.application.usecase.products_usecase.GetAllProductsUseCase.execute",
        side_effect=InfrastructureError,
    ):
        response = client.get("/get_products/")
        assert response.status_code == 500
        assert response.json == {"error": "Internal Error"}
