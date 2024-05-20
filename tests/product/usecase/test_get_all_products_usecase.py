from unittest.mock import patch
from system.application.dto.responses.product_response import GetAllProductsResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.repository_exception import DataRepositoryExeption
from system.application.usecase.products_usecase import GetAllProductsUseCase


def test_get_all_products_usecase_success(
    mock_get_products_repository_response, mock_get_products_usecase_response
):
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_all_products"
    ) as mock_get_all_products:
        mock_get_all_products.return_value = mock_get_products_repository_response
        response = GetAllProductsUseCase.execute()
        assert isinstance(response, GetAllProductsResponse)
        assert response.response == mock_get_products_usecase_response


def test_get_all_products_usecase_failure():
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_all_products"
    ) as mock_get_all_products:
        mock_get_all_products.side_effect = DataRepositoryExeption(
            "Database connection error"
        )
        try:
            GetAllProductsUseCase.execute()
        except InfrastructureError:
            assert True
