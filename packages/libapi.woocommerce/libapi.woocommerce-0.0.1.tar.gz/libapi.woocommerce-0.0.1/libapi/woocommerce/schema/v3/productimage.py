"""Declares :class:`ProductImage`."""
from .woocommercemodel import WooCommerceModel


class ProductImage(WooCommerceModel):
    src: str = ""
    name: str = ""
    alt: str = ""