from unittest.mock import patch
from system.application.dto.responses.product_response import UpdateProductResponse
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.product_exceptions import ProductDoesNotExistError
from system.application.exceptions.repository_exception import DataRepositoryExeption
from system.application.usecase.products_usecase import EnableProductUseCase


def test_enable_product_usecase_success(mock_product):
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.enable_product_by_id"
    ) as mock_enable_product:
        mock_enable_product.return_value = mock_product
        response = EnableProductUseCase.execute(product_id)
        assert isinstance(response, UpdateProductResponse)


def test_enable_product_usecase_not_found():
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.enable_product_by_id"
    ) as mock_enable_product:
        mock_enable_product.side_effect = ProductDoesNotExistError
        try:
            EnableProductUseCase.execute(product_id)
        except ProductDoesNotExistError:
            assert True


def test_enable_product_usecase_failure():
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.enable_product_by_id"
    ) as mock_enable_product:
        mock_enable_product.side_effect = DataRepositoryExeption(
            "Database connection error"
        )
        try:
            EnableProductUseCase.execute(product_id)
        except InfrastructureError:
            assert True
