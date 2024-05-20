import pytest
from unittest.mock import patch
from system.infrastructure.adapters.database.models.product_model import ProductModel
from system.infrastructure.adapters.database.repositories.product_repository import (
    ProductRepository,
)
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
)
from system.domain.entities.product import ProductEntity
from tests.conftest import BaseRepositoryConfTest
from app import db


class TestGetDeletedProducts(BaseRepositoryConfTest):
    def product_repository(self):
        return ProductRepository()

    def test_get_deleted_products_success(self):
        product1 = ProductModel(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price=20.0,
            prep_time=6,
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=False,
        )
        product2 = ProductModel(
            product_id=2,
            type="SNACK",
            name="Cheeseburger",
            price=34.0,
            prep_time=10,
            description="pao, carne, queijo e salada",
            image="url_cheeseburger",
            is_active=True,
        )
        db.session.add(product1)
        db.session.add(product2)
        db.session.commit()

        product_repo = self.product_repository()
        deleted_products = product_repo.get_deleted_products()

        assert len(deleted_products) == 1
        for product in deleted_products:
            assert not product.is_active
            assert isinstance(product, ProductEntity)
        p1 = ProductEntity.from_orm(product1)
        expected_result = [p1]
        assert expected_result == deleted_products

    def test_get_deleted_products_error(self):
        # Setup - Mock a database error during query execution
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=PostgreSQLError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(PostgreSQLError):
                product_repo.get_deleted_products()
