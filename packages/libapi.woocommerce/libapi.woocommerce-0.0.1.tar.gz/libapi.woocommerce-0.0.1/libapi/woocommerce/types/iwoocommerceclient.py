"""Declares :class:`IWooCommerceClient`."""
import typing


class IWooCommerceClient:
    __module__: str = 'libapi.woocommerce.types'

    async def get_product_variations(
        self,
        product_id: int,
        variations: list[int]
    ) -> list[dict[str, typing.Any]]:
        """Returns the variations for the given product."""
        raise NotImplementedError