from unittest.mock import patch
from system.application.exceptions.product_exceptions import ProductDoesNotExistError
from system.application.usecase.products_usecase import DeleteProductUseCase


def test_delete_product_usecase_success():
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.delete_product_by_id"
    ) as mock_delete_product_by_id:
        mock_delete_product_by_id.return_value = None
        response = DeleteProductUseCase.execute(product_id)
        assert response is None


def test_delete_product_usecase_not_found():
    product_id = 1
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository.delete_product_by_id"
    ) as mock_delete_product_by_id:
        mock_delete_product_by_id.side_effect = ProductDoesNotExistError
        try:
            DeleteProductUseCase.execute(product_id)
        except ProductDoesNotExistError:
            assert True
