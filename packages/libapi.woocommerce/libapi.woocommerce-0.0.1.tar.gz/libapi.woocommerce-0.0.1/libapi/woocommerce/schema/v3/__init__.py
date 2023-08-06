# pylint: skip-file
from .product import Product
from .productcatalogvisibility import ProductCatalogVisibility
from .productstatus import ProductStatus
from .producttype import ProductType
from .productvariation import ProductVariation


__all__ = [
    'Client',
    'Product',
    'ProductCatalogVisibility',
    'ProductStatus',
    'ProductType',
    'ProductVariation',
]


class Client:

    async def get_product(self, product_id: int) -> Product:
        raise NotImplementedError

    async def get_product_variations(
        self,
        product_id: int,
        variants: list[int]
    ) -> list[ProductVariation]:
        raise NotImplementedError