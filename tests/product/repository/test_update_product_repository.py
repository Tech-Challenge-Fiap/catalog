import pytest
from unittest.mock import patch
from system.application.dto.requests.product_request import UpdateProductRequest
from system.infrastructure.adapters.database.models.product_model import ProductModel
from system.infrastructure.adapters.database.repositories.product_repository import (
    ProductRepository,
)
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
    NoObjectFoundError,
)
from tests.conftest import BaseRepositoryConfTest
from app import db


class TestUpdateProduct(BaseRepositoryConfTest):
    def product_repository(self):
        return ProductRepository()

    def test_update_product_success(self):
        product = ProductModel(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price=20.0,
            prep_time=6,
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
        )
        db.session.add(product)
        db.session.commit()

        update_data = UpdateProductRequest(
            type="SIDE",
            name="Batata Frita Grande",
            price=15.0,
            prep_time=6,
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
        )

        product_repo = self.product_repository()
        updated_product = product_repo.update_product(product_id=1, request=update_data)

        assert updated_product.price == 15.0

    def test_update_product_not_found(self):
        # No product setup, expecting to handle not found
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=NoObjectFoundError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(NoObjectFoundError):
                product_repo.update_product(999, {"name": "Nonexistent"})

    def test_update_product_error(self):
        # Simulate a database error on update
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=PostgreSQLError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(PostgreSQLError):
                product_repo.update_product(1, {"name": "Error Case"})
