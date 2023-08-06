"""Declares :class:`ProductDefaultAttribute."""
import pydantic


class ProductDefaultAttribute(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'

    id: int
    name: str = ""
    option: str = ""