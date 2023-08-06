"""Declares :class:`ProductVariation`."""
import datetime
import typing

import pydantic

from .productattributeref import ProductAttributeRef
from .productdimensions import ProductDimensions
from .productdownload import ProductDownload
from .productimage import ProductImage
from .productmetadataproperty import ProductMetadataProperty
from .productstatus import ProductStatus
from .woocommercemodel import WooCommerceModel


class ProductVariation(WooCommerceModel):
    __module__: str = 'libapi.woocommerce.schema.v3'
    description: str = ""
    permalink: str | None = None
    sku: str = ""
    price: str = ""
    regular_price: str = ""
    sale_price: str = ""
    date_on_sale_from: datetime.datetime | None = None
    date_on_sale_from_gmt: datetime.datetime | None = None
    date_on_sale_to: datetime.datetime | None = None
    date_on_sale_to_gmt: datetime.datetime | None = None
    on_sale: bool = False
    status: ProductStatus = ProductStatus.publish
    purchasable: bool = False
    virtual: bool = False
    downloadable: bool = False
    downloads: list[ProductDownload] = []
    download_limit: int = -1
    download_expiry: int = -1
    tax_status: str = "taxable"
    tax_class: str = ""
    manage_stock: bool = False
    stock_quantity: int | None = None
    stock_status: str = "instock"
    backorders: str = "no"
    backorders_allowed: bool = False
    backordered: bool = False
    weight: str = ""
    dimensions: ProductDimensions = pydantic.Field(
        default={
            "width": "",
            "height": "",
            "length": ""
        }
    )
    shipping_class: str = ""
    shipping_class_id: int = 0
    image: ProductImage | None = None
    attributes: list[ProductAttributeRef] = []
    menu_order: int = 0
    meta_data: list[ProductMetadataProperty] = []

    class Config:
        title: str = "WooCommerceProductVariation"
        example: dict[str, typing.Any] = {
            "id": 732,
            "date_created": "2017-03-23T00:36:38",
            "date_created_gmt": "2017-03-23T03:36:38",
            "date_modified": "2017-03-23T00:36:38",
            "date_modified_gmt": "2017-03-23T03:36:38",
            "description": "",
            "permalink": "https://example.com/product/ship-your-idea/?attribute_pa_color=black",
            "sku": "",
            "price": "9.00",
            "regular_price": "9.00",
            "sale_price": "",
            "date_on_sale_from": None,
            "date_on_sale_from_gmt": None,
            "date_on_sale_to": None,
            "date_on_sale_to_gmt": None,
            "on_sale": False,
            "status": "publish",
            "purchasable": True,
            "virtual": False,
            "downloadable": False,
            "downloads": [],
            "download_limit": -1,
            "download_expiry": -1,
            "tax_status": "taxable",
            "tax_class": "",
            "manage_stock": False,
            "stock_quantity": None,
            "stock_status": "instock",
            "backorders": "no",
            "backorders_allowed": False,
            "backordered": False,
            "weight": "",
            "dimensions": {
                "length": "",
                "width": "",
                "height": ""
            },
            "shipping_class": "",
            "shipping_class_id": 0,
            "image": {
                "id": 423,
                "date_created": "2016-10-19T12:21:14",
                "date_created_gmt": "2016-10-19T16:21:14",
                "date_modified": "2016-10-19T12:21:14",
                "date_modified_gmt": "2016-10-19T16:21:14",
                "src": "https://example.com/wp-content/uploads/2016/10/T_4_front-12.jpg",
                "name": "",
                "alt": ""
            },
            "attributes": [
                {
                "id": 6,
                "name": "Color",
                "option": "Black"
                }
            ],
            "menu_order": 0,
            "meta_data": [],
            "_links": {
                "self": [
                {
                    "href": "https://example.com/wp-json/wc/v3/products/22/variations/732"
                }
                ],
                "collection": [
                {
                    "href": "https://example.com/wp-json/wc/v3/products/22/variations"
                }
                ],
                "up": [
                {
                    "href": "https://example.com/wp-json/wc/v3/products/22"
                }
                ]
            }
        }