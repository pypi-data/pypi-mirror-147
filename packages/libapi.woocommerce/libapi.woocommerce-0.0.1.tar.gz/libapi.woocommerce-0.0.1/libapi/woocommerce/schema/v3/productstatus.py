"""Declares :class:`ProductStatus`."""
import enum


class ProductStatus(str, enum.Enum):
    __module__: str = 'libapi.woocommerce.schema.v3'
    draft = "draft"
    pending = "pending"
    private = "private"
    publish = "publish"