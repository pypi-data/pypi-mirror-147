"""Declares :class:`ProductCategoryRef`."""
import pydantic


class ProductCategoryRef(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'

    id: int
    name: str = ""
    slug: str = ""