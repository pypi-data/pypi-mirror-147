"""Declares :class:`ProductDownload`."""
import pydantic


class ProductDownload(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'
    id: str
    name: str
    file: str