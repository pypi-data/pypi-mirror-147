"""Declares :class:`ProductAttributeRef`."""
import pydantic


class ProductAttributeRef(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'
    id: int
    name: str = ""
    position: int = 0
    visible: bool = False
    variation: bool = False