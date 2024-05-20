from typing import List
from unittest.mock import patch

import pytest

from system.application.dto.requests.product_request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from system.application.dto.responses.product_response import (
    ProductResponse,
    GetAllProductsResponse,
)
from system.domain.entities.product import ProductEntity


def create_product():
    return ProductEntity(
        product_id=1,
        type="SIDE",
        name="Batata Frita Grande",
        price="20",
        prep_time="6",
        description="batatinha crocante tamanho grande",
        image="url_imagem2",
        is_active=True,
    )


@pytest.fixture
def mock_product_repository():
    with patch(
        "system.infrastructure.adapters.database.repositories.product_repository.ProductRepository",
        autospec=True,
    ) as product_repository:
        yield product_repository


@pytest.fixture
def mock_product() -> ProductEntity:
    """
    Mock that creates a Product
    """
    return create_product()


@pytest.fixture
def mock_create_product_request() -> CreateProductRequest:
    """
    Mock that creates a CreateProductRequest
    """
    return CreateProductRequest(
        type="SIDE",
        name="Batata Frita Grande",
        price="20",
        prep_time="6",
        description="batatinha crocante tamanho grande",
        image="url_imagem2",
    )


@pytest.fixture
def mock_get_products_response() -> GetAllProductsResponse:
    """
    Mock that creates a GetAllProductsResponse
    """
    product_list: List[ProductResponse] = []
    product_list.append(
        ProductResponse(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price="20",
            prep_time="6",
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
        )
    )
    product_list.append(
        ProductResponse(
            product_id=2,
            type="SNACK",
            name="Cheeseburger com bacon",
            price="34",
            prep_time="10",
            description="pao, carne, queijo, bacon, picles e molho da casa",
            image="url_imagem_cheeseburger",
            is_active=True,
        )
    )
    return GetAllProductsResponse(products=product_list)


@pytest.fixture
def mock_get_products_usecase_response() -> List[ProductEntity]:
    """
    Mock that creates a List[ProductEntity]
    """
    product_list: List[ProductEntity] = []
    product_list.append(
        ProductEntity(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price="20",
            prep_time="6",
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
        )
    )
    product_list.append(
        ProductEntity(
            product_id=2,
            type="SNACK",
            name="Cheeseburger com bacon",
            price="34",
            prep_time="10",
            description="pao, carne, queijo, bacon, picles e molho da casa",
            image="url_imagem_cheeseburger",
            is_active=True,
        )
    )
    return GetAllProductsResponse(product_list)


@pytest.fixture
def mock_get_products_by_type_repository_response() -> List[ProductEntity]:
    """
    Mock that creates a List[ProductEntity]
    """
    product_list: List = []
    product_list.append(
        ProductEntity(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price="20",
            prep_time="6",
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
        )
    )
    return product_list


@pytest.fixture
def mock_get_products_by_ids_repository_response() -> List[ProductEntity]:
    """
    Mock that creates a List[ProductEntity]
    """
    product_list: List = []
    product_list.append(
        ProductEntity(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price="20",
            prep_time="6",
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
        )
    )
    return product_list


@pytest.fixture
def product_repository_response() -> ProductEntity:
    """
    Mock that creates a ProductEntity
    """
    return ProductEntity(
        product_id=1,
        type="SIDE",
        name="Batata Frita Grande",
        price="20",
        prep_time="6",
        description="batatinha crocante tamanho grande",
        image="url_imagem2",
        is_active=True,
    )


@pytest.fixture
def mock_get_products_repository_response() -> List[ProductEntity]:
    """
    Mock that creates a List[ProductEntity]
    """
    product_list: List = []
    product_list.append(
        ProductEntity(
            product_id=1,
            type="SIDE",
            name="Batata Frita Grande",
            price="20",
            prep_time="6",
            description="batatinha crocante tamanho grande",
            image="url_imagem2",
            is_active=True,
        )
    )
    product_list.append(
        ProductEntity(
            product_id=1,
            type="SNACK",
            name="Cheeseburger com bacon",
            price="34",
            prep_time="10",
            description="pao, carne, queijo, bacon, picles e molho da casa",
            image="url_imagem_cheeseburger",
            is_active=True,
        )
    )
    return product_list


@pytest.fixture
def mock_get_products_usecase_response(
    mock_get_products_repository_response: List[ProductEntity],
) -> List[dict]:
    """
    Mock that creates a list ProductEntity for use case responses
    """
    return [product.model_dump() for product in mock_get_products_repository_response]


@pytest.fixture
def mock_get_products_by_type_usecase_response(
    mock_get_products_by_type_repository_response: List[ProductEntity],
) -> List[dict]:
    """
    Mock that creates a list of dictionaries representing ProductEntity for use case responses
    """
    return [
        product.model_dump()
        for product in mock_get_products_by_type_repository_response
    ]


@pytest.fixture
def mock_update_product_request() -> UpdateProductRequest:
    """
    Mock that creates a UpdateProductRequest
    """
    return UpdateProductRequest(
        name="Batata Frita Grande",
        price="20",
        prep_time="6",
        description="batatinha crocante tamanho grande",
        image="url_imagem2",
    )
