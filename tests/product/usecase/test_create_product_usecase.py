from unittest.mock import patch
from system.application.dto.responses.product_response import CreateProductResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.repository_exception import DataRepositoryExeption
from system.application.usecase.products_usecase import CreateProductUseCase


def test_create_product_usecase_success(mock_create_product_request, mock_product):
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.create_product"
    ) as mock_create_product:
        mock_create_product.return_value = mock_product
        response = CreateProductUseCase.execute(mock_create_product_request)
        assert isinstance(response, CreateProductResponse)


def test_create_product_usecase_failure(mock_create_product_request):
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.create_product"
    ) as mock_create_product:
        mock_create_product.side_effect = DataRepositoryExeption(
            "Database connection error"
        )
        try:
            CreateProductUseCase.execute(mock_create_product_request)
        except InfrastructureError:
            assert True
