"""Declares :class:`Product`."""
import datetime
import typing

import pydantic

from .productattributeref import ProductAttributeRef
from .productcategoryref import ProductCategoryRef
from .productdefaultattribute import ProductDefaultAttribute
from .productdimensions import ProductDimensions
from .productdownload import ProductDownload
from .productimage import ProductImage
from .productmetadataproperty import ProductMetadataProperty
from .productstatus import ProductStatus
from .producttagref import ProductTagRef
from .producttype import ProductType
from .resourcelink import ResourceLink
from .woocommercemodel import WooCommerceModel


class Product(WooCommerceModel):
    __module__: str = 'libapi.woocommerce.schema.v3'

    name: str
    slug: str = ""
    permalink: str | None = None
    type: ProductType = ProductType.simple
    status: ProductStatus = ProductStatus.publish
    featured: bool = False
    description: str = ""
    short_description: str = ""
    sku: str = ""
    price: str = ""
    regular_price: str = ""
    sale_price: str = ""
    date_on_sale_from: datetime.datetime | None = None
    date_on_sale_from_gmt: datetime.datetime | None = None
    date_on_sale_to: datetime.datetime | None = None
    date_on_sale_to_gmt: datetime.datetime | None = None
    price_html: str = ""
    on_sale: bool = False
    purchasable: bool = False
    total_sales: int = 0
    virtual: bool = False
    downloadable: bool = False
    downloads: list[ProductDownload] = []
    download_limit: int = -1
    download_expiry: int = -1
    external_url: str = ""
    button_text: str = ""
    tax_status: str = "taxable"
    tax_class: str = ""
    manage_stock: bool = False
    stock_quantity: int | None = None
    stock_status: str = "instock"
    backorders: str = "no"
    backorders_allowed: bool = False
    backordered: bool = False
    sold_individually: bool = False
    weight: str = ""
    dimensions: ProductDimensions = pydantic.Field(
        default={
            "width": "",
            "height": "",
            "length": ""
        }
    )
    shipping_required: bool = True
    shipping_taxable: bool = True
    shipping_class: str = ""
    shipping_class_id: int = 0
    reviews_allowed: bool = True
    average_rating: str = "0.00"
    rating_count: int = 0
    related_ids: list[int] = []
    upsell_ids: list[int] = []
    cross_sell_ids: list[int] = []
    parent_id: int = 0
    purchase_note: str = ""
    categories: list[ProductCategoryRef] = []
    tags: list[ProductTagRef] = []
    images: list[ProductImage] = []
    attributes: list[ProductAttributeRef] = []
    default_attributes: list[ProductDefaultAttribute] = []
    variations: list[int] = []
    grouped_products: list[int] = []
    menu_order: int = 0
    meta_data: list[ProductMetadataProperty] = []
    links: dict[str, list[ResourceLink]] = pydantic.Field(
        alias='_links',
        default={}
    )

    class Config:
        title: str = "WooCommerceProduct"
        example: dict[str, typing.Any] = {
            "id": 794,
            "name": "Premium Quality",
            "slug": "premium-quality-19",
            "permalink": "https://example.com/product/premium-quality-19/",
            "date_created": "2017-03-23T17:01:14",
            "date_created_gmt": "2017-03-23T20:01:14",
            "date_modified": "2017-03-23T17:01:14",
            "date_modified_gmt": "2017-03-23T20:01:14",
            "type": "simple",
            "status": "publish",
            "featured": False,
            "catalog_visibility": "visible",
            "description": "<p>Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.</p>\n",
            "short_description": "<p>Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.</p>\n",
            "sku": "",
            "price": "21.99",
            "regular_price": "21.99",
            "sale_price": "",
            "date_on_sale_from": None,
            "date_on_sale_from_gmt": None,
            "date_on_sale_to": None,
            "date_on_sale_to_gmt": None,
            "price_html": "<span class=\"woocommerce-Price-amount amount\"><span class=\"woocommerce-Price-currencySymbol\">&#36;</span>21.99</span>",
            "on_sale": False,
            "purchasable": True,
            "total_sales": 0,
            "virtual": False,
            "downloadable": False,
            "downloads": [],
            "download_limit": -1,
            "download_expiry": -1,
            "external_url": "",
            "button_text": "",
            "tax_status": "taxable",
            "tax_class": "",
            "manage_stock": False,
            "stock_quantity": None,
            "stock_status": "instock",
            "backorders": "no",
            "backorders_allowed": False,
            "backordered": False,
            "sold_individually": False,
            "weight": "",
            "dimensions": {
                "length": "",
                "width": "",
                "height": ""
            },
            "shipping_required": True,
            "shipping_taxable": True,
            "shipping_class": "",
            "shipping_class_id": 0,
            "reviews_allowed": True,
            "average_rating": "0.00",
            "rating_count": 0,
            "related_ids": [
                53,
                40,
                56,
                479,
                99
            ],
            "upsell_ids": [],
            "cross_sell_ids": [],
            "parent_id": 0,
            "purchase_note": "",
            "categories": [
                {
                "id": 9,
                "name": "Clothing",
                "slug": "clothing"
                },
                {
                "id": 14,
                "name": "T-shirts",
                "slug": "t-shirts"
                }
            ],
            "tags": [],
            "images": [
                {
                "id": 792,
                "date_created": "2017-03-23T14:01:13",
                "date_created_gmt": "2017-03-23T20:01:13",
                "date_modified": "2017-03-23T14:01:13",
                "date_modified_gmt": "2017-03-23T20:01:13",
                "src": "https://example.com/wp-content/uploads/2017/03/T_2_front-4.jpg",
                "name": "",
                "alt": ""
                },
                {
                "id": 793,
                "date_created": "2017-03-23T14:01:14",
                "date_created_gmt": "2017-03-23T20:01:14",
                "date_modified": "2017-03-23T14:01:14",
                "date_modified_gmt": "2017-03-23T20:01:14",
                "src": "https://example.com/wp-content/uploads/2017/03/T_2_back-2.jpg",
                "name": "",
                "alt": ""
                }
            ],
            "attributes": [],
            "default_attributes": [],
            "variations": [],
            "grouped_products": [],
            "menu_order": 0,
            "meta_data": [],
            "_links": {
                "self": [
                {
                    "href": "https://example.com/wp-json/wc/v3/products/794"
                }
                ],
                "collection": [
                {
                    "href": "https://example.com/wp-json/wc/v3/products"
                }
                ]
            }
        }
