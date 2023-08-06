"""Declares :class:`ProductCatalogVisibility`."""
import enum


class ProductCatalogVisibility(str, enum.Enum):
    __module__: str = 'libapi.woocommerce.schema.v3'
    visible = "visible"
    catalog = "catalog"
    search = "search"
    hidden = "hidden"