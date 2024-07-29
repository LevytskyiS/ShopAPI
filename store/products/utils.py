from django.apps import apps
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from .serializers import (
    CategorySerializer,
    GenderSerializer,
    TrademarkSerializer,
    ProductTypeSerializer,
    SubtitleSerializer,
    SpecificationSerializer,
    DescriptionSerializer,
    ProductSerializer,
    ColorSerializer,
    ProductVariantSerializer,
    SizeSerializer,
    NomenclatureSerializer,
)

from .models import (
    Category,
    Gender,
    Trademark,
    ProductType,
    Subtitle,
    Specification,
    Description,
    Product,
    Color,
    ProductVariant,
    Size,
    Nomenclature,
)

APP_NAME = "products"

model_serializers_mapping = {
    "Category": CategorySerializer,
    "Gender": GenderSerializer,
    "Trademark": TrademarkSerializer,
    "ProductType": ProductTypeSerializer,
    "Subtitle": SubtitleSerializer,
    "Specification": SpecificationSerializer,
    "Description": DescriptionSerializer,
    "Product": ProductSerializer,
    "Color": ColorSerializer,
    "ProductVariant": ProductVariantSerializer,
    "Size": SizeSerializer,
    "Nomenclature": NomenclatureSerializer,
}

models = {
    "Category": Category,
    "Gender": Gender,
    "Trademark": Trademark,
    "ProductType": ProductType,
    "Subtitle": Subtitle,
    "Specification": Specification,
    "Description": Description,
    "Product": Product,
    "Color": Color,
    "ProductVariant": ProductVariant,
    "Size": Size,
    "Nomenclature": Nomenclature,
}


def get_categories(data: list) -> dict:
    categories = []
    seen = set()

    for product in data:
        category_name = product.get("categoryName")
        category_code = product.get("categoryCode")
        category = (category_name, category_code)

        if category not in seen:
            if "Trucker 5P" in category_name:
                print(category_name)
            seen.add(category)
            categories.append({"name": category_name, "code": category_code})

    if categories:
        return {"Category": categories}


def get_genders(data: list) -> dict:
    genders = []
    seen = set()

    for product in data:
        gender_name = product.get("gender")
        gender_code = product.get("genderCode")
        gender = (gender_name, gender_code)

        if not gender_code and not gender_name:
            continue

        if gender not in seen:
            seen.add(gender)
            genders.append({"name": gender_name, "code": gender_code})

    if genders:
        return {"Gender": genders}


def get_trademarks(data: list) -> dict:
    trademarks = []
    seen = set()

    for poduct in data:
        trademark = poduct.get("trademark")

        if not trademark:
            continue

        if trademark not in seen:
            seen.add(trademark)
            trademarks.append({"trademark": trademark})

    if trademarks:
        return {"Trademark": trademarks}


def get_product_types(data: list) -> dict:
    types = []
    seen = set()

    for product in data:
        kind = product.get("type")

        if not kind or kind in seen:
            continue

        seen.add(kind)
        types.append({"type": kind})

    if types:
        return {"ProductType": types}


def get_subtitles(data: list) -> dict:
    seen_subtitles = set()
    subtitles = []

    for product in data:
        subtitle = product.get("subtitle")

        if subtitle and subtitle not in seen_subtitles:
            seen_subtitles.add(subtitle)
            subtitles.append({"subtitle": subtitle})

    if subtitles:
        return {"Subtitle": subtitles}


def get_specifications(data: list) -> dict:
    seen_specifications = set()
    specifications = []

    for product in data:
        specification = product.get("specification")

        if specification and specification not in seen_specifications:
            seen_specifications.add(specification)
            specifications.append({"specification": specification})

    if specifications:
        return {"Specification": specifications}


def get_descriptions(data: list) -> dict:
    seen_descriptions = set()
    descriptions = []

    for product in data:
        description = product.get("description")

        if description and description not in seen_descriptions:
            seen_descriptions.add(description)
            descriptions.append({"description": description})

    if descriptions:
        return {"Description": descriptions}


def get_products(data: list) -> dict:
    products = []
    for product in data:
        name = product.get("name")
        code = product.get("code")
        if not name and not code:
            continue
        products.append(
            {
                "name": name,
                "code": code,
                "category": product.get("categoryName"),
                "gender": product.get("gender"),
                "trademark": product.get("trademark"),
                "type": product.get("type"),
                "subtitle": product.get("subtitle"),
                "specification": product.get("specification"),
            }
        )

    if products:
        return {"Product": products}


def get_colors(data: list) -> dict:
    colors = []
    colors_seen = set()

    for product in data:
        variants = product.get("variants")
        if not variants:
            continue
        for variant in variants:
            color_name = variant.get("name")
            color_code = variant.get("colorCode")
            color_image = variant.get("colorIconLink")
            size = (color_name, color_code), color_image

            if size and size not in colors_seen:
                colors_seen.add(size)
                colors.append(
                    {"name": color_name, "code": color_code, "image": color_image}
                )

    if colors:
        return {"Color": colors}


def get_products_variants(data: list) -> dict:
    product_variants = []

    for product in data:
        variants = product.get("variants")
        if variants:
            for variant in variants:
                product_variants.append(
                    {
                        "code": variant.get("code"),
                        "colorCode": variant.get("colorCode"),
                    }
                )
    if product_variants:
        return {"ProductVariant": product_variants}


def get_sizes(data: list) -> dict:
    sizes = []
    sizes_seen = set()

    for product in data:
        variants = product.get("variants")
        if not variants:
            continue
        for variant in variants:
            for nomenclature in variant.get("nomenclatures"):
                size_name = nomenclature.get("sizeName")
                size_code = nomenclature.get("sizeCode")
                size = (size_name, size_code)

                if size and size not in sizes_seen:
                    sizes_seen.add(size)
                    sizes.append({"name": size_name, "code": size_code})

    if sizes:
        return {"Size": sizes}


def get_nomenclatures(data: list) -> list:
    nomenclatures = []
    seen = set()

    for product in data:
        variants = product.get("variants")

        if variants:
            for variant in variants:
                variant_nomenclatures = variant.get("nomenclatures")

                if variant_nomenclatures:
                    for item_data in variant_nomenclatures:
                        code = item_data.get("productSizeCode")
                        size = item_data.get("sizeCode")
                        ean = item_data.get("ean")
                        item = (size, code, ean)

                        if item not in seen:
                            seen.add(item)
                            nomenclatures.append(
                                {
                                    "code": code,
                                    "size": size,
                                    "ean": ean,
                                }
                            )

    if nomenclatures:
        return {"Nomenclature": nomenclatures}


def parse_json_data(data: list):
    categories = get_categories(data)
    genders = get_genders(data)
    trademarks = get_trademarks(data)
    product_types = get_product_types(data)
    subtitles = get_subtitles(data)
    specifications = get_specifications(data)
    descriptions = get_descriptions(data)
    products = get_products(data)
    colors = get_colors(data)
    products_variants = get_products_variants(data)
    sizes = get_sizes(data)
    nomenclatures = get_nomenclatures(data)

    return [
        categories,
        genders,
        trademarks,
        product_types,
        subtitles,
        specifications,
        descriptions,
        products,
        colors,
        products_variants,
        sizes,
        nomenclatures,
    ]


def filter_models(model_name: str):
    """Find and retrieve models by name."""
    app_models = apps.get_app_config(APP_NAME).get_models()

    for model in app_models:
        if model.__name__.lower() == model_name.lower():
            return model.objects.all()

    return Response(
        {"error": f"No model with name '{model_name}' was found"},
        status=status.HTTP_404_NOT_FOUND,
    )


def filter_models(model_name: str):
    """Find and retrieve models by name."""
    app_models = apps.get_app_config(APP_NAME).get_models()

    for model in app_models:
        if model.__name__.lower() == model_name.lower():
            return model.objects.all()

    return Response(
        {"error": f"No model with name '{model_name}' was found"},
        status=status.HTTP_404_NOT_FOUND,
    )


def get_deserialized_object(obj: object) -> ReturnDict:
    for key, value in models.items():
        if isinstance(obj, value):
            return model_serializers_mapping[key](obj).data
