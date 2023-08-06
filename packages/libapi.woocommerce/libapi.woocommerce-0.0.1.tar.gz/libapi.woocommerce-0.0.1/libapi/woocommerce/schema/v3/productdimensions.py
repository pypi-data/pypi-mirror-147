"""Declares :class:`ProductDimensions`."""
import pydantic


class ProductDimensions(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'
    length: str = ""
    width: str = ""
    height: str = ""