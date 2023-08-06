"""Declares :class:`ProductMetadataProperty`."""
import pydantic


class ProductMetadataProperty(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'

    id: int
    key: str = ""
    value: str = "" 