import pytest
from unittest.mock import patch
from system.application.exceptions.repository_exception import NoObjectFoundError
from system.infrastructure.adapters.database.models.product_model import ProductModel
from system.infrastructure.adapters.database.repositories.product_repository import (
    ProductRepository,
)
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    InvalidInputError,
)
from system.domain.entities.product import ProductEntity
from tests.conftest import BaseRepositoryConfTest
from app import db


class TestGetProductsByType(BaseRepositoryConfTest):
    def product_repository(self):
        return ProductRepository()

    def test_get_products_by_type_success(self):
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
        result = product_repo.get_products_by_type("SIDE")
        assert len(result) == 1
        assert all(isinstance(p, ProductEntity) for p in result)
        p1 = ProductEntity.from_orm(product1)
        expected_result = [p1]
        assert expected_result == result

    def test_get_products_by_type_not_found(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=NoObjectFoundError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(NoObjectFoundError):
                product_repo.get_products_by_type("Nonexistent")

    def test_get_products_by_type_error(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=InvalidInputError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(InvalidInputError):
                product_repo.get_products_by_type("Invalid")
