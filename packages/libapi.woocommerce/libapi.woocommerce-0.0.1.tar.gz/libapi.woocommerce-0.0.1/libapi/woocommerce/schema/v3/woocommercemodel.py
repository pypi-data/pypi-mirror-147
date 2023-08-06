"""Declares :class:`WooCommerceModel`."""
import datetime

import pydantic


class WooCommerceModel(pydantic.BaseModel):
    __module__: str = 'libapi.woocommerce.schema.v3'

    id: int | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    date_modified: datetime.datetime | None = None
    date_modified_gmt: datetime.datetime | None = None