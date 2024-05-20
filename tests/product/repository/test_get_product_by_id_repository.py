import pytest
from unittest.mock import patch
from system.infrastructure.adapters.database.models.product_model import ProductModel
from system.infrastructure.adapters.database.repositories.product_repository import (
    ProductRepository,
)
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import (
    PostgreSQLError,
)
from tests.conftest import BaseRepositoryConfTest
from app import db


class TestGetProductByID(BaseRepositoryConfTest):
    def product_repository(self):
        return ProductRepository()

    def mock_product_model(self):
        return ProductModel(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price=20.0,
            prep_time=6,
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
        )

    def test_get_product_by_id_success(self):
        product = self.mock_product_model()
        db.session.add(product)
        db.session.commit()

        product_repo = self.product_repository()
        retrieved_product = product_repo.get_product_by_id(1)

        assert retrieved_product is not None
        assert retrieved_product.product_id == 1
        assert retrieved_product.name == "Batata Frita Grande"

    def test_get_product_by_id_error(self):
        with patch(
            "system.infrastructure.adapters.database.repositories.product_repository.db.session.query",
            side_effect=PostgreSQLError(),
        ):
            product_repo = self.product_repository()
            with pytest.raises(PostgreSQLError):
                product_repo.get_product_by_id(1)
