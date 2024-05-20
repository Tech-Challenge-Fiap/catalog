import pytest
from unittest.mock import patch
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
)
from system.infrastructure.adapters.database.repositories.product_repository import (
    ProductRepository,
)
from system.domain.entities.product import ProductEntity
from tests.conftest import BaseRepositoryConfTest


class TestCreateProduct(BaseRepositoryConfTest):
    def product_repository(self):
        return ProductRepository()

    def mock_product_entity(self):
        return ProductEntity(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price=20.0,
            prep_time=6,
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
        )

    def test_create_product_success(self):
        product = self.mock_product_entity()
        product_repo = self.product_repository()
        created_product = product_repo.create_product(product)
        assert product == created_product

    def test_create_product_error(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.add"
        ), patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.commit",
            side_effect=PostgreSQLError(),
        ):
            with pytest.raises(PostgreSQLError):
                product = self.mock_product_entity()
                product_repo = self.product_repository()
                product_repo.create_product(product)
