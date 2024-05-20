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
from tests.conftest import BaseRepositoryConfTest
from app import db


class TestEnableProductById(BaseRepositoryConfTest):
    def product_repository(self):
        return ProductRepository()

    def test_enable_product_by_id_success(self):
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

        product_repo = self.product_repository()
        enabled_product = product_repo.enable_product_by_id(1)

        assert enabled_product.is_active == True

    def test_enable_product_by_id_not_found(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=NoObjectFoundError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(NoObjectFoundError):
                product_repo.enable_product_by_id(999)

    def test_enable_product_by_id_error(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=PostgreSQLError,
        ):
            product_repo = self.product_repository()
            with pytest.raises(PostgreSQLError):
                product_repo.enable_product_by_id(1)
