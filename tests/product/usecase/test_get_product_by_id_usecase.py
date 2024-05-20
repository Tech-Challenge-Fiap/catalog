from unittest.mock import patch
from system.application.dto.responses.product_response import GetProductByIDResponse
from system.application.exceptions.product_exceptions import ProductDoesNotExistError
from system.application.usecase.products_usecase import GetProductByIDUseCase


def test_get_product_by_id_usecase_success(mock_product):
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_product_by_id"
    ) as mock_get_product_by_id:
        mock_get_product_by_id.return_value = mock_product
        response = GetProductByIDUseCase.execute(product_id)
        assert isinstance(response, GetProductByIDResponse)


def test_get_product_by_id_usecase_not_found():
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.get_product_by_id"
    ) as mock_get_product_by_id:
        mock_get_product_by_id.side_effect = ProductDoesNotExistError
        try:
            GetProductByIDUseCase.execute(product_id)
        except ProductDoesNotExistError:
            assert True
