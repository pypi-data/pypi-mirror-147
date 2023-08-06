"""Declares :class:`ResourceLink`."""
import pydantic


class ResourceLink(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'

    href: str