from unittest.mock import patch
from system.application.dto.responses.product_response import GetProductsByTypeResponse
from system.application.exceptions.product_exceptions import ProductTypeError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.repository_exception import (
    InvalidInputError,
    DataRepositoryExeption,
)
from system.application.usecase.products_usecase import GetProductsByTypeUseCase

product_type = "SIDE"


def test_get_products_by_type_usecase_success(
    mock_get_products_by_type_usecase_response,
    mock_get_products_by_type_repository_response,
):
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_products_by_type"
    ) as mock_get_products_by_type:
        mock_get_products_by_type.return_value = (
            mock_get_products_by_type_repository_response
        )
        response = GetProductsByTypeUseCase.execute(product_type)
        assert isinstance(response, GetProductsByTypeResponse)
        assert response.response == mock_get_products_by_type_usecase_response


def test_get_products_by_type_usecase_invalid_input():
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_products_by_type"
    ) as mock_get_products_by_type:
        mock_get_products_by_type.side_effect = InvalidInputError("Invalid type")
        try:
            GetProductsByTypeUseCase.execute(product_type)
        except ProductTypeError:
            assert True


def test_get_products_by_type_usecase_failure():
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_products_by_type"
    ) as mock_get_products_by_type:
        mock_get_products_by_type.side_effect = DataRepositoryExeption(
            "Database connection error"
        )
        try:
            GetProductsByTypeUseCase.execute(product_type)
        except InfrastructureError:
            assert True
