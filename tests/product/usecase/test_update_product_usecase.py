from unittest.mock import patch
from system.application.dto.responses.product_response import UpdateProductResponse
from system.application.exceptions.product_exceptions import ProductDoesNotExistError
from system.application.usecase.products_usecase import UpdateProductUseCase


def test_update_product_usecase_success(mock_update_product_request, mock_product):
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.update_product"
    ) as mock_update_product:
        mock_update_product.return_value = mock_product
        response = UpdateProductUseCase.execute(product_id, mock_update_product_request)
        assert isinstance(response, UpdateProductResponse)


def test_update_product_usecase_not_found(mock_update_product_request):
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.update_product"
    ) as mock_update_product:
        mock_update_product.side_effect = ProductDoesNotExistError
        try:
            UpdateProductUseCase.execute(product_id, mock_update_product_request)
        except ProductDoesNotExistError:
            assert True
