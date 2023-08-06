"""Declares :class:`ProductTagRef`."""
import pydantic


class ProductTagRef(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'

    id: int
    name: str = ""
    slug: str = ""