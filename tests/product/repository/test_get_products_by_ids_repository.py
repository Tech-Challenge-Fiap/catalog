import pytest
from unittest.mock import patch
from system.infrastructure.adapters.database.models.product_model import ProductModel
from system.infrastructure.adapters.database.repositories.product_repository import (
    ProductRepository,
)
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
    NoObjectFoundError,
)
from system.domain.entities.product import ProductEntity
from tests.conftest import BaseRepositoryConfTest
from app import db


class TestGetProductsByIds(BaseRepositoryConfTest):
    def product_repository(self):
        return ProductRepository()

    def test_get_products_by_ids_success(self):
        product1 = ProductModel(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price=20.0,
            prep_time=6,
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
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
        result = product_repo.get_products_by_ids([1, 2])
        assert len(result) == 2
        assert all(isinstance(p, ProductEntity) for p in result)
        p1 = ProductEntity.from_orm(product1)
        p2 = ProductEntity.from_orm(product2)
        expected_result = [p1, p2]
        assert expected_result == result

    def test_get_products_by_ids_not_found(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=NoObjectFoundError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(NoObjectFoundError):
                product_repo.get_products_by_ids([99])

    def test_get_products_by_ids_error(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=PostgreSQLError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(PostgreSQLError):
                product_repo.get_products_by_ids([1, 2])
