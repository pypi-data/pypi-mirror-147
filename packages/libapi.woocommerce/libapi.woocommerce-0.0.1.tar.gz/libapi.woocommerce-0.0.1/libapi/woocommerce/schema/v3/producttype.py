"""Declares :class:`ProductType`."""
import enum


class ProductType(str, enum.Enum):
    __module__: str = 'libapi.woocommerce.schema.v3'
    simple = 'simple'
    grouped = 'grouped'
    external = 'external'
    variable = 'variable'